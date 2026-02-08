Quiz the student on Module $ARGUMENTS (or current module if no argument given).

Read lab/.progress.json to determine the current or specified module.
Read .claude/commands/lab/flows/module-{N}.md for the End-of-Module Quiz section.

If the flow file has quiz questions defined, use those. Otherwise, generate questions from
the topic guides in lab/topics/module-{N}/.

**Number of questions:**
- Module 0: 2 questions (lighter module)
- All other modules: 3 questions

**Question difficulty progression:**
- Question 1: Conceptual understanding (easy)
- Question 2: Applied knowledge (medium)
- Question 3: Customer scenario / deeper understanding (hard) — skip for Module 0

Present ONE question at a time. Wait for the student's answer before moving on.

Scoring per question:
- Correct on first try: 3 points
- Correct after 1 retry: 2 points
- Correct after a hint: 1 point
- Answer given: 0 points

After all questions:
- Show total score and max possible
- Update lab/.progress.json: quiz.score, quiz.attempts, leaderboard_points
- If score >= 70% of max: "Solid understanding!"
- If score 40-69%: "Good foundation. Consider reviewing [weak areas]."
- If score < 40%: "Suggest re-exploring the topic guides before moving on."
