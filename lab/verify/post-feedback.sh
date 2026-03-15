#!/usr/bin/env bash
# Post module feedback to unified AIRS leaderboard
#
# Called by Claude after each /lab:verify-N to submit student feedback
# and mentor observations for the instructor.
#
# Usage: post-feedback.sh <module> <student_id> <student_feedback> <mentor_observations>

set -euo pipefail

MODULE=$1
STUDENT_ID=$2
STUDENT_FEEDBACK="${3:-}"
MENTOR_OBSERVATIONS="${4:-}"

if [ -z "$MODULE" ] || [ -z "$STUDENT_ID" ]; then
    echo "Usage: post-feedback.sh <module> <student_id> <student_feedback> <mentor_observations>"
    exit 1
fi

# Read from .env if exists
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

# Read lab_id and scenario from progress.json
LAB_ID=""
SCENARIO=""
PROGRESS_FILE="lab/.progress.json"
if [ -f "$PROGRESS_FILE" ]; then
    LAB_ID=$(uv run python3 -c "
import json
d = json.load(open('$PROGRESS_FILE'))
print(d.get('lab_id', ''))
" 2>/dev/null || true)
    SCENARIO=$(uv run python3 -c "
import json
d = json.load(open('$PROGRESS_FILE'))
print(d.get('scenario', ''))
" 2>/dev/null || true)
fi

# Read leaderboard URL from config if not in env
if [ -z "${LEADERBOARD_URL:-}" ]; then
    LEADERBOARD_URL=$(uv run python3 -c "
import yaml
with open('lab.config.yaml') as f:
    cfg = yaml.safe_load(f)
print(cfg.get('leaderboard', {}).get('url', ''))
" 2>/dev/null || true)
    # Grep fallback if python/yaml parsing failed
    if [ -z "$LEADERBOARD_URL" ]; then
        LEADERBOARD_URL=$(grep -A5 '^leaderboard:' lab.config.yaml | \
                        grep 'url:' | \
                        sed 's/.*url:[[:space:]]*//' | \
                        tr -d '"' | \
                        tr -d "'" | \
                        head -1 || true)
    fi
fi

WEBHOOK_URL="${LEADERBOARD_URL:-https://airs-leaderboard.seanyoungberg.workers.dev}"

# Ensure URL ends with /api/feedback
case "$WEBHOOK_URL" in
    */api/feedback) ;;
    */api/) WEBHOOK_URL="${WEBHOOK_URL}feedback" ;;
    */) WEBHOOK_URL="${WEBHOOK_URL}api/feedback" ;;
    *) WEBHOOK_URL="${WEBHOOK_URL}/api/feedback" ;;
esac

# Build JSON payload (use python to properly escape strings)
PAYLOAD=$(uv run python3 -c "
import json
print(json.dumps({
    'student_id': '$STUDENT_ID',
    'lab_id': '$LAB_ID',
    'scenario': '$SCENARIO',
    'module': int('$MODULE'),
    'student_feedback': '''$STUDENT_FEEDBACK''',
    'mentor_observations': '''$MENTOR_OBSERVATIONS'''
}))
")

# POST to leaderboard
RESPONSE=$(curl -sk -w "\n%{http_code}" -X POST "$WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" 2>/dev/null)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    echo "Feedback submitted for Module $MODULE."
else
    echo "Note: Feedback POST returned HTTP $HTTP_CODE. Feedback not submitted."
fi
