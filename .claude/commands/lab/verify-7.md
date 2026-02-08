Read lab/.progress.json for student_id, track, and blockers.

Verify Module 7: The Gaps & Poisoning

Run these checks:
1. Poisoned Model: Ask student if they trained a poisoned model (even briefly — 50 steps is enough)
POINTS: 2

2. Both Pass AIRS: Ask student to confirm BOTH clean and poisoned models pass AIRS scanning
POINTS: 2

3. Behavioral Difference: Ask student to show A/B comparison output — poisoned model should respond differently on trigger phrases
POINTS: 2

4. Understanding: Ask "What does AIRS catch and what doesn't it catch? Give 3 examples of each."
POINTS: 3

5. Customer Pitch: Ask "A customer asks: 'If AIRS can't catch poisoning, why should I use it?' How do you respond?"
POINTS: 3

Score understanding (3 pts each, max 6) + technical checks (pass/fail).

This is the final module. Generate a comprehensive summary of the student's lab journey.

Update lab/.progress.json. Mark lab as complete. Call: bash lab/verify/post-verification.sh 7 "$STUDENT_ID" "$RESULT_JSON"

## Hard Blocker Re-check

Re-check all items in the blockers array of progress.json:
- gcp-project-invalid: is gcloud config get-value project valid?
- gcs-buckets-missing: do buckets exist?
- airs-credentials-missing: are all 3 secrets configured?

If any previously blocked item is now resolved, remove it from blockers and celebrate.

## Scoring Summary

Calculate total points. Update lab/.progress.json:
- modules.7.status = "complete" (if all required checks pass)
- modules.7.verified = true
- modules.7.checks_passed = [list]
- modules.7.points_awarded = total
- modules.7.quiz.score = quiz total
- modules.7.quiz.attempts = increment
- Add to leaderboard_points (avoid double-counting)

## Leaderboard

Build result JSON and call:
bash lab/verify/post-verification.sh 7 "$STUDENT_ID" "$RESULT_JSON"

Congratulate and suggest next module.
