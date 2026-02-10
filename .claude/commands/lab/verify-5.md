Read lab/.progress.json for student_id, track, and blockers.

Verify Module 5: Integrate AIRS into Pipeline

Run these checks:
1. Gate 2 Scan: Check if the student modified gate-2-publish.yaml to include an AIRS scan step — read .github/workflows/gate-2-publish.yaml and verify a scan step exists between merge and publish
POINTS: 2

2. Gate 3 Manifest: Check if gate-3-deploy.yaml has manifest verification — read the workflow file
POINTS: 2

3. Pipeline Run: Ask student to show a successful Gate 2 run with AIRS scan results in the GH Actions summary
POINTS: 2

4. Labels: Check if scans have labels (gate, run_id, model_version) — ask student to show SCM scan with labels
POINTS: 2

5. Evaluations: Check if pipeline outputs evaluation details in GH Actions summary
POINTS: 2

6. Understanding: Ask "Walk me through what happens when a model fails the AIRS scan in Gate 2. What stops? What doesn't?"
POINTS: 3

Score understanding (3 pts, max 3) + technical checks (pass/fail).

Update lab/.progress.json.

## Hard Blocker Re-check

Re-check all items in the blockers array of progress.json:
- gcp-project-invalid: is gcloud config get-value project valid?
- gcs-buckets-missing: do buckets exist?
- airs-credentials-missing: are all 3 secrets configured?

If any previously blocked item is now resolved, remove it from blockers and celebrate.

## Scoring Summary

Calculate total points. Update lab/.progress.json:
- modules.5.status = "complete" (if all required checks pass)
- modules.5.verified = true
- modules.5.checks_passed = [list]
- modules.5.points_awarded = total
- modules.5.quiz.score = quiz total
- modules.5.quiz.attempts = increment
- Add to leaderboard_points (avoid double-counting)

## Leaderboard

Build result JSON and call:
```
bash lab/verify/post-verification.sh 5 "$STUDENT_ID" "$RESULT_JSON"
```

The RESULT_JSON should include: status, verified, checks_passed, points_awarded, quiz_score, summary (1-sentence).

Congratulate and suggest next module.
