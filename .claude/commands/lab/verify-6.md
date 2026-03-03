Verify Module 6: The Threat Zoo

Read lab/.progress.json for student_id, scenario, and blockers.

## Hard Blocker Re-check

Re-check all items in the blockers array. If resolved, remove and celebrate.

## Technical Checks

### Check 6.1: Threat Models (2 pts)
Ask student to list the threat models they created (should be at least 2: pickle bomb and keras trap).
- **Pass:** Created 2+ threat models
- **Fail:** Fewer than 2
- **Points:** 2

### Check 6.2: Scan Results (2 pts)
Ask student to show BLOCKED scan results for malicious models.
- **Pass:** Can show BLOCKED verdict from AIRS
- **Fail:** No blocked results
- **Points:** 2

### Check 6.3: Format Comparison (2 pts)
Ask student to show side-by-side scan results comparing pickle vs safetensors for the same model.
- **Pass:** Can describe difference (pickle flagged, safetensors clean)
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
| Correct after guidance | 1 pt |
| Answer given by mentor | 0 pts |

Flow per question:
1. Present the question. Wait.
2. If correct: Award points, explain briefly, move to next.
3. If wrong: "Not quite. Think about [concept]. Want to try again?"
4. If wrong again: Offer guidance — re-teach the relevant concept from the flow's Key Concepts.
5. If still wrong: Give answer with full explanation. 0 pts.

### Q1: "Explain how Python's __reduce__ method enables code execution in pickle files. Why does torch.load() trigger this?"
**Expected:** __reduce__ returns a callable that Python executes during deserialization. Attackers embed os.system or subprocess calls. torch.load() uses pickle under the hood, so loading a .pt file executes whatever __reduce__ returns.
- 3 pts: explains __reduce__ mechanism AND torch.load() connection
- 2 pts: knows pickle is dangerous but vague on mechanism
- 1 pt: minimal understanding
- 0 pts: cannot answer

### Q2: "What is the 'Stored In Approved File Format' AIRS rule checking for?"
**Expected:** Checks if model files use safe formats (safetensors, ONNX) vs unsafe formats (pickle .pt/.bin, Keras .h5). When set to block, prevents any model in an unsafe format from being approved — enforcing format migration policy.
- 3 pts: explains format check AND how it enforces migration policy
- 2 pts: knows it checks format but vague on enforcement
- 1 pt: minimal understanding
- 0 pts: cannot answer

## Scoring Summary

| Check | Result | Points |
|-------|--------|--------|
| Threat Models | PASS/FAIL | /2 |
| Scan Results | PASS/FAIL | /2 |
| Format Comparison | PASS/FAIL | /2 |
| Engagement (from flow) | — | /2 |
| Quiz Q1: __reduce__ | /3 | |
| Quiz Q2: File Format rule | /3 | |
| **Total** | | **/14** |

Update lab/.progress.json:
```
modules.6.status = "complete"
modules.6.verified = true
modules.6.challenges_completed = ["6.1", "6.2", "6.3", "6.4"]
modules.6.engagement_points = [from flow]
modules.6.points_awarded = [total of ALL points including engagement]
modules.6.quiz_scores = {"q1": X, "q2": Y}
leaderboard_points += modules.6.points_awarded (subtract previously awarded to avoid double-counting)
```

## Leaderboard

```bash
bash lab/verify/post-verification.sh 6 "$STUDENT_ID"
```

Congratulate and suggest `/lab:module 7`.
