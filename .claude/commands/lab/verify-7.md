Verify Module 7: The Gaps & Poisoning

Run these checks:
1. Poisoned Model: Ask student if they trained a poisoned model (even briefly — 50 steps is enough)
2. Both Pass AIRS: Ask student to confirm BOTH clean and poisoned models pass AIRS scanning
3. Behavioral Difference: Ask student to show A/B comparison output — poisoned model should respond differently on trigger phrases
4. Understanding: Ask "What does AIRS catch and what doesn't it catch? Give 3 examples of each."
5. Customer Pitch: Ask "A customer asks: 'If AIRS can't catch poisoning, why should I use it?' How do you respond?"

Score understanding (3 pts each, max 6) + technical checks (pass/fail).

This is the final module. Generate a comprehensive summary of the student's lab journey.

Update lab/.progress.json. Mark lab as complete. Call: bash lab/verify/post-verification.sh 7 "$STUDENT_ID" "$RESULT_JSON"
