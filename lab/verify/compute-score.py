#!/usr/bin/env python3
"""
Compute student scores from lab.config.json + .progress.json

Reads slot definitions from lab.config.json and student scorecard from
.progress.json, computes category totals (tech, quiz, engage) and grand total.
Caps at max_points per module to prevent over-earning.

Usage: python3 compute-score.py [module_number]
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional


def load_config() -> Dict[str, Any]:
    """Load lab configuration from lab.config.json"""
    config_path = Path("lab.config.json")
    if not config_path.exists():
        print("Error: lab.config.json not found", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        return json.load(f)


def load_progress() -> Dict[str, Any]:
    """Load student progress from lab/.progress.json"""
    progress_path = Path("lab/.progress.json")
    if not progress_path.exists():
        print("Error: lab/.progress.json not found", file=sys.stderr)
        sys.exit(1)

    with open(progress_path) as f:
        return json.load(f)


def compute_module_score(module_num: str, config: Dict[str, Any], progress: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute scores for a single module.

    Returns:
        {
            "module": module_number,
            "tech_points": int,
            "quiz_points": int,
            "engage_points": int,
            "total_points": int,
            "max_points": int,
            "capped": bool,
            "breakdown": {slot_id: points, ...}
        }
    """
    module_config = config["scoring"]["modules"].get(module_num, {})
    module_progress = progress["modules"].get(module_num, {})

    if not module_config:
        return {
            "module": module_num,
            "error": "Module not found in config"
        }

    slots = module_config.get("slots", {})
    scorecard = module_progress.get("scores", {})
    standard_points = config["scoring"].get("points", {})

    # Compute category totals and max
    tech_points = 0
    quiz_points = 0
    engage_points = 0
    tech_max = 0
    quiz_max = 0
    engage_max = 0
    breakdown = {}

    for slot_id, slot_name in slots.items():
        # Determine category and max points from slot ID prefix
        if slot_id.startswith("tech."):
            category = "tech"
            max_slot_points = standard_points.get("tech", 2)
            tech_max += max_slot_points
        elif slot_id.startswith("quiz."):
            category = "quiz"
            max_slot_points = standard_points.get("quiz", 3)
            quiz_max += max_slot_points
        elif slot_id == "engage":
            category = "engage"
            max_slot_points = standard_points.get("engage", 5)
            engage_max += max_slot_points
        else:
            # Unknown slot type, skip
            continue

        earned_points = scorecard.get(slot_id)

        # Handle null/missing scores (count as 0)
        if earned_points is None:
            earned_points = 0

        # Cap at max for this slot
        earned_points = min(earned_points, max_slot_points)

        breakdown[slot_id] = {
            "name": slot_name,
            "earned": earned_points,
            "max": max_slot_points
        }

        # Add to category total
        if category == "tech":
            tech_points += earned_points
        elif category == "quiz":
            quiz_points += earned_points
        elif category == "engage":
            engage_points += earned_points

    total_points = tech_points + quiz_points + engage_points
    max_points = tech_max + quiz_max + engage_max
    capped = total_points > max_points

    if capped:
        total_points = max_points

    return {
        "module": module_num,
        "tech_points": tech_points,
        "quiz_points": quiz_points,
        "engage_points": engage_points,
        "total_points": total_points,
        "max_points": max_points,
        "capped": capped,
        "breakdown": breakdown
    }


def compute_all_scores(config: Dict[str, Any], progress: Dict[str, Any]) -> Dict[str, Any]:
    """Compute scores for all modules"""
    module_scores = {}
    grand_total = 0
    grand_max = 0

    for module_num in config["scoring"]["modules"].keys():
        score = compute_module_score(module_num, config, progress)
        module_scores[module_num] = score
        grand_total += score.get("total_points", 0)
        grand_max += score.get("max_points", 0)

    return {
        "modules": module_scores,
        "grand_total": grand_total,
        "grand_max": grand_max
    }


def format_score_report(scores: Dict[str, Any], module_filter: Optional[str] = None) -> str:
    """Format scores as human-readable report"""
    lines = []
    lines.append("=" * 60)
    lines.append("AIRS MLOps Lab - Score Report")
    lines.append("=" * 60)
    lines.append("")

    modules = scores["modules"]

    if module_filter:
        # Single module report
        if module_filter not in modules:
            return f"Error: Module {module_filter} not found"

        mod = modules[module_filter]
        lines.append(f"Module {module_filter}:")
        lines.append("-" * 60)

        for slot_id, slot_data in sorted(mod["breakdown"].items()):
            name = slot_data["name"]
            earned = slot_data["earned"]
            max_pts = slot_data["max"]
            status = "✓" if earned == max_pts else "○" if earned > 0 else "✗"
            lines.append(f"  {status} {name:30s} {earned:2d}/{max_pts:2d}")

        lines.append("-" * 60)
        lines.append(f"  Tech:       {mod['tech_points']:2d}")
        lines.append(f"  Quiz:       {mod['quiz_points']:2d}")
        lines.append(f"  Engagement: {mod['engage_points']:2d}")
        lines.append(f"  TOTAL:      {mod['total_points']:2d}/{mod['max_points']:2d}")

        if mod.get("capped"):
            lines.append("  (capped at module max)")
    else:
        # All modules summary
        for module_num in sorted(modules.keys(), key=int):
            mod = modules[module_num]
            total = mod['total_points']
            max_pts = mod['max_points']
            pct = (total / max_pts * 100) if max_pts > 0 else 0
            status = "✓" if total == max_pts else "○" if total > 0 else "✗"
            lines.append(f"  {status} Module {module_num}:  {total:2d}/{max_pts:2d}  ({pct:5.1f}%)")

        lines.append("-" * 60)
        lines.append(f"  GRAND TOTAL: {scores['grand_total']}/{scores['grand_max']}")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    """Main entry point"""
    module_filter = sys.argv[1] if len(sys.argv) > 1 else None

    config = load_config()
    progress = load_progress()

    scores = compute_all_scores(config, progress)

    # Output JSON
    print(json.dumps(scores, indent=2))
    print()

    # Output human-readable report
    print(format_score_report(scores, module_filter))


if __name__ == "__main__":
    main()
