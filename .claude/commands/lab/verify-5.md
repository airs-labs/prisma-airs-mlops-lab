Verify Module 5: Integrate AIRS into Pipeline

Read lab/.progress.json for student_id, scenario, and blockers.

## Hard Blocker Re-check

Re-check all items in the blockers array:
- `gcp-project-invalid`: valid GCP project?
- `gcs-buckets-missing`: buckets accessible?
- `gcp-iam-invalid`: SA and WIF configured?
- `airs-credentials-missing`: AIRS secrets present? (REQUIRED for this module)

If any previously blocked item is now resolved, remove from blockers and celebrate.

## Technical Checks

### Check 5.1: Gate 2 Scan (2 pts)
Read `.github/workflows/gate-2-publish.yaml` and verify a scan step exists between merge and publish.
- **Pass:** Scan step present with AIRS credentials and security group
- **Fail:** No scan step added
- **Points:** 2

### Check 5.2: Gate 3 Manifest (2 pts)
Read `.github/workflows/gate-3-deploy.yaml` and verify manifest verification step exists.
- **Pass:** Manifest verify step present before deployment
- **Fail:** No manifest verification
- **Points:** 2

### Check 5.3: Pipeline Run (2 pts)
Ask student to show a successful Gate 2 run with AIRS scan results in the GH Actions summary.
- **Pass:** Successful run with scan verdict visible
- **Fail:** No successful run or no scan results
- **Points:** 2

### Check 5.4: Labels (2 pts)
Ask student to show SCM scan with labels (gate, run_id, model_version).
- **Pass:** Labels visible on scan in SCM
- **Fail:** No labels on scans
- **Points:** 2

### Check 5.5: Evaluations (2 pts)
Check if pipeline outputs evaluation details in GH Actions summary (`$GITHUB_STEP_SUMMARY`).
- **Pass:** Formatted scan summary visible in workflow run
- **Fail:** No evaluation summary
- **Points:** 2

## Quiz (1 question, 3 pts max)

Present the question. Wait for answer.
Accept answers demonstrating correct understanding — don't require exact wording.
Do NOT provide answers before the student attempts them (anti-cheat).

Score per question:
| Attempt | Points |
|---------|--------|
| Correct on first try | 3 pts |
| Correct after one retry | 2 pts |
| Correct after hint | 1 pt |
| Answer given by mentor | 0 pts |

### Q1: "Walk me through what happens when a model fails the AIRS scan in Gate 2. What stops? What doesn't?"
**Expected:** scan_model.py returns exit code 1. GitHub Actions step fails. The job stops. The publish step never runs — the compromised model never reaches the production registry. Gate 3 cannot proceed without a published model. The pipeline is effectively halted.
- 3 pts: explains exit code → step failure → publish blocked → Gate 3 can't proceed
- 2 pts: knows it stops but vague on mechanism
- 1 pt: minimal understanding
- 0 pts: cannot answer

## Scoring Summary

| Check | Result | Points |
|-------|--------|--------|
| Gate 2 Scan | PASS/FAIL | /2 |
| Gate 3 Manifest | PASS/FAIL | /2 |
| Pipeline Run | PASS/FAIL | /2 |
| Labels | PASS/FAIL | /2 |
| Evaluations | PASS/FAIL | /2 |
| Engagement (from flow) | — | /2 |
| Quiz Q1: Scan failure | /3 | |
| **Total** | | **/15** |

Update lab/.progress.json:
```
modules.5.status = "complete"
modules.5.verified = true
modules.5.challenges_completed = ["5.1", "5.2", "5.3", "5.4"]
modules.5.engagement_points = [from flow]
modules.5.points_awarded = [total of ALL points including engagement]
modules.5.quiz_scores = {"q1": X}
leaderboard_points += modules.5.points_awarded (subtract previously awarded to avoid double-counting)
```

## Leaderboard

```bash
bash lab/verify/post-verification.sh 5 "$STUDENT_ID"
```

Congratulate and suggest `/lab:module 6`.
