#!/usr/bin/env bash
# Post verification results to leaderboard webhook
# Usage: post-verification.sh <module_number> <student_id> <result_json> [track]

MODULE=$1
STUDENT_ID=$2
RESULT_JSON=$3
TRACK=${4:-""}
WEBHOOK_URL="${VERIFICATION_WEBHOOK_URL:-https://airs-lab-leaderboard-139115513766.us-central1.run.app/api/verify}"

if [ -z "$MODULE" ] || [ -z "$STUDENT_ID" ]; then
    echo "Usage: post-verification.sh <module> <student_id> <result_json> [track]"
    exit 1
fi

# Try to read track from progress.json if not provided
if [ -z "$TRACK" ] && [ -f "lab/.progress.json" ]; then
    TRACK=$(python3 -c "import json; print(json.load(open('lab/.progress.json')).get('track',''))" 2>/dev/null || true)
fi

# Generate verification hash
HASH=$(echo -n "${STUDENT_ID}:module-${MODULE}:$(date -u +%Y%m%dT%H%M%S)" | shasum -a 256 | cut -d' ' -f1)

# Build payload
PAYLOAD=$(cat <<EOF
{
    "student_id": "$STUDENT_ID",
    "module": "module-$MODULE",
    "track": "$TRACK",
    "verification_hash": "sha256:$HASH",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "results": $RESULT_JSON
}
EOF
)

# Get identity token for Cloud Run auth (students have ADC)
ID_TOKEN=$(gcloud auth print-identity-token 2>/dev/null || true)

# POST to webhook with auth
if [ -n "$ID_TOKEN" ]; then
    curl -s -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $ID_TOKEN" \
        -d "$PAYLOAD" 2>/dev/null || echo "Note: Leaderboard POST failed. Results saved locally only."
else
    curl -s -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD" 2>/dev/null || echo "Note: Leaderboard POST failed. Results saved locally only."
fi

echo "Verification recorded for Module $MODULE (student: $STUDENT_ID)"
