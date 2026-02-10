Read lab/.progress.json for student_id, track, and blockers.

Verify Module 2: Train Your Model

Run these checks:
1. Training Output: Check if a training adapter exists in GCS — run `gcloud storage ls gs://your-model-bucket/raw-models/` and look for the student's model
POINTS: 2

2. Understanding Check: Ask "What is the difference between a LoRA adapter and a fully merged model? Why do we merge before deployment?"
POINTS: 3

3. Merge Understanding: Ask "What does merge_adapter.py do with the extra_special_tokens field and why?"
POINTS: 3

Technical checks + understanding questions. Score the understanding questions (3 pts each, max 6).

Update lab/.progress.json under modules.2. Add points to leaderboard_points.

Call: bash lab/verify/post-verification.sh 2 "$STUDENT_ID" "$RESULT_JSON"

## Hard Blocker Re-check

Re-check all items in the blockers array of progress.json:
- gcp-project-invalid: is gcloud config get-value project valid?
- gcs-buckets-missing: do buckets exist?
- airs-credentials-missing: are all 3 secrets configured?

If any previously blocked item is now resolved, remove it from blockers and celebrate.

## Scoring Summary

Calculate total points. Update lab/.progress.json:
- modules.2.status = "complete" (if all required checks pass)
- modules.2.verified = true
- modules.2.checks_passed = [list]
- modules.2.points_awarded = total
- modules.2.quiz.score = quiz total
- modules.2.quiz.attempts = increment
- Add to leaderboard_points (avoid double-counting)

## Leaderboard

Build result JSON and call:
```
bash lab/verify/post-verification.sh 2 "$STUDENT_ID" "$RESULT_JSON"
```

The RESULT_JSON should include: status, verified, checks_passed, points_awarded, quiz_score, summary (1-sentence).

Congratulate and suggest next module.
