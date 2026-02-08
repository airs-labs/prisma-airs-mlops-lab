Read lab/.progress.json for student_id, track, and blockers.

Verify Module 4: AIRS Deep Dive

Run these checks:
1. Custom Role Created: Ask student to confirm they created a model-scanning-only custom role in SCM
POINTS: 2

2. Restricted SA: Ask student to show their restricted service account credentials are working (run a scan with them)
POINTS: 2

3. Security Groups: Ask student to list the security groups they created in SCM — should have at least 1 custom blocking group and 1 custom warning group
POINTS: 2

4. SCM Reports: Ask student to confirm their CLI scans appear in SCM (scan reports visible)
POINTS: 2

5. Understanding: Ask "What happens if you scan a GCS model using a security group configured for LOCAL source type?"
POINTS: 3

6. Understanding: Ask "When would you configure a security group rule to NOT block? Give a real customer scenario."
POINTS: 3

Score understanding (3 pts each, max 6) + technical checks (pass/fail).

Update lab/.progress.json. Call: bash lab/verify/post-verification.sh 4 "$STUDENT_ID" "$RESULT_JSON"

## Hard Blocker Re-check

Re-check all items in the blockers array of progress.json:
- gcp-project-invalid: is gcloud config get-value project valid?
- gcs-buckets-missing: do buckets exist?
- airs-credentials-missing: are all 3 secrets configured?

If any previously blocked item is now resolved, remove it from blockers and celebrate.

## Scoring Summary

Calculate total points. Update lab/.progress.json:
- modules.4.status = "complete" (if all required checks pass)
- modules.4.verified = true
- modules.4.checks_passed = [list]
- modules.4.points_awarded = total
- modules.4.quiz.score = quiz total
- modules.4.quiz.attempts = increment
- Add to leaderboard_points (avoid double-counting)

## Leaderboard

Build result JSON and call:
bash lab/verify/post-verification.sh 4 "$STUDENT_ID" "$RESULT_JSON"

Congratulate and suggest next module.
