"""
AIRS MLOps Lab - Verification Leaderboard

FastAPI application that receives verification webhooks from Claude Code
and displays real-time student progress on an instructor-facing dashboard.

In-memory storage — suitable for a 2-day workshop.
Features: SSE live updates, toast notifications, confetti celebrations.
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import time
from collections import deque
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AIRS MLOps Lab Leaderboard",
    description="Instructor-facing dashboard for student verification progress",
    version="2.0.0",
)

# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------

# { student_id: StudentRecord }
students_db: dict[str, dict[str, Any]] = {}

# Event log for activity feed (last 50 events)
event_log: deque[dict[str, Any]] = deque(maxlen=50)

# SSE subscribers (set of asyncio.Queue)
sse_subscribers: set[asyncio.Queue] = set()

# Track first-to-complete per module
first_completions: dict[str, str] = {}  # module -> student_id

# Module metadata — titles for Modules 0-7
MODULE_META: dict[str, str] = {
    "module-0": "Setup",
    "module-1": "ML Fundamentals",
    "module-2": "Train",
    "module-3": "Deploy",
    "module-4": "AIRS Deep Dive",
    "module-5": "Pipeline",
    "module-6": "Threat Zoo",
    "module-7": "Gaps",
}

# Act boundaries
MODULE_ACTS: dict[str, str] = {
    "module-0": "Build It",
    "module-1": "Build It",
    "module-2": "Build It",
    "module-3": "Build It",
    "module-4": "Understand",
    "module-5": "Secure It",
    "module-6": "Secure It",
    "module-7": "Secure It",
}

# Points per module
MODULE_POINTS: dict[str, int] = {
    "module-0": 5,
    "module-1": 10,
    "module-2": 15,
    "module-3": 15,
    "module-4": 10,
    "module-5": 15,
    "module-6": 15,
    "module-7": 20,
}

MAX_POINTS = sum(MODULE_POINTS.values())  # 105


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class VerificationResults(BaseModel):
    status: str = Field(..., description="complete or incomplete")
    verified: bool = Field(default=False)
    checks_passed: list[str] = Field(default_factory=list)
    points_awarded: int | None = Field(
        default=None,
        description="Total points awarded by verify command (preferred over fallback)",
    )
    quiz_score: int | None = Field(default=None)
    summary: str = Field(default="")


class VerificationPayload(BaseModel):
    student_id: str
    module: str
    track: str = Field(default="")
    verification_hash: str = Field(default="")
    timestamp: str = Field(default="")
    results: VerificationResults


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def relative_time(iso_timestamp: str) -> str:
    """Convert ISO timestamp to human-readable relative time."""
    try:
        dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = now - dt
        seconds = int(diff.total_seconds())

        if seconds < 0:
            return "just now"
        if seconds < 60:
            return f"{seconds}s ago"
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} min ago"
        hours = minutes // 60
        if hours < 24:
            return f"{hours}h ago"
        days = hours // 24
        return f"{days}d ago"
    except Exception:
        return "unknown"


def compute_points(student: dict[str, Any]) -> int:
    """Compute total points for a student based on completed modules.

    Uses points_awarded from verification payload when available (new format).
    Falls back to MODULE_POINTS lookup for older payloads.
    """
    total = 0
    modules = student.get("modules", {})
    for mod_key, mod_data in modules.items():
        if mod_data.get("status") == "complete" and mod_data.get("verified"):
            # Prefer points_awarded from verify command (new format)
            awarded = mod_data.get("points_awarded")
            if awarded is not None and isinstance(awarded, int):
                total += awarded
            else:
                # Fallback for old-format payloads without points_awarded
                total += MODULE_POINTS.get(mod_key, 10)
                quiz = mod_data.get("quiz_score")
                if quiz is not None and isinstance(quiz, int):
                    total += quiz
    return total


def get_completed_count(student: dict[str, Any]) -> int:
    """Count completed modules for a student."""
    return sum(
        1
        for m in student.get("modules", {}).values()
        if m.get("status") == "complete" and m.get("verified")
    )


def detect_milestones(
    student_id: str, module: str, student: dict[str, Any]
) -> list[dict[str, Any]]:
    """Detect celebration-worthy milestones."""
    milestones = []
    completed = get_completed_count(student)
    mod_title = MODULE_META.get(module, module)

    # First to complete this module
    if module not in first_completions:
        first_completions[module] = student_id
        milestones.append(
            {
                "type": "first_completion",
                "message": f"First to complete {mod_title}!",
                "icon": "trophy",
                "confetti": True,
            }
        )

    # Act 1 complete (finished module-3)
    act1_modules = {"module-0", "module-1", "module-2", "module-3"}
    student_modules = {
        k
        for k, v in student.get("modules", {}).items()
        if v.get("status") == "complete" and v.get("verified")
    }
    if module == "module-3" and act1_modules.issubset(student_modules):
        milestones.append(
            {
                "type": "act_complete",
                "message": "Act 1 Complete: Build It!",
                "icon": "rocket",
                "confetti": True,
            }
        )

    # All modules complete
    if completed == len(MODULE_META):
        milestones.append(
            {
                "type": "full_complete",
                "message": "ALL MODULES COMPLETE!",
                "icon": "star",
                "confetti": True,
            }
        )

    # Point milestones
    points = student.get("total_points", 0)
    if points >= 50 and (points - MODULE_POINTS.get(module, 0)) < 50:
        milestones.append(
            {
                "type": "points_milestone",
                "message": "50+ Points!",
                "icon": "fire",
                "confetti": False,
            }
        )
    if points >= 100 and (points - MODULE_POINTS.get(module, 0)) < 100:
        milestones.append(
            {
                "type": "points_milestone",
                "message": "100+ Points!",
                "icon": "fire",
                "confetti": True,
            }
        )

    return milestones


async def broadcast_event(event: dict[str, Any]) -> None:
    """Push an event to all connected SSE subscribers."""
    event_log.append(event)
    dead = []
    for queue in sse_subscribers:
        try:
            queue.put_nowait(event)
        except asyncio.QueueFull:
            dead.append(queue)
    for q in dead:
        sse_subscribers.discard(q)


def get_rankings() -> list[dict[str, Any]]:
    """Get current student rankings."""
    return sorted(
        students_db.values(),
        key=lambda s: (s.get("total_points", 0), -len(s.get("modules", {}))),
        reverse=True,
    )


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/verify")
async def receive_verification(payload: VerificationPayload):
    """Receive a verification webhook from Claude Code."""
    student_id = payload.student_id
    module = payload.module
    ts = payload.timestamp or datetime.now(timezone.utc).isoformat()

    # Capture old rank for comparison
    old_rankings = [s["student_id"] for s in get_rankings()]
    old_rank = (
        old_rankings.index(student_id) + 1
        if student_id in old_rankings
        else len(old_rankings) + 1
    )
    old_points = (
        students_db[student_id].get("total_points", 0)
        if student_id in students_db
        else 0
    )

    # Initialize student record if new
    is_new = student_id not in students_db
    if is_new:
        students_db[student_id] = {
            "student_id": student_id,
            "track": payload.track or "",
            "modules": {},
            "first_seen": ts,
            "last_active": ts,
        }

    student = students_db[student_id]
    student["last_active"] = ts
    if payload.track:
        student["track"] = payload.track

    # Store module results
    student["modules"][module] = {
        "status": payload.results.status,
        "verified": payload.results.verified,
        "checks_passed": payload.results.checks_passed,
        "points_awarded": payload.results.points_awarded,
        "quiz_score": payload.results.quiz_score,
        "summary": payload.results.summary,
        "verification_hash": payload.verification_hash,
        "timestamp": ts,
    }

    # Recompute points
    student["total_points"] = compute_points(student)
    new_points = student["total_points"]

    # New rank
    new_rankings = [s["student_id"] for s in get_rankings()]
    new_rank = new_rankings.index(student_id) + 1

    # Detect milestones
    milestones = []
    if payload.results.status == "complete" and payload.results.verified:
        milestones = detect_milestones(student_id, module, student)

    # Build event
    mod_title = MODULE_META.get(module, module)
    event = {
        "type": "verification",
        "student_id": student_id,
        "module": module,
        "module_title": mod_title,
        "track": student.get("track", ""),
        "verified": payload.results.verified,
        "status": payload.results.status,
        "points_before": old_points,
        "points_after": new_points,
        "points_delta": new_points - old_points,
        "rank_before": old_rank,
        "rank_after": new_rank,
        "rank_delta": old_rank - new_rank,
        "completed_count": get_completed_count(student),
        "total_modules": len(MODULE_META),
        "milestones": milestones,
        "is_new_student": is_new,
        "timestamp": ts,
    }

    await broadcast_event(event)

    return {
        "status": "accepted",
        "student_id": student_id,
        "module": module,
        "total_points": new_points,
    }


@app.get("/api/students")
async def list_students():
    """Return all student data as JSON."""
    students = get_rankings()
    return {"students": students, "count": len(students)}


@app.get("/api/students/{student_id}")
async def get_student(student_id: str):
    """Return full detail for a single student."""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]


@app.get("/api/events")
async def event_stream(request: Request):
    """SSE endpoint for live dashboard updates."""
    queue: asyncio.Queue = asyncio.Queue(maxsize=100)
    sse_subscribers.add(queue)

    async def event_generator():
        try:
            # Send initial state
            students = get_rankings()
            yield {
                "event": "init",
                "data": json.dumps(
                    {
                        "students": students,
                        "event_log": list(event_log),
                        "first_completions": first_completions,
                    },
                    default=str,
                ),
            }
            while True:
                if await request.is_disconnected():
                    break
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield {
                        "event": "verification",
                        "data": json.dumps(event, default=str),
                    }
                except asyncio.TimeoutError:
                    # Send keepalive
                    yield {"event": "ping", "data": "{}"}
        finally:
            sse_subscribers.discard(queue)

    return EventSourceResponse(event_generator())


@app.get("/api/feed")
async def get_feed():
    """Return recent event log as JSON."""
    return {"events": list(event_log), "count": len(event_log)}


@app.get("/api/export")
async def export_state():
    """Export full in-memory state for backup before redeploy.

    Usage: curl $URL/api/export > backup.json
    """
    return {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "students": dict(students_db),
        "event_log": list(event_log),
        "first_completions": dict(first_completions),
    }


@app.post("/api/import")
async def import_state(request: Request):
    """Restore state from a previous /api/export backup.

    Usage: curl -X POST $URL/api/import -H 'Content-Type: application/json' -d @backup.json

    Clears existing state and replaces with imported data.
    Reconstructs first_completions from timestamps if not provided.
    Does NOT trigger SSE events or milestone detection.
    """
    data = await request.json()

    # Validate structure
    if "students" not in data:
        raise HTTPException(status_code=400, detail="Missing 'students' key in payload")

    # Clear and restore students
    students_db.clear()
    students_db.update(data["students"])

    # Recompute points for all students (in case scoring logic changed)
    for student in students_db.values():
        student["total_points"] = compute_points(student)

    # Restore event log
    event_log.clear()
    for evt in data.get("event_log", []):
        event_log.append(evt)

    # Restore or reconstruct first_completions
    first_completions.clear()
    if data.get("first_completions"):
        first_completions.update(data["first_completions"])
    else:
        # Reconstruct from student timestamps
        for sid, student in students_db.items():
            for mod_key, mod_data in student.get("modules", {}).items():
                if mod_data.get("status") == "complete" and mod_data.get("verified"):
                    ts = mod_data.get("timestamp", "")
                    if mod_key not in first_completions:
                        first_completions[mod_key] = sid
                    else:
                        # Keep the earliest timestamp
                        existing_sid = first_completions[mod_key]
                        existing_ts = (
                            students_db[existing_sid]
                            .get("modules", {})
                            .get(mod_key, {})
                            .get("timestamp", "")
                        )
                        if ts and existing_ts and ts < existing_ts:
                            first_completions[mod_key] = sid

    return {
        "status": "imported",
        "students_count": len(students_db),
        "events_count": len(event_log),
        "first_completions": dict(first_completions),
    }


# ---------------------------------------------------------------------------
# Dashboard HTML
# ---------------------------------------------------------------------------

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AIRS MLOps Lab — Leaderboard</title>
<style>
  :root {
    --bg-dark: #0a0c10;
    --bg-card: #13161f;
    --bg-header: #0f1219;
    --bg-feed: #111318;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-green: #22c55e;
    --accent-yellow: #eab308;
    --accent-orange: #f97316;
    --accent-red: #ef4444;
    --accent-purple: #a855f7;
    --accent-pink: #ec4899;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: #1e2433;
    --border-bright: #2d3a52;
    --row-hover: #161b28;
    --glow-blue: rgba(59,130,246,0.15);
    --glow-green: rgba(34,197,94,0.2);
    --glow-gold: rgba(251,191,36,0.2);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: 'SF Mono', 'Cascadia Code', 'JetBrains Mono', 'Fira Code', monospace;
    background: var(--bg-dark);
    color: var(--text-primary);
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* ---- Layout ---- */
  .layout {
    display: grid;
    grid-template-columns: 1fr 320px;
    grid-template-rows: auto auto 1fr;
    min-height: 100vh;
  }
  .header { grid-column: 1 / -1; }
  .stats-bar { grid-column: 1 / -1; }
  .main { grid-column: 1; overflow-y: auto; }
  .feed { grid-column: 2; border-left: 1px solid var(--border); overflow-y: auto; max-height: calc(100vh - 130px); }

  /* ---- Header ---- */
  .header {
    background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
    border-bottom: 1px solid var(--border);
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  .header-logo {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 0.8rem; color: #fff;
    box-shadow: 0 0 20px rgba(59,130,246,0.3);
  }
  .header h1 {
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.02em;
  }
  .header h1 .accent { color: var(--accent-blue); }
  .header h1 .dim { color: var(--text-muted); font-weight: 400; }
  .header-right {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.75rem;
    color: var(--text-secondary);
  }
  .live-badge {
    display: flex; align-items: center; gap: 0.4rem;
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 999px;
    padding: 0.25rem 0.6rem;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--accent-green);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .live-dot {
    width: 6px; height: 6px;
    background: var(--accent-green);
    border-radius: 50%;
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(34,197,94,0.4); }
    50% { opacity: 0.6; box-shadow: 0 0 0 4px rgba(34,197,94,0); }
  }
  .connection-status {
    font-size: 0.65rem;
    color: var(--text-muted);
  }
  .connection-status.connected { color: var(--accent-green); }
  .connection-status.disconnected { color: var(--accent-red); }

  /* ---- Stats bar ---- */
  .stats-bar {
    display: flex;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: var(--bg-header);
    border-bottom: 1px solid var(--border);
  }
  .stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.5rem 1rem;
    flex: 1;
    max-width: 180px;
    position: relative;
    overflow: hidden;
  }
  .stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent-blue);
    opacity: 0.5;
  }
  .stat-card .label {
    font-size: 0.6rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .stat-card .value {
    font-size: 1.4rem;
    font-weight: 800;
    margin-top: 0.1rem;
    font-variant-numeric: tabular-nums;
    background: linear-gradient(135deg, var(--text-primary), var(--accent-blue));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .stat-card.highlight .value {
    background: linear-gradient(135deg, var(--accent-yellow), var(--accent-orange));
    -webkit-background-clip: text;
    background-clip: text;
  }

  /* ---- Table ---- */
  .table-wrap {
    padding: 1rem 1.5rem;
    overflow-x: auto;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.8rem;
  }
  thead th {
    background: var(--bg-header);
    color: var(--text-muted);
    font-weight: 600;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.6rem 0.5rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
    position: sticky;
    top: 0;
    z-index: 2;
  }
  thead th.module-col {
    text-align: center;
    min-width: 64px;
  }
  /* Act boundary indicator */
  thead th.act-boundary {
    border-left: 2px solid var(--accent-purple);
  }
  tbody tr {
    border-bottom: 1px solid var(--border);
    transition: all 0.3s ease;
  }
  tbody tr:hover {
    background: var(--row-hover);
  }
  tbody tr.highlight-new {
    animation: rowGlow 2s ease-out;
  }
  @keyframes rowGlow {
    0% { background: var(--glow-green); box-shadow: inset 0 0 30px var(--glow-green); }
    100% { background: transparent; box-shadow: none; }
  }
  @keyframes rowRankUp {
    0% { background: var(--glow-gold); }
    100% { background: transparent; }
  }
  td {
    padding: 0.6rem 0.5rem;
    vertical-align: middle;
  }
  td.act-boundary {
    border-left: 2px solid rgba(168,85,247,0.3);
  }

  /* Rank */
  .rank {
    font-weight: 800;
    color: var(--text-muted);
    width: 36px;
    text-align: center;
    font-size: 0.85rem;
  }
  .rank-1 { color: #fbbf24; text-shadow: 0 0 10px rgba(251,191,36,0.5); }
  .rank-2 { color: #d1d5db; text-shadow: 0 0 8px rgba(209,213,219,0.3); }
  .rank-3 { color: #d97706; text-shadow: 0 0 8px rgba(217,119,6,0.3); }

  /* Student name */
  .student-cell {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .student-name {
    font-weight: 700;
    color: var(--text-primary);
    font-size: 0.85rem;
  }
  .track-badge {
    font-size: 0.55rem;
    padding: 0.1rem 0.35rem;
    border-radius: 3px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }
  .track-ts { background: rgba(59,130,246,0.15); color: var(--accent-blue); border: 1px solid rgba(59,130,246,0.3); }
  .track-sp { background: rgba(168,85,247,0.15); color: var(--accent-purple); border: 1px solid rgba(168,85,247,0.3); }

  /* Module cells */
  .mod-cell {
    text-align: center;
    font-size: 0.9rem;
    cursor: default;
    position: relative;
    transition: all 0.3s;
  }
  .mod-complete {
    color: var(--accent-green);
  }
  .mod-complete.first-badge::after {
    content: '\u2605';
    position: absolute;
    top: -2px; right: 2px;
    font-size: 0.5rem;
    color: var(--accent-yellow);
  }
  .mod-progress {
    color: var(--accent-yellow);
  }
  .mod-empty {
    color: var(--text-muted);
    opacity: 0.2;
  }
  .mod-cell.just-completed {
    animation: moduleComplete 1.5s ease-out;
  }
  @keyframes moduleComplete {
    0% { transform: scale(1); }
    20% { transform: scale(1.8); filter: brightness(2); }
    40% { transform: scale(1.2); }
    60% { transform: scale(1.4); filter: brightness(1.5); }
    100% { transform: scale(1); filter: brightness(1); }
  }

  /* Progress bar */
  .progress-bar-wrap {
    width: 50px;
    height: 4px;
    background: var(--border);
    border-radius: 2px;
    overflow: hidden;
    margin-top: 2px;
  }
  .progress-bar-fill {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan));
    transition: width 0.8s cubic-bezier(0.22, 1, 0.36, 1);
  }

  /* Points */
  .points {
    font-weight: 800;
    font-variant-numeric: tabular-nums;
    font-size: 0.95rem;
  }
  .points-value {
    background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .points-delta {
    font-size: 0.6rem;
    color: var(--accent-green);
    font-weight: 700;
    animation: pointsPop 0.6s ease-out;
  }
  @keyframes pointsPop {
    0% { transform: translateY(10px); opacity: 0; }
    50% { transform: translateY(-3px); }
    100% { transform: translateY(0); opacity: 1; }
  }

  /* Last active */
  .last-active {
    color: var(--text-muted);
    font-size: 0.7rem;
    white-space: nowrap;
  }

  /* ---- Activity Feed ---- */
  .feed {
    background: var(--bg-feed);
    padding: 0;
  }
  .feed-header {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border);
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    position: sticky;
    top: 0;
    background: var(--bg-feed);
    z-index: 2;
  }
  .feed-header .count {
    background: var(--accent-blue);
    color: #fff;
    font-size: 0.55rem;
    padding: 0.1rem 0.35rem;
    border-radius: 999px;
    min-width: 18px;
    text-align: center;
  }
  .feed-items {
    padding: 0.5rem;
  }
  .feed-item {
    padding: 0.6rem 0.75rem;
    border-radius: 6px;
    margin-bottom: 0.4rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    font-size: 0.72rem;
    line-height: 1.4;
    animation: feedSlide 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    transition: border-color 0.3s;
  }
  .feed-item:hover {
    border-color: var(--border-bright);
  }
  .feed-item.milestone {
    border-color: var(--accent-yellow);
    background: linear-gradient(135deg, rgba(251,191,36,0.05), var(--bg-card));
  }
  @keyframes feedSlide {
    0% { transform: translateX(20px); opacity: 0; }
    100% { transform: translateX(0); opacity: 1; }
  }
  .feed-item .fi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.25rem;
  }
  .feed-item .fi-name {
    font-weight: 700;
    color: var(--text-primary);
  }
  .feed-item .fi-time {
    font-size: 0.6rem;
    color: var(--text-muted);
  }
  .feed-item .fi-body {
    color: var(--text-secondary);
  }
  .feed-item .fi-module {
    color: var(--accent-cyan);
    font-weight: 600;
  }
  .feed-item .fi-points {
    color: var(--accent-green);
    font-weight: 700;
  }
  .feed-item .fi-milestone {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    margin-top: 0.3rem;
    padding: 0.15rem 0.4rem;
    background: rgba(251,191,36,0.1);
    border: 1px solid rgba(251,191,36,0.2);
    border-radius: 4px;
    font-size: 0.65rem;
    color: var(--accent-yellow);
    font-weight: 700;
  }

  /* Summary toggle */
  .summary-toggle {
    background: none;
    border: 1px solid var(--border);
    color: var(--text-muted);
    border-radius: 3px;
    padding: 0.1rem 0.3rem;
    font-size: 0.6rem;
    cursor: pointer;
    transition: all 0.15s;
    font-family: inherit;
  }
  .summary-toggle:hover {
    border-color: var(--accent-blue);
    color: var(--accent-blue);
  }
  .summary-row td {
    padding: 0 0.5rem 0.5rem 3rem;
    border-bottom: 1px solid var(--border);
  }
  .summary-content {
    background: var(--bg-header);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.5rem 0.75rem;
    font-size: 0.7rem;
    color: var(--text-secondary);
    line-height: 1.4;
    max-width: 800px;
  }
  .summary-module { margin-bottom: 0.35rem; }
  .summary-module strong { color: var(--text-primary); }

  /* ---- Toast notifications ---- */
  .toast-container {
    position: fixed;
    top: 1rem;
    right: 340px;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    pointer-events: none;
  }
  .toast {
    background: var(--bg-card);
    border: 1px solid var(--border-bright);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    min-width: 280px;
    max-width: 380px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    animation: toastIn 0.4s cubic-bezier(0.22, 1, 0.36, 1), toastOut 0.3s ease-in 4.7s forwards;
    font-size: 0.8rem;
    pointer-events: auto;
  }
  .toast.milestone-toast {
    border-color: var(--accent-yellow);
    box-shadow: 0 8px 32px rgba(251,191,36,0.15);
  }
  @keyframes toastIn {
    0% { transform: translateX(100px) scale(0.8); opacity: 0; }
    100% { transform: translateX(0) scale(1); opacity: 1; }
  }
  @keyframes toastOut {
    0% { transform: translateX(0); opacity: 1; }
    100% { transform: translateX(100px); opacity: 0; }
  }
  .toast .toast-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.25rem;
  }
  .toast .toast-name { font-weight: 700; }
  .toast .toast-points { color: var(--accent-green); font-weight: 800; }
  .toast .toast-body { color: var(--text-secondary); font-size: 0.75rem; }
  .toast .toast-milestone {
    margin-top: 0.3rem;
    font-size: 0.75rem;
    color: var(--accent-yellow);
    font-weight: 700;
  }

  /* ---- Confetti ---- */
  .confetti-container {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 9999;
    overflow: hidden;
  }
  .confetti-piece {
    position: absolute;
    width: 10px; height: 10px;
    top: -10px;
    animation: confettiFall linear forwards;
  }
  @keyframes confettiFall {
    0% { transform: translateY(0) rotate(0deg); opacity: 1; }
    100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
  }

  /* ---- Empty state ---- */
  .empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
    grid-column: 1;
  }
  .empty-state h2 {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
    color: var(--text-secondary);
    font-weight: 600;
  }
  .empty-state p {
    font-size: 0.8rem;
    max-width: 400px;
    margin: 0 auto;
    line-height: 1.6;
  }
  .empty-state code {
    background: var(--bg-card);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    font-size: 0.75rem;
    border: 1px solid var(--border);
  }
  .empty-state .waiting-animation {
    margin: 1.5rem auto;
    display: flex;
    gap: 0.4rem;
    justify-content: center;
  }
  .empty-state .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent-blue);
    animation: waitDot 1.4s ease-in-out infinite;
  }
  .empty-state .dot:nth-child(2) { animation-delay: 0.2s; }
  .empty-state .dot:nth-child(3) { animation-delay: 0.4s; }
  @keyframes waitDot {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.3; }
    40% { transform: scale(1); opacity: 1; }
  }

  /* ---- Responsive ---- */
  @media (max-width: 1100px) {
    .layout { grid-template-columns: 1fr; }
    .feed { display: none; }
    .toast-container { right: 1rem; }
  }
</style>
</head>
<body>

<div class="layout">
  <div class="header">
    <div class="header-left">
      <div class="header-logo">AI</div>
      <h1><span class="accent">AIRS MLOps Lab</span> <span class="dim">&mdash; Leaderboard</span></h1>
    </div>
    <div class="header-right">
      <div class="live-badge"><span class="live-dot"></span> LIVE</div>
      <span class="connection-status" id="conn-status">connecting...</span>
    </div>
  </div>

  <div class="stats-bar">
    <div class="stat-card">
      <div class="label">Students</div>
      <div class="value" id="stat-students">0</div>
    </div>
    <div class="stat-card">
      <div class="label">Modules Done</div>
      <div class="value" id="stat-modules">0</div>
    </div>
    <div class="stat-card">
      <div class="label">Avg Points</div>
      <div class="value" id="stat-avg">0</div>
    </div>
    <div class="stat-card highlight">
      <div class="label">Top Score</div>
      <div class="value" id="stat-top">0</div>
    </div>
  </div>

  <div class="main">
    <div id="table-area"></div>
  </div>

  <div class="feed">
    <div class="feed-header">
      Activity Feed <span class="count" id="feed-count">0</span>
    </div>
    <div class="feed-items" id="feed-items"></div>
  </div>
</div>

<div class="toast-container" id="toast-container"></div>
<div class="confetti-container" id="confetti-container"></div>

<script>
(function() {
  // ---- State ----
  let students = [];
  let eventLog = [];
  let firstCompletions = {};
  const MODULE_KEYS = ['module-0','module-1','module-2','module-3','module-4','module-5','module-6','module-7'];
  const MODULE_TITLES = {
    'module-0':'Setup','module-1':'ML Fundamentals','module-2':'Train','module-3':'Deploy',
    'module-4':'AIRS Deep Dive','module-5':'Pipeline','module-6':'Threat Zoo','module-7':'Gaps'
  };
  const ACT_BOUNDARIES = {'module-4': true, 'module-5': true}; // act transitions
  const MILESTONE_ICONS = {
    'trophy': '\u{1F3C6}',
    'rocket': '\u{1F680}',
    'star': '\u{2B50}',
    'fire': '\u{1F525}'
  };

  // ---- SSE Connection ----
  let evtSource = null;
  function connectSSE() {
    const status = document.getElementById('conn-status');
    evtSource = new EventSource('/api/events');

    evtSource.addEventListener('init', function(e) {
      const data = JSON.parse(e.data);
      students = data.students || [];
      eventLog = data.event_log || [];
      firstCompletions = data.first_completions || {};
      status.textContent = 'connected';
      status.className = 'connection-status connected';
      renderAll();
    });

    evtSource.addEventListener('verification', function(e) {
      const event = JSON.parse(e.data);
      handleVerification(event);
    });

    evtSource.addEventListener('ping', function() {});

    evtSource.onerror = function() {
      status.textContent = 'reconnecting...';
      status.className = 'connection-status disconnected';
      evtSource.close();
      setTimeout(connectSSE, 3000);
    };
  }

  // ---- Event handling ----
  function handleVerification(event) {
    eventLog.unshift(event);
    if (eventLog.length > 50) eventLog.pop();

    // Refresh full state
    fetch('/api/students')
      .then(r => r.json())
      .then(data => {
        students = data.students;
        renderAll();
        highlightStudent(event.student_id);
      });

    // Toast
    showToast(event);

    // Feed
    renderFeed();

    // Confetti
    if (event.milestones && event.milestones.some(m => m.confetti)) {
      launchConfetti();
    }
  }

  // ---- Render ----
  function renderAll() {
    renderStats();
    renderTable();
    renderFeed();
  }

  function renderStats() {
    const count = students.length;
    const modulesDone = students.reduce((sum, s) => {
      return sum + Object.values(s.modules || {}).filter(m => m.status === 'complete' && m.verified).length;
    }, 0);
    const avg = count > 0 ? Math.round(students.reduce((s, st) => s + (st.total_points || 0), 0) / count) : 0;
    const top = students.length > 0 ? Math.max(...students.map(s => s.total_points || 0)) : 0;

    animateNumber('stat-students', count);
    animateNumber('stat-modules', modulesDone);
    animateNumber('stat-avg', avg);
    animateNumber('stat-top', top);
  }

  function animateNumber(id, target) {
    const el = document.getElementById(id);
    const current = parseInt(el.textContent) || 0;
    if (current === target) return;
    const diff = target - current;
    const steps = Math.min(Math.abs(diff), 20);
    const stepTime = 400 / steps;
    let step = 0;
    const timer = setInterval(() => {
      step++;
      el.textContent = Math.round(current + (diff * step / steps));
      if (step >= steps) { clearInterval(timer); el.textContent = target; }
    }, stepTime);
  }

  function renderTable() {
    const area = document.getElementById('table-area');
    if (students.length === 0) {
      area.innerHTML = `
        <div class="empty-state">
          <h2>Waiting for students...</h2>
          <div class="waiting-animation"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
          <p>Students will appear here as they complete modules.<br>Verifications POST to <code>/api/verify</code></p>
        </div>`;
      return;
    }

    let modHeaders = '';
    MODULE_KEYS.forEach(key => {
      const num = key.split('-')[1];
      const title = MODULE_TITLES[key];
      const boundary = ACT_BOUNDARIES[key] ? ' act-boundary' : '';
      modHeaders += '<th class="module-col' + boundary + '">M' + num + '<br><span style="font-weight:400;font-size:0.5rem;text-transform:none;letter-spacing:0">' + title + '</span></th>';
    });

    let rows = '';
    students.forEach((student, idx) => {
      const rank = idx + 1;
      const rankClass = rank <= 3 ? ' rank-' + rank : '';
      const sid = student.student_id;
      const points = student.total_points || 0;
      const completed = Object.values(student.modules || {}).filter(m => m.status === 'complete' && m.verified).length;
      const pct = Math.round((completed / MODULE_KEYS.length) * 100);
      const track = student.track || '';
      const trackBadge = track === 'ts-workshop' ? '<span class="track-badge track-ts">TS</span>'
                       : track === 'self-paced' ? '<span class="track-badge track-sp">SP</span>' : '';

      let modCells = '';
      MODULE_KEYS.forEach(key => {
        const mod = (student.modules || {})[key];
        const boundary = ACT_BOUNDARIES[key] ? ' act-boundary' : '';
        const first = firstCompletions[key] === sid ? ' first-badge' : '';
        if (!mod) {
          modCells += '<td class="mod-cell mod-empty' + boundary + '">&#183;</td>';
        } else if (mod.status === 'complete' && mod.verified) {
          modCells += '<td class="mod-cell mod-complete' + first + boundary + '" title="Complete">&#10003;</td>';
        } else {
          modCells += '<td class="mod-cell mod-progress' + boundary + '" title="In progress">&#9679;</td>';
        }
      });

      const hasSummaries = Object.values(student.modules || {}).some(m => m.summary);
      const detailBtn = hasSummaries ? ' <button class="summary-toggle" onclick="toggleSummary(' + idx + ')">+</button>' : '';

      rows += '<tr id="row-' + sid + '">' +
        '<td class="rank' + rankClass + '">' + rank + '</td>' +
        '<td><div class="student-cell"><span class="student-name">' + escHtml(sid) + '</span>' + trackBadge + detailBtn + '</div>' +
        '<div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:' + pct + '%"></div></div></td>' +
        modCells +
        '<td class="points"><span class="points-value">' + points + '</span></td>' +
        '<td class="last-active">' + relativeTime(student.last_active) + '</td></tr>';

      // Summary row
      if (hasSummaries) {
        let summaryHtml = '';
        MODULE_KEYS.forEach(key => {
          const mod = (student.modules || {})[key];
          if (mod && mod.summary) {
            const title = MODULE_TITLES[key];
            const icon = (mod.verified) ? '&#10003;' : '&#9679;';
            summaryHtml += '<div class="summary-module"><strong>' + icon + ' ' + title + '</strong>: ' + escHtml(mod.summary) + '</div>';
          }
        });
        rows += '<tr id="summary-' + idx + '" class="summary-row" style="display:none"><td colspan="12"><div class="summary-content">' + summaryHtml + '</div></td></tr>';
      }
    });

    area.innerHTML = '<div class="table-wrap"><table><thead><tr>' +
      '<th style="width:36px">#</th><th>Student</th>' + modHeaders +
      '<th>Pts</th><th>Active</th></tr></thead><tbody>' + rows + '</tbody></table></div>';
  }

  function renderFeed() {
    const container = document.getElementById('feed-items');
    const countEl = document.getElementById('feed-count');
    countEl.textContent = eventLog.length;

    let html = '';
    eventLog.slice(0, 30).forEach(evt => {
      const isMilestone = evt.milestones && evt.milestones.length > 0;
      const cls = isMilestone ? ' milestone' : '';

      let milestoneHtml = '';
      if (isMilestone) {
        evt.milestones.forEach(m => {
          const icon = MILESTONE_ICONS[m.icon] || '';
          milestoneHtml += '<div class="fi-milestone">' + icon + ' ' + escHtml(m.message) + '</div>';
        });
      }

      const deltaStr = evt.points_delta > 0 ? '+' + evt.points_delta : '' + evt.points_delta;
      html += '<div class="feed-item' + cls + '">' +
        '<div class="fi-header"><span class="fi-name">' + escHtml(evt.student_id) + '</span>' +
        '<span class="fi-time">' + relativeTime(evt.timestamp) + '</span></div>' +
        '<div class="fi-body">' +
        (evt.verified ? 'Completed' : 'Attempted') + ' <span class="fi-module">' + escHtml(evt.module_title) + '</span>' +
        ' <span class="fi-points">' + deltaStr + ' pts</span>' +
        (evt.rank_delta > 0 ? ' &#9650;' + evt.rank_delta : '') +
        '</div>' + milestoneHtml + '</div>';
    });

    container.innerHTML = html;
  }

  // ---- Highlight ----
  function highlightStudent(sid) {
    const row = document.getElementById('row-' + sid);
    if (row) {
      row.classList.add('highlight-new');
      setTimeout(() => row.classList.remove('highlight-new'), 2000);
    }
  }

  // ---- Toast ----
  function showToast(event) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    const isMilestone = event.milestones && event.milestones.length > 0;
    toast.className = 'toast' + (isMilestone ? ' milestone-toast' : '');

    let milestoneHtml = '';
    if (isMilestone) {
      event.milestones.forEach(m => {
        const icon = MILESTONE_ICONS[m.icon] || '';
        milestoneHtml += '<div class="toast-milestone">' + icon + ' ' + escHtml(m.message) + '</div>';
      });
    }

    const delta = event.points_delta > 0 ? '+' + event.points_delta : '' + event.points_delta;
    toast.innerHTML = '<div class="toast-header">' +
      '<span class="toast-name">' + escHtml(event.student_id) + '</span>' +
      '<span class="toast-points">' + delta + ' pts</span></div>' +
      '<div class="toast-body">' + (event.verified ? 'Completed' : 'Attempted') + ' ' + escHtml(event.module_title) + '</div>' +
      milestoneHtml;

    container.appendChild(toast);
    setTimeout(() => { if (toast.parentNode) toast.remove(); }, 5000);
  }

  // ---- Confetti ----
  function launchConfetti() {
    const container = document.getElementById('confetti-container');
    const colors = ['#fbbf24','#3b82f6','#22c55e','#ef4444','#a855f7','#ec4899','#06b6d4','#f97316'];
    for (let i = 0; i < 80; i++) {
      const piece = document.createElement('div');
      piece.className = 'confetti-piece';
      piece.style.left = Math.random() * 100 + 'vw';
      piece.style.background = colors[Math.floor(Math.random() * colors.length)];
      piece.style.width = (Math.random() * 8 + 4) + 'px';
      piece.style.height = (Math.random() * 8 + 4) + 'px';
      piece.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
      piece.style.animationDuration = (Math.random() * 2 + 1.5) + 's';
      piece.style.animationDelay = (Math.random() * 0.8) + 's';
      container.appendChild(piece);
      setTimeout(() => piece.remove(), 4000);
    }
  }

  // ---- Utilities ----
  function escHtml(str) {
    if (!str) return '';
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function relativeTime(ts) {
    if (!ts) return '';
    try {
      const dt = new Date(ts);
      const now = new Date();
      const diff = Math.floor((now - dt) / 1000);
      if (diff < 0) return 'just now';
      if (diff < 60) return diff + 's ago';
      const min = Math.floor(diff / 60);
      if (min < 60) return min + 'm ago';
      const hr = Math.floor(min / 60);
      if (hr < 24) return hr + 'h ago';
      return Math.floor(hr / 24) + 'd ago';
    } catch(e) { return ''; }
  }

  // ---- Summary toggle (global) ----
  window.toggleSummary = function(id) {
    const row = document.getElementById('summary-' + id);
    if (row) row.style.display = row.style.display === 'none' ? 'table-row' : 'none';
  };

  // ---- Init ----
  connectSSE();
})();
</script>
</body>
</html>"""


def _render_module_cell(mod_data: dict | None) -> str:
    """Render a single module cell as HTML (fallback for non-JS)."""
    if mod_data is None:
        return '<td class="mod-cell mod-empty">&middot;</td>'
    if mod_data.get("status") == "complete" and mod_data.get("verified"):
        return '<td class="mod-cell mod-complete">&#10003;</td>'
    return '<td class="mod-cell mod-progress">&#9679;</td>'


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the live dashboard — all rendering happens client-side via SSE."""
    return DASHBOARD_HTML
