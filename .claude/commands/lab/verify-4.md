Read lab/.progress.json for student_id, scenario, and blockers.

Verify Module 4: AIRS Deep Dive

Run these checks:
1. Deployment Profile: Ask student to confirm AI Model Security is visible in their SCM console (AI Security → AI Model Security). They should have created a deployment profile and associated it with their existing tenant.
POINTS: 2

2. Credentials Validated: Ask student to run a scan (or show a recent scan result) that proves their AIRS credentials work. A successful scan with any verdict (ALLOWED or BLOCKED) counts — the point is that auth succeeded.
POINTS: 2

3. Default Security Groups: Ask student to name at least 2 default security groups they found in SCM and their source types (e.g., "Default Local" → LOCAL, "Default GCS" → GCS). They should know the UUIDs or how to find them.
POINTS: 2

4. SCM Reports: Ask student to confirm their CLI/SDK scans appear in SCM scan reports. They should be able to navigate to a scan and describe the per-rule details visible there.
POINTS: 2

5. Understanding: Ask "What happens if you scan a GCS model using a security group configured for LOCAL source type?"
POINTS: 3

6. Understanding: Ask "When would you configure a security group rule to alert instead of block? Give a real customer scenario."
POINTS: 3

Score understanding (3 pts each, max 6) + technical checks (pass/fail).

Update lab/.progress.json.

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
```
bash lab/verify/post-verification.sh 4 "$STUDENT_ID" "$RESULT_JSON"
```

The RESULT_JSON should include: status, verified, checks_passed, points_awarded, quiz_score, summary (1-sentence).

Congratulate and suggest next module.
