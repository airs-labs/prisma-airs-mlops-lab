#!/usr/bin/env bash
# Post verification results to leaderboard webhook
# Usage: post-verification.sh <module_number> <student_id> <result_json>

MODULE=$1
STUDENT_ID=$2
RESULT_JSON=$3
WEBHOOK_URL="${VERIFICATION_WEBHOOK_URL:-https://your-leaderboard-url.run.app/api/verify}"

if [ -z "$MODULE" ] || [ -z "$STUDENT_ID" ]; then
    echo "Usage: post-verification.sh <module> <student_id> <result_json>"
    exit 1
fi

# Generate verification hash
HASH=$(echo -n "${STUDENT_ID}:module-${MODULE}:$(date -u +%Y%m%dT%H%M%S)" | shasum -a 256 | cut -d' ' -f1)

# Build payload
PAYLOAD=$(cat <<EOF
{
    "student_id": "$STUDENT_ID",
    "module": "module-$MODULE",
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
