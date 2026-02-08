"""
AIRS MLOps Lab - Verification Leaderboard

FastAPI application that receives verification webhooks from Claude Code
and displays real-time student progress on an instructor-facing dashboard.

In-memory storage — suitable for a 2-day workshop.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AIRS MLOps Lab Leaderboard",
    description="Instructor-facing dashboard for student verification progress",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------

# { student_id: StudentRecord }
students_db: dict[str, dict[str, Any]] = {}

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


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class VerificationResults(BaseModel):
    status: str = Field(..., description="complete or incomplete")
    verified: bool = Field(default=False)
    checks_passed: list[str] = Field(default_factory=list)
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
                # Fallback for old-format payloads
                total += MODULE_POINTS.get(mod_key, 10)
                quiz = mod_data.get("quiz_score")
                if quiz is not None and isinstance(quiz, int):
                    total += min(quiz // 3, 3)
    return total


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

    # Initialize student record if new
    if student_id not in students_db:
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
        "quiz_score": payload.results.quiz_score,
        "summary": payload.results.summary,
        "verification_hash": payload.verification_hash,
        "timestamp": ts,
    }

    # Recompute points
    student["total_points"] = compute_points(student)

    return {
        "status": "accepted",
        "student_id": student_id,
        "module": module,
        "total_points": student["total_points"],
    }


@app.get("/api/students")
async def list_students():
    """Return all student data as JSON."""
    students = sorted(
        students_db.values(),
        key=lambda s: s.get("total_points", 0),
        reverse=True,
    )
    return {"students": students, "count": len(students)}


@app.get("/api/students/{student_id}")
async def get_student(student_id: str):
    """Return full detail for a single student."""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]


# ---------------------------------------------------------------------------
# Dashboard HTML
# ---------------------------------------------------------------------------

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AIRS MLOps Lab - Leaderboard</title>
<style>
  :root {
    --bg-dark: #0f1117;
    --bg-card: #1a1d27;
    --bg-header: #161922;
    --accent-blue: #3b82f6;
    --accent-green: #22c55e;
    --accent-yellow: #eab308;
    --accent-red: #ef4444;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: #2d3348;
    --row-hover: #1e2235;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-dark);
    color: var(--text-primary);
    min-height: 100vh;
  }

  /* ---- Header ---- */
  .header {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-bottom: 1px solid var(--border);
    padding: 1.25rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  .header-logo {
    width: 36px; height: 36px;
    background: var(--accent-blue);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 1.1rem; color: #fff;
  }
  .header h1 {
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.01em;
  }
  .header h1 span { color: var(--accent-blue); }
  .header-right {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    font-size: 0.85rem;
    color: var(--text-secondary);
  }
  .refresh-badge {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.35rem 0.75rem;
    font-variant-numeric: tabular-nums;
  }
  .live-dot {
    width: 8px; height: 8px;
    background: var(--accent-green);
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }

  /* ---- Stats bar ---- */
  .stats-bar {
    display: flex;
    gap: 1rem;
    padding: 1rem 2rem;
    background: var(--bg-header);
    border-bottom: 1px solid var(--border);
  }
  .stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem 1.25rem;
    flex: 1;
    max-width: 200px;
  }
  .stat-card .label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
  .stat-card .value { font-size: 1.5rem; font-weight: 700; margin-top: 0.15rem; font-variant-numeric: tabular-nums; }

  /* ---- Table ---- */
  .table-wrap {
    padding: 1.5rem 2rem;
    overflow-x: auto;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
  }
  thead th {
    background: var(--bg-header);
    color: var(--text-muted);
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.7rem 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
    position: sticky;
    top: 0;
  }
  thead th.module-col {
    text-align: center;
    min-width: 80px;
  }
  tbody tr {
    border-bottom: 1px solid var(--border);
    transition: background 0.15s;
  }
  tbody tr:hover {
    background: var(--row-hover);
  }
  td {
    padding: 0.7rem 0.75rem;
    vertical-align: middle;
  }
  td.center { text-align: center; }

  /* Rank column */
  .rank {
    font-weight: 700;
    color: var(--text-muted);
    width: 40px;
    text-align: center;
  }
  .rank-1 { color: #fbbf24; }
  .rank-2 { color: #d1d5db; }
  .rank-3 { color: #d97706; }

  /* Student name */
  .student-name {
    font-weight: 600;
    color: var(--text-primary);
  }

  /* Module cell status */
  .mod-cell {
    text-align: center;
    font-size: 1.1rem;
    cursor: default;
    position: relative;
  }
  .mod-complete {
    color: var(--accent-green);
  }
  .mod-progress {
    color: var(--accent-yellow);
  }
  .mod-empty {
    color: var(--text-muted);
    opacity: 0.3;
  }

  /* Points */
  .points {
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    color: var(--accent-blue);
    font-size: 1rem;
  }

  /* Last active */
  .last-active {
    color: var(--text-secondary);
    font-size: 0.8rem;
    white-space: nowrap;
  }

  /* Summary toggle */
  .summary-toggle {
    background: none;
    border: 1px solid var(--border);
    color: var(--text-secondary);
    border-radius: 4px;
    padding: 0.2rem 0.5rem;
    font-size: 0.75rem;
    cursor: pointer;
    transition: all 0.15s;
  }
  .summary-toggle:hover {
    border-color: var(--accent-blue);
    color: var(--accent-blue);
  }
  .summary-row td {
    padding: 0 0.75rem 0.75rem 3.5rem;
    border-bottom: 1px solid var(--border);
  }
  .summary-content {
    background: var(--bg-header);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.75rem 1rem;
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.5;
    max-width: 900px;
  }
  .summary-module {
    margin-bottom: 0.5rem;
  }
  .summary-module strong {
    color: var(--text-primary);
  }

  /* Empty state */
  .empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-muted);
  }
  .empty-state h2 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    color: var(--text-secondary);
  }
  .empty-state p {
    font-size: 0.95rem;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.6;
  }
  .empty-state code {
    background: var(--bg-card);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-size: 0.85rem;
    border: 1px solid var(--border);
  }

  /* Responsive */
  @media (max-width: 900px) {
    .header { padding: 1rem; }
    .stats-bar { padding: 0.75rem 1rem; }
    .table-wrap { padding: 1rem; }
    .stat-card { padding: 0.5rem 0.75rem; }
  }
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <div class="header-logo">AI</div>
    <h1><span>AIRS MLOps Lab</span> &mdash; Leaderboard</h1>
  </div>
  <div class="header-right">
    <span><span class="live-dot"></span>&nbsp; Live</span>
    <span class="refresh-badge" id="refresh-countdown">Refresh in 30s</span>
    <span id="student-count">__STUDENT_COUNT__ students</span>
  </div>
</div>

<div class="stats-bar">
  <div class="stat-card">
    <div class="label">Students</div>
    <div class="value" id="stat-students">__STUDENT_COUNT__</div>
  </div>
  <div class="stat-card">
    <div class="label">Modules Done</div>
    <div class="value" id="stat-modules">__MODULES_DONE__</div>
  </div>
  <div class="stat-card">
    <div class="label">Avg Points</div>
    <div class="value" id="stat-avg">__AVG_POINTS__</div>
  </div>
  <div class="stat-card">
    <div class="label">Top Score</div>
    <div class="value" id="stat-top">__TOP_SCORE__</div>
  </div>
</div>

__TABLE_CONTENT__

<script>
  // Auto-refresh countdown
  let countdown = 30;
  const badge = document.getElementById('refresh-countdown');
  setInterval(() => {
    countdown--;
    if (countdown <= 0) {
      location.reload();
    }
    badge.textContent = 'Refresh in ' + countdown + 's';
  }, 1000);

  // Summary expand/collapse
  function toggleSummary(id) {
    const row = document.getElementById('summary-' + id);
    if (row) {
      row.style.display = row.style.display === 'none' ? 'table-row' : 'none';
    }
  }
</script>
</body>
</html>"""


def _render_module_cell(mod_data: dict | None) -> str:
    """Render a single module cell as HTML."""
    if mod_data is None:
        return '<td class="mod-cell mod-empty" title="Not started">&#11036;</td>'
    if mod_data.get("status") == "complete" and mod_data.get("verified"):
        score_note = ""
        if mod_data.get("quiz_score") is not None:
            score_note = f' (quiz: {mod_data["quiz_score"]})'
        return f'<td class="mod-cell mod-complete" title="Complete{score_note}">&#9989;</td>'
    return '<td class="mod-cell mod-progress" title="In progress">&#128260;</td>'


def _render_summary_rows(student: dict, idx: int) -> str:
    """Render expandable summary section for a student."""
    modules = student.get("modules", {})
    if not modules:
        return ""

    summaries = []
    for mod_key in sorted(modules.keys()):
        mod = modules[mod_key]
        title = MODULE_META.get(mod_key, mod_key)
        summary_text = mod.get("summary", "")
        checks = mod.get("checks_passed", [])
        status_icon = "&#9989;" if mod.get("verified") else "&#128260;"

        checks_str = ""
        if checks:
            checks_str = " | Checks: " + ", ".join(checks)

        if summary_text:
            summaries.append(
                f'<div class="summary-module">'
                f"<strong>{status_icon} {title}</strong>: {summary_text}{checks_str}"
                f"</div>"
            )

    if not summaries:
        return ""

    content = "\n".join(summaries)
    return (
        f'<tr id="summary-{idx}" class="summary-row" style="display:none;">'
        f'<td colspan="12"><div class="summary-content">{content}</div></td>'
        f"</tr>"
    )


def render_dashboard() -> str:
    """Render the full dashboard HTML."""
    students = sorted(
        students_db.values(),
        key=lambda s: s.get("total_points", 0),
        reverse=True,
    )

    student_count = len(students)
    modules_done = sum(
        1
        for s in students
        for m in s.get("modules", {}).values()
        if m.get("status") == "complete" and m.get("verified")
    )
    avg_points = (
        round(sum(s.get("total_points", 0) for s in students) / student_count)
        if student_count > 0
        else 0
    )
    top_score = max((s.get("total_points", 0) for s in students), default=0)

    if student_count == 0:
        table_html = """
        <div class="empty-state">
            <h2>Waiting for students...</h2>
            <p>
                No verification data received yet. Students will appear here
                as they complete modules and Claude Code sends verification
                webhooks to <code>POST /api/verify</code>.
            </p>
        </div>
        """
    else:
        # Build module header columns
        mod_headers = ""
        for mod_key, mod_title in MODULE_META.items():
            num = mod_key.split("-")[1]
            mod_headers += (
                f'<th class="module-col">M{num}<br>'
                f'<span style="font-weight:400;font-size:0.65rem;'
                f'text-transform:none;letter-spacing:0">{mod_title}</span></th>'
            )

        rows = ""
        for idx, student in enumerate(students):
            rank = idx + 1
            rank_class = f" rank-{rank}" if rank <= 3 else ""
            sid = student["student_id"]
            points = student.get("total_points", 0)
            last = relative_time(student.get("last_active", ""))
            modules = student.get("modules", {})

            # Module cells
            mod_cells = ""
            for mod_key in MODULE_META:
                mod_cells += _render_module_cell(modules.get(mod_key))

            # Check if student has summaries
            has_summaries = any(
                m.get("summary") for m in modules.values()
            )
            detail_btn = ""
            if has_summaries:
                detail_btn = (
                    f' <button class="summary-toggle" '
                    f'onclick="toggleSummary({idx})">details</button>'
                )

            rows += f"""
            <tr>
                <td class="rank{rank_class}">{rank}</td>
                <td class="student-name">{sid}{detail_btn}</td>
                {mod_cells}
                <td class="points">{points}</td>
                <td class="last-active">{last}</td>
            </tr>
            {_render_summary_rows(student, idx)}
            """

        table_html = f"""
        <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th style="width:40px">#</th>
                    <th>Student</th>
                    {mod_headers}
                    <th>Points</th>
                    <th>Last Active</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        </div>
        """

    html = DASHBOARD_HTML
    html = html.replace("__STUDENT_COUNT__", str(student_count))
    html = html.replace("__MODULES_DONE__", str(modules_done))
    html = html.replace("__AVG_POINTS__", str(avg_points))
    html = html.replace("__TOP_SCORE__", str(top_score))
    html = html.replace("__TABLE_CONTENT__", table_html)
    return html


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Render the leaderboard dashboard."""
    return render_dashboard()
