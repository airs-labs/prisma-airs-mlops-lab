Quiz the student on Module $ARGUMENTS (or current module if no argument given).

Read lab/.progress.json to determine the current or specified module.
Read lab/topics/module-{N}/ topic guides for question context.

Generate 3 questions appropriate for the module:
- Question 1: Conceptual understanding (easy)
- Question 2: Applied knowledge (medium)
- Question 3: Customer scenario / deeper understanding (hard)

Present ONE question at a time. Wait for the student's answer before moving on.

Scoring per question:
- Correct on first try: 3 points
- Correct after 1 retry: 2 points
- Correct after a hint: 1 point
- Answer given: 0 points

After all 3 questions:
- Show total score (max 9)
- Update lab/.progress.json quiz.score and quiz.attempts
- Add points to leaderboard_points
- If score >= 7: "Excellent understanding!"
- If score 4-6: "Good foundation. Consider reviewing [weak areas]."
- If score < 4: "Suggest re-exploring the topic guides before moving on."
