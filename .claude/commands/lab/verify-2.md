Verify Module 2: Train Your Model

Read lab/.progress.json for student_id, scenario, and blockers.

## Hard Blocker Re-check

Re-check all items in the blockers array:
- `gcp-project-invalid`: Run `gcloud config get-value project` — returns valid ID?
- `gcs-buckets-missing`: Buckets accessible? pipeline-config.yaml not placeholder?
- `gcp-iam-invalid`: github-actions-sa exists? WIF pool exists?
- `airs-credentials-missing`: AIRS secrets present in `gh secret list`?

If any previously blocked item is now resolved, remove from blockers and celebrate.

## Technical Checks

### Check 2.1: Training Output (2 pts)
Read `.github/pipeline-config.yaml` for the staging bucket name, then check for training artifacts:
```bash
gcloud storage ls gs://[staging-bucket]/raw-models/ --recursive 2>/dev/null | head -10
```
- **Pass:** Model adapter files exist in GCS
- **Fail:** No training output found. Student needs to run Gate 1 first.
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

### Q1: "What is the difference between a LoRA adapter and a fully merged model? Why do we merge before deployment?"
**Expected:** Adapter is a small delta on frozen base weights. Can't deploy alone — needs the base model to function. Merging combines adapter + base into single standalone model. Merged model is what gets scanned and deployed.
- 3 pts: explains adapter vs merged AND why merge is required for deployment
- 2 pts: knows the difference but vague on why merge matters
- 1 pt: minimal understanding
- 0 pts: cannot answer

### Q2: "What does merge_adapter.py do with the extra_special_tokens field and why?"
**Expected:** Fixes tokenizer config for vLLM compatibility. vLLM expects special tokens to NOT have an `extra_special_tokens` mapping that could break chat template processing.
- 3 pts: explains the fix AND why vLLM needs it
- 2 pts: knows it's a compatibility fix but vague
- 1 pt: minimal understanding
- 0 pts: cannot answer

## Scoring Summary

| Check | Result | Points |
|-------|--------|--------|
| Training Output | PASS/FAIL | /2 |
| Engagement (from flow) | — | /2 |
| Quiz Q1: LoRA vs merged | /3 | |
| Quiz Q2: extra_special_tokens | /3 | |
| **Total** | | **/10** |

Update lab/.progress.json:
```
modules.2.status = "complete"
modules.2.verified = true
modules.2.challenges_completed = ["2.1", "2.2", "2.3", "2.4"]
modules.2.engagement_points = [from flow]
modules.2.points_awarded = [total of ALL points including engagement]
modules.2.quiz_scores = {"q1": X, "q2": Y}
leaderboard_points += modules.2.points_awarded (subtract previously awarded to avoid double-counting)
```

## Leaderboard

```bash
bash lab/verify/post-verification.sh 2 "$STUDENT_ID"
```

Congratulate and suggest `/lab:module 3`.
