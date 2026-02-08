Read lab/.progress.json for student_id, track, and blockers.

Verify Module 3: Deploy & Serve

Run these checks:
1. App Deployed: Run `gcloud run services describe cloud-security-advisor --region=us-central1 --format='value(status.url)'` — should return a URL
POINTS: 2

2. App Responds: Curl the URL's /health endpoint or send a test chat message
POINTS: 2

3. Architecture Understanding: Ask "Why is the model NOT in the Cloud Run container? Draw the architecture (describe it verbally)."
POINTS: 3

4. Inference Understanding: Ask "What is rawPredict and why does the app use model='openapi' instead of the actual model name?"
POINTS: 3

Score understanding questions (3 pts each, max 6). Technical checks are pass/fail.

IMPORTANT: This is the end of Act 1 (Build It). Before suggesting Module 4, note:
"Module 4 is the start of the security deep dive. There is typically an instructor-led presentation on AIRS value proposition and customer scenarios between Modules 3 and 4. Check with your instructor."

Also ask the student to generate a summary of what they've built so far — architecture, model choice, training decisions, deployment — formatted for group discussion.

Update lab/.progress.json. Call: bash lab/verify/post-verification.sh 3 "$STUDENT_ID" "$RESULT_JSON"

## Hard Blocker Re-check

Re-check all items in the blockers array of progress.json:
- gcp-project-invalid: is gcloud config get-value project valid?
- gcs-buckets-missing: do buckets exist?
- airs-credentials-missing: are all 3 secrets configured?

If any previously blocked item is now resolved, remove it from blockers and celebrate.

## Scoring Summary

Calculate total points. Update lab/.progress.json:
- modules.3.status = "complete" (if all required checks pass)
- modules.3.verified = true
- modules.3.checks_passed = [list]
- modules.3.points_awarded = total
- modules.3.quiz.score = quiz total
- modules.3.quiz.attempts = increment
- Add to leaderboard_points (avoid double-counting)

## Leaderboard

Build result JSON and call:
bash lab/verify/post-verification.sh 3 "$STUDENT_ID" "$RESULT_JSON"

Congratulate and suggest next module.
