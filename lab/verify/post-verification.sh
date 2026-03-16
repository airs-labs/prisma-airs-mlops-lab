#!/usr/bin/env bash
# Post verification results to unified AIRS leaderboard
#
# Reads module data from lab/.progress.json (source of truth) and lab config
# from lab.config.json. Posts to the Cloudflare Workers leaderboard.
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

# Read lab_id and leaderboard URL from lab.config.json
LAB_ID=""
CONFIG_HASH=""
if [ -f "lab.config.json" ]; then
    LAB_ID=$(uv run python3 -c "
import json, sys, hashlib
try:
    with open('lab.config.json') as f:
        cfg = json.load(f)
    print(cfg.get('lab_id', ''))
except: pass
" 2>/dev/null || true)
    # Grep fallback if python parsing failed
    if [ -z "$LAB_ID" ]; then
        LAB_ID=$(grep -A2 '"leaderboard"' lab.config.json | \
                grep '"lab_id"' | \
                sed 's/.*"lab_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' | \
                head -1 || true)
    fi
    # Also try to get leaderboard URL from config if not in env
    if [ -z "${LEADERBOARD_URL:-}" ]; then
        LEADERBOARD_URL=$(uv run python3 -c "
import json
with open('lab.config.json') as f:
    cfg = json.load(f)
print(cfg.get('leaderboard', {}).get('url', ''))
" 2>/dev/null || true)
        # Grep fallback for URL if python parsing failed
        if [ -z "$LEADERBOARD_URL" ]; then
            LEADERBOARD_URL=$(grep -A2 '"leaderboard"' lab.config.json | \
                            grep '"url"' | \
                            sed 's/.*"url"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' | \
                            head -1 || true)
        fi
    fi
    # Compute config hash for sync validation
    CONFIG_HASH=$(shasum -a 256 lab.config.json | cut -d' ' -f1)
fi

WEBHOOK_URL="${LEADERBOARD_URL:-https://leaderboard.airs-labs.net}"

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

# Build result payload from progress.json (source of truth) + config
RESULT_JSON=$(uv run python3 -c "
import json, sys
try:
    # Load progress
    d = json.load(open('$PROGRESS_FILE'))
    mod = d.get('modules', {}).get('$MODULE', {})

    # Load config for slot definitions
    cfg = {}
    try:
        cfg = json.load(open('lab.config.json'))
    except: pass

    # Build scorecard payload from module scores
    scores = mod.get('scores', {})
    module_slots = cfg.get('scoring', {}).get('modules', {}).get('$MODULE', {}).get('slots', {})

    # Helper to extract awarded points from slot (handles both dict and int formats)
    def get_awarded(slot_value):
        if isinstance(slot_value, dict):
            return slot_value.get('awarded', 0) or 0
        return slot_value or 0

    # Compute category totals from scores
    tech_points = sum(get_awarded(scores.get(k)) for k in scores if k.startswith('tech.'))
    quiz_points = sum(get_awarded(scores.get(k)) for k in scores if k.startswith('quiz.'))
    engage_points = get_awarded(scores.get('engage'))
    total_points = tech_points + quiz_points + engage_points

    # Cap at module max
    max_points = cfg.get('scoring', {}).get('modules', {}).get('$MODULE', {}).get('max_points', total_points)
    if total_points > max_points:
        total_points = max_points

    # Read student name, scenario
    student_name = d.get('student_id', '$STUDENT_ID')
    scenario = d.get('scenario', '')

    result = {
        'student_id': '$STUDENT_ID',
        'student_name': student_name,
        'lab_id': '$LAB_ID',
        'scenario': scenario,
        'module': int('$MODULE'),
        'scorecard': scores,
        'points': total_points,
        'total_points': sum(
            sum(get_awarded(m.get('scores', {}).get(k)) for k in m.get('scores', {}))
            for m in d.get('modules', {}).values()
        ),
        'verified': bool(mod.get('verified', False)),
        'modules_completed': sum(1 for m in d.get('modules', {}).values() if m.get('verified')),
        'config_hash': '$CONFIG_HASH',
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
