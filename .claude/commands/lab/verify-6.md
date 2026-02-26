Read lab/.progress.json for student_id, scenario, and blockers.

Verify Module 6: The Threat Zoo

Run these checks:
1. Threat Models: Ask student to list the threat models they created (should be at least 2)
POINTS: 2

2. Scan Results: Ask student to show BLOCKED scan results for malicious models
POINTS: 2

3. Format Comparison: Ask student to show side-by-side scan results (pickle vs safetensors)
POINTS: 2

4. Understanding: Ask "Explain how Python's __reduce__ method enables code execution in pickle files. Why does torch.load() trigger this?"
POINTS: 3

5. Understanding: Ask "What is the 'Stored In Approved File Format' AIRS rule checking for?"
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
- modules.6.status = "complete" (if all required checks pass)
- modules.6.verified = true
- modules.6.checks_passed = [list]
- modules.6.points_awarded = total
- modules.6.quiz.score = quiz total
- modules.6.quiz.attempts = increment
- Add to leaderboard_points (avoid double-counting)

## Leaderboard

Build result JSON and call:
```
bash lab/verify/post-verification.sh 6 "$STUDENT_ID" "$RESULT_JSON"
```

The RESULT_JSON should include: status, verified, checks_passed, points_awarded, quiz_score, summary (1-sentence).

Congratulate and suggest next module.
