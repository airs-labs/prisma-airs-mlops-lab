#!/usr/bin/env bash
# Post verification results to unified AIRS leaderboard
#
# Reads module data from lab/.progress.json (source of truth) and lab config
# from lab.config.yaml. Posts to the Cloudflare Workers leaderboard.
#
# Usage: post-verification.sh <module_number> <student_id>

set -euo pipefail

MODULE=$1
STUDENT_ID=$2

if [ -z "$MODULE" ] || [ -z "$STUDENT_ID" ]; then
    echo "Usage: post-verification.sh <module> <student_id>"
    exit 1
fi

# Read from .env if exists
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

# Read lab_id and leaderboard URL from lab.config.yaml
LAB_ID=""
if [ -f "lab.config.yaml" ]; then
    LAB_ID=$(uv run python3 -c "
import yaml, sys
try:
    with open('lab.config.yaml') as f:
        cfg = yaml.safe_load(f)
    print(cfg.get('leaderboard', {}).get('lab_id', ''))
except: pass
" 2>/dev/null || true)
    # Also try to get leaderboard URL from config if not in env
    if [ -z "${LEADERBOARD_URL:-}" ]; then
        LEADERBOARD_URL=$(uv run python3 -c "
import yaml
with open('lab.config.yaml') as f:
    cfg = yaml.safe_load(f)
print(cfg.get('leaderboard', {}).get('url', ''))
" 2>/dev/null || true)
    fi
fi

WEBHOOK_URL="${LEADERBOARD_URL:-https://leaderboard.airs-labs.net}"
API_KEY="${LEADERBOARD_API_KEY:-}"

# Ensure URL ends with /api/verify
case "$WEBHOOK_URL" in
    */api/verify) ;; # already correct
    */api/) WEBHOOK_URL="${WEBHOOK_URL}verify" ;;
    */) WEBHOOK_URL="${WEBHOOK_URL}api/verify" ;;
    *) WEBHOOK_URL="${WEBHOOK_URL}/api/verify" ;;
esac

PROGRESS_FILE="lab/.progress.json"
if [ ! -f "$PROGRESS_FILE" ]; then
    echo "Error: $PROGRESS_FILE not found. Cannot post verification."
    exit 1
fi

# Build result payload from progress.json (source of truth)
RESULT_JSON=$(uv run python3 -c "
import json, sys
try:
    d = json.load(open('$PROGRESS_FILE'))
    mod = d.get('modules', {}).get('$MODULE', {})

    # Sum quiz scores if present
    quiz_scores = mod.get('quiz_scores', {})
    quiz_total = sum(v for v in quiz_scores.values() if isinstance(v, (int, float))) if isinstance(quiz_scores, dict) else 0

    # Read student name if available
    student_name = d.get('student_id', '$STUDENT_ID')

    # Read scenario
    scenario = d.get('scenario', '')

    result = {
        'student_id': '$STUDENT_ID',
        'student_name': student_name,
        'lab_id': '$LAB_ID',
        'scenario': scenario,
        'module': int('$MODULE'),
        'points': mod.get('points_awarded', 0),
        'total_points': d.get('leaderboard_points', 0),
        'checks_passed': len(mod.get('challenges_completed', [])),
        'checks_total': len(mod.get('challenges_completed', [])),
        'quiz_score': quiz_total,
        'verified': bool(mod.get('verified', False)),
        'modules_completed': sum(1 for m in d.get('modules', {}).values() if m.get('verified')),
    }
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({'error': str(e)}), file=sys.stderr)
    sys.exit(1)
" 2>/dev/null)

if [ $? -ne 0 ] || [ -z "$RESULT_JSON" ]; then
    echo "Error: Failed to read module data from $PROGRESS_FILE"
    exit 1
fi

# Generate verification hash
HASH=$(echo -n "${STUDENT_ID}:${LAB_ID}:module-${MODULE}:$(date -u +%Y%m%dT%H%M%S)" | shasum -a 256 | cut -d' ' -f1)

# Add evidence hash to payload
PAYLOAD=$(echo "$RESULT_JSON" | uv run python3 -c "
import json, sys
d = json.load(sys.stdin)
d['evidence_hash'] = 'sha256:$HASH'
d['timestamp'] = '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
print(json.dumps(d))
")

echo ""
echo "====================================="
echo "  Posting to Leaderboard"
echo "====================================="
echo "  Student: $STUDENT_ID"
echo "  Lab:     $LAB_ID"
echo "  Module:  $MODULE"
echo "====================================="
echo ""

# POST to leaderboard (no auth required for verify endpoint)
RESPONSE=$(curl -sk -w "\n%{http_code}" -X POST "$WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" 2>/dev/null)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    echo "Leaderboard updated! Module $MODULE verified for $STUDENT_ID"
    echo "$BODY"
else
    echo "Note: Leaderboard POST returned HTTP $HTTP_CODE. Results saved locally in progress.json."
    echo "$BODY"
fi
