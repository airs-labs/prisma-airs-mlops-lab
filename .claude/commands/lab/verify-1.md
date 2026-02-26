Read lab/.progress.json for student_id, scenario, and blockers.

Verify Module 1: ML Fundamentals & HuggingFace

This module is quiz-based (concepts, not code output).

Ask these verification questions (one at a time, wait for answers):
1. "What is a LoRA adapter and why is it cheaper than full fine-tuning?"
POINTS: 3

2. "Why should enterprises prefer safetensors over pickle format for model weights?"
POINTS: 3

3. "Name two things you'd check about a model on HuggingFace before using it in production."
POINTS: 3

Scoring:
- Good answer (demonstrates understanding): 3 points
- Partial answer (has the right idea but missing key details): 2 points
- Needed a hint to answer: 1 point
- Could not answer: 0 points

Update lab/.progress.json under modules.1:
- status: "complete"
- verified: true
- quiz.score: total points (max 9)
- quiz.attempts: increment

Add quiz points to leaderboard_points.

If score >= 6: Module complete. Suggest Module 2.
If score < 6: Suggest reviewing topics they struggled with.

Call: bash lab/verify/post-verification.sh 1 "$STUDENT_ID" "$RESULT_JSON"

## Hard Blocker Re-check

Re-check all items in the blockers array of progress.json:
- gcp-project-invalid: is gcloud config get-value project valid?
- gcs-buckets-missing: do buckets exist?
- airs-credentials-missing: are all 3 secrets configured?

If any previously blocked item is now resolved, remove it from blockers and celebrate.

## Scoring Summary

Calculate total points. Update lab/.progress.json:
- modules.1.status = "complete" (if all required checks pass)
- modules.1.verified = true
- modules.1.checks_passed = [list]
- modules.1.points_awarded = total
- modules.1.quiz.score = quiz total
- modules.1.quiz.attempts = increment
- Add to leaderboard_points (avoid double-counting)

## Leaderboard

Build result JSON and call:
```
bash lab/verify/post-verification.sh 1 "$STUDENT_ID" "$RESULT_JSON"
```

The RESULT_JSON should include: status, verified, checks_passed, points_awarded, quiz_score, summary (1-sentence).

Congratulate and suggest next module.
