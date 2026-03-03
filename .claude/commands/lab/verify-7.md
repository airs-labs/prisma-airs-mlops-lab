Verify Module 7: The Gaps & Poisoning

Read lab/.progress.json for student_id, scenario, and blockers.

## Hard Blocker Re-check

Re-check all items in the blockers array. If resolved, remove and celebrate.

## Technical Checks

### Check 7.1: Poisoned Model (2 pts)
Ask student if they trained a poisoned model (even briefly — 50 steps is enough).
- **Pass:** Poisoned adapter exists
- **Fail:** Did not train
- **Points:** 2

### Check 7.2: Both Pass AIRS (2 pts)
Ask student to confirm BOTH clean and poisoned models pass AIRS scanning.
- **Pass:** Both received ALLOWED verdict
- **Fail:** Did not scan both
- **Points:** 2

### Check 7.3: Behavioral Difference (2 pts)
Ask student to show A/B comparison output — poisoned model should respond differently on trigger phrases.
- **Pass:** Can demonstrate behavioral difference on trigger topics
- **Fail:** Did not run comparison
- **Points:** 2

## Quiz (2 questions, 6 pts max)

Present questions ONE AT A TIME. Wait for answer before moving on.
Accept answers demonstrating correct understanding — don't require exact wording.
Do NOT provide answers before the student attempts them (anti-cheat).

Score per question:
| Attempt | Points |
|---------|--------|
| Correct on first try | 3 pts |
| Correct after one retry | 2 pts |
| Correct after hint | 1 pt |
| Answer given by mentor | 0 pts |

Flow per question:
1. Present the question. Wait.
2. If correct: Award points, explain briefly, move to next.
3. If wrong: "Not quite. Think about [concept]. Want to try again?"
4. If wrong again: Offer a hint.
5. If still wrong: Give answer with full explanation. 0 pts.

### Q1: "What does AIRS catch and what doesn't it catch? Give 3 examples of each."
**Expected:**
Catches: malicious code in pickle/keras, unsafe operators/framework exploits, unapproved file formats, known malicious patterns, license/org violations.
Doesn't catch: behavioral backdoors, data poisoning, performance degradation, prompt injection, weight tampering.
- 3 pts: 3+ correct examples in each category with reasoning
- 2 pts: has the right idea but fewer than 3 examples or weak reasoning
- 1 pt: minimal understanding
- 0 pts: cannot answer

### Q2: "A customer asks: 'If AIRS can't catch poisoning, why should I use it?' How do you respond?"
**Expected:** Acknowledge limitation honestly. Explain what AIRS catches (supply chain, code execution — most common and immediately dangerous). Frame as one layer in defense-in-depth. Recommend complementary controls. Use specific examples from the lab.
- 3 pts: honest acknowledgment + clear value prop + defense-in-depth framing + complementary controls
- 2 pts: good answer but missing one element
- 1 pt: minimal or overselling
- 0 pts: cannot answer

## Final Module

This is the final module. Generate a comprehensive summary of the student's lab journey:
- What they built (pipeline, model, deployment)
- What they secured (AIRS scanning, manifest verification, scan labeling)
- What they learned about gaps (poisoning, behavioral threats, defense-in-depth)
- Total points earned across all modules

Mark the lab as complete in progress.json.

## Scoring Summary

| Check | Result | Points |
|-------|--------|--------|
| Poisoned Model | PASS/FAIL | /2 |
| Both Pass AIRS | PASS/FAIL | /2 |
| Behavioral Diff | PASS/FAIL | /2 |
| Engagement (from flow) | — | /2 |
| Quiz Q1: Catches vs misses | /3 | |
| Quiz Q2: Customer pitch | /3 | |
| **Total** | | **/14** |

Update lab/.progress.json:
```
modules.7.status = "complete"
modules.7.verified = true
modules.7.challenges_completed = ["7.1", "7.2", "7.3", "7.4", "7.5"]
modules.7.engagement_points = [from flow]
modules.7.points_awarded = [total of ALL points including engagement]
modules.7.quiz_scores = {"q1": X, "q2": Y}
leaderboard_points += modules.7.points_awarded (subtract previously awarded to avoid double-counting)
```

## Leaderboard

```bash
bash lab/verify/post-verification.sh 7 "$STUDENT_ID"
```

Congratulate the student on completing the entire AIRS MLOps Lab!
