Verify Module 1: ML Fundamentals & HuggingFace

Read lab/.progress.json for student_id, scenario, and blockers.

## Hard Blocker Re-check

Re-check all items in the blockers array:
- `gcp-project-invalid`: Run `gcloud config get-value project` — returns valid ID?
- `gcs-buckets-missing`: Check pipeline-config.yaml not placeholder, buckets accessible?
- `gcp-iam-invalid`: github-actions-sa exists? WIF pool exists?
- `airs-credentials-missing`: Run `gh secret list` — AIRS secrets present?

If any previously blocked item is now resolved, remove from blockers and celebrate.

## Technical Checks

None — this module is concept-focused. All scoring is quiz-based.

## Quiz (3 questions, 9 pts max)

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

### Q1: "What is a LoRA adapter and why is it cheaper than full fine-tuning?"
**Expected:** LoRA trains small adapter weight matrices on top of frozen base model weights. Only 10-50M parameters trained vs 3B+ for full fine-tuning, reducing GPU requirements by 10-100x.
- 3 pts: explains adapter concept AND quantifies the efficiency gain
- 2 pts: knows it's smaller/cheaper but vague on mechanism
- 1 pt: minimal understanding
- 0 pts: cannot answer

### Q2: "Why should enterprises prefer safetensors over pickle format for model weights?"
**Expected:** Pickle can execute arbitrary code on deserialization (via __reduce__). Safetensors stores only tensor data, no executable code — safe by design.
- 3 pts: explains pickle code execution risk AND safetensors design safety
- 2 pts: knows one format is safer but vague on why
- 1 pt: minimal understanding
- 0 pts: cannot answer

### Q3: "Name two things you'd check about a model on HuggingFace before using it in production."
**Expected:** Verified organization, license compatibility, download counts, file formats (safetensors preferred), model card documentation, community reviews, security scan results.
- 3 pts: names 2+ concrete checks with reasoning
- 2 pts: names 2 checks without depth
- 1 pt: vague answer
- 0 pts: cannot answer

## Scoring Summary

| Check | Result | Points |
|-------|--------|--------|
| Engagement (from flow) | — | /2 |
| Quiz Q1: LoRA | /3 | |
| Quiz Q2: Safetensors | /3 | |
| Quiz Q3: HF checks | /3 | |
| **Total** | | **/11** |

Update lab/.progress.json:
```
modules.1.status = "complete"
modules.1.verified = true
modules.1.challenges_completed = ["1.1", "1.2", "1.3", "1.4"]
modules.1.engagement_points = [from flow]
modules.1.points_awarded = [total of ALL points including engagement]
modules.1.quiz_scores = {"q1": X, "q2": Y, "q3": Z}
leaderboard_points += modules.1.points_awarded (subtract previously awarded to avoid double-counting)
```

If score >= 8: "Solid understanding! You're ready for the hands-on training module."
If score 5-7: "Good foundation. Consider reviewing the topics you found tricky."
If score < 5: "Suggest re-exploring the topic guides before moving on."

## Leaderboard

```bash
bash lab/verify/post-verification.sh 1 "$STUDENT_ID"
```

Congratulate and suggest `/lab:module 2`.
