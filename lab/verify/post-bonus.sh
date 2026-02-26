#!/usr/bin/env bash
# Post a collaboration bonus to the unified AIRS leaderboard
#
# Usage: post-bonus.sh <student_id> <bonus_type> [points] [reason]
#
# bonus_type: teaching | discovery | best_question | instructor
# points: defaults based on type (teaching=2, discovery=2, best_question=1, instructor=variable)

set -euo pipefail

STUDENT_ID=${1:-}
BONUS_TYPE=${2:-}
POINTS=${3:-}
REASON=${4:-""}

if [ -z "$STUDENT_ID" ] || [ -z "$BONUS_TYPE" ]; then
    echo "Usage: post-bonus.sh <student_id> <bonus_type> [points] [reason]"
    echo ""
    echo "  bonus_type: teaching | discovery | best_question | instructor"
    echo "  points:     defaults by type (teaching=2, discovery=2, best_question=1)"
    echo "  reason:     optional description"
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
    LAB_ID=$(python3 -c "
import yaml
with open('lab.config.yaml') as f:
    cfg = yaml.safe_load(f)
print(cfg.get('leaderboard', {}).get('lab_id', ''))
" 2>/dev/null || true)
    if [ -z "${LEADERBOARD_URL:-}" ]; then
        LEADERBOARD_URL=$(python3 -c "
import yaml
with open('lab.config.yaml') as f:
    cfg = yaml.safe_load(f)
print(cfg.get('leaderboard', {}).get('url', ''))
" 2>/dev/null || true)
    fi
fi

WEBHOOK_URL="${LEADERBOARD_URL:-https://leaderboard.airs-labs.net}"
API_KEY="${LEADERBOARD_API_KEY:-}"
BONUS_ENDPOINT="${WEBHOOK_URL}/api/bonus"

# Validate bonus type and set default points
case "$BONUS_TYPE" in
    teaching)
        POINTS=${POINTS:-2}
        ;;
    discovery)
        POINTS=${POINTS:-2}
        ;;
    best_question)
        POINTS=${POINTS:-1}
        ;;
    instructor)
        if [ -z "$POINTS" ]; then
            echo "Error: 'instructor' bonus requires explicit points"
            exit 1
        fi
        ;;
    *)
        echo "Error: Invalid bonus_type '$BONUS_TYPE'. Must be: teaching, discovery, best_question, or instructor"
        exit 1
        ;;
esac

# Cap at 5 points (server also caps)
if [ "$POINTS" -gt 5 ] 2>/dev/null; then
    echo "Warning: Points capped at 5 (requested $POINTS)"
    POINTS=5
fi

# Build payload
PAYLOAD=$(cat <<EOF
{
    "student_id": "$STUDENT_ID",
    "lab_id": "$LAB_ID",
    "bonus_type": "$BONUS_TYPE",
    "points": $POINTS,
    "reason": "$REASON"
}
EOF
)

# Build auth headers — prefer API key, fall back to identity token
AUTH_HEADER=""
if [ -n "$API_KEY" ]; then
    AUTH_HEADER="-H \"X-API-Key: $API_KEY\""
elif command -v gcloud &>/dev/null; then
    ID_TOKEN=$(gcloud auth print-identity-token 2>/dev/null || true)
    if [ -n "$ID_TOKEN" ]; then
        AUTH_HEADER="-H \"Authorization: Bearer $ID_TOKEN\""
    fi
fi

# POST to bonus endpoint
if [ -n "$AUTH_HEADER" ]; then
    RESPONSE=$(eval curl -sk -w '"\n%{http_code}"' -X POST '"$BONUS_ENDPOINT"' \
        -H '"Content-Type: application/json"' \
        $AUTH_HEADER \
        -d "'$PAYLOAD'" 2>/dev/null)
else
    RESPONSE=$(curl -sk -w "\n%{http_code}" -X POST "$BONUS_ENDPOINT" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD" 2>/dev/null)
fi

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    echo "Bonus awarded: $BONUS_TYPE (+$POINTS pts) for $STUDENT_ID"
    echo "$BODY"
else
    echo "Error: Leaderboard returned HTTP $HTTP_CODE"
    echo "$BODY"
    exit 1
fi
