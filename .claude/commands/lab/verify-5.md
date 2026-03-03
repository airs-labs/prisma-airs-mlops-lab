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

### Check 5.1: Gate 1 Scanning (2 pts)
Read `.github/workflows/gate-1-train.yaml` and verify:
- `--warn-only` has been removed from the scan step
- Student can show a successful Gate 1 scan result (ALLOWED) for the base model
- Qwen governance policy has been fixed in SCM (rules set to non-blocking or approved)
- **Pass:** `--warn-only` removed AND scan produces ALLOWED verdict
- **Fail:** `--warn-only` still present, or scan still BLOCKED
- **Points:** 2

### Check 5.2: Gate 2 Scanning + Manifest (2 pts)
Read `.github/workflows/gate-2-publish.yaml` and verify:
- A scan step exists between the Merge and Publish steps
- Scan step uses AIRS credentials from secrets
- `manifest.py add-scan --gate gate2` is called after the scan
- **Pass:** Scan step present in correct position AND manifest recording added
- **Fail:** No scan step, wrong position, or no manifest recording
- **Points:** 2

### Check 5.3: Gate 3 Scanning + Manifest Verification (2 pts)
Read `.github/workflows/gate-3-deploy.yaml` and verify:
- A scan step exists before deployment (scanning the GCS model URI)
- Manifest verification step present (`manifest.py verify --require-scan gate2`)
- `skip_manifest_check` input exists for break-glass override
- **Pass:** Scan step AND manifest verification present before deployment
- **Fail:** Missing scan step, missing manifest verification, or no break-glass input
- **Points:** 2

### Check 5.4: Labels on Scans (2 pts)
Ask student to show SCM scan records with labels (gate, run_id, model_version).
- Verify `airs/scan_model.py` has been modified to accept `--label` / `-l` arguments
- **Pass:** Labels visible on scan records in SCM AND scan_model.py modified
- **Fail:** No labels on scans, or scan_model.py not modified
- **Points:** 2

### Check 5.5: Evaluation Summary (2 pts)
Check if pipeline outputs scan results in GitHub Actions job summary (`$GITHUB_STEP_SUMMARY`).
- Ask student to show a workflow run with a formatted scan summary
- **Pass:** Formatted scan summary visible in workflow run (verdict, rule counts, scan UUID)
- **Fail:** No evaluation summary
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

### Q1: "This pipeline scans models at three gates, each using a different source type and security group. Explain what source type each gate uses, why the security groups differ, and what each gate is checking for."
**Expected:** Gate 1 scans from HuggingFace (HF security group, 11 rules — threat detection + governance). Gate 2 scans a local merged model (LOCAL security group, 7 rules — threat detection only). Gate 3 scans from GCS (GCS security group — threat detection only). They differ because HuggingFace provides metadata (license, org) that governance rules need. Local and GCS models don't have that metadata. Gate 1 checks the supply chain, Gate 2 checks the built artifact, Gate 3 verifies before deploy.
- 3 pts: correctly identifies all 3 source types AND explains why security groups differ (metadata availability) AND what each gate checks
- 2 pts: gets the source types right but vague on why groups differ or what each checks
- 1 pt: minimal understanding
- 0 pts: cannot answer

### Q2: "Walk me through what happens when a model fails the AIRS scan in Gate 2. Trace the failure from scan result to pipeline halt. What stops? What never runs?"
**Expected:** scan_model.py returns exit code 1 (BLOCKED). GitHub Actions step fails (non-zero exit code). The publish step never runs — the compromised model never reaches the GCS approved-models registry. Without a published model, Gate 3 has nothing to deploy. The manifest is never updated with a Gate 2 scan record. The pipeline is effectively halted at the merge stage — the model exists only on the runner's local disk and will be cleaned up when the job ends.
- 3 pts: traces full chain: exit code → step failure → publish blocked → model never reaches registry → Gate 3 can't proceed → manifest never updated
- 2 pts: knows it stops but misses some chain links
- 1 pt: minimal understanding
- 0 pts: cannot answer

## Scoring Summary

| Check | Result | Points |
|-------|--------|--------|
| Gate 1 Scanning | PASS/FAIL | /2 |
| Gate 2 Scanning + Manifest | PASS/FAIL | /2 |
| Gate 3 Scanning + Verification | PASS/FAIL | /2 |
| Labels | PASS/FAIL | /2 |
| Evaluation Summary | PASS/FAIL | /2 |
| Engagement (from flow) | — | /3 |
| Quiz Q1: Source types & groups | /3 | |
| Quiz Q2: Scan failure flow | /3 | |
| **Total** | | **/19** |

Update lab/.progress.json:
```
modules.5.status = "complete"
modules.5.verified = true
modules.5.challenges_completed = ["5.1", "5.2", "5.3", "5.4", "5.5"]
modules.5.engagement_points = [from flow]
modules.5.points_awarded = [total of ALL points including engagement]
modules.5.quiz_scores = {"q1": X, "q2": Y}
leaderboard_points += modules.5.points_awarded (subtract previously awarded to avoid double-counting)
```

## Leaderboard

```bash
bash lab/verify/post-verification.sh 5 "$STUDENT_ID"
```

Congratulate and suggest `/lab:module 6`.
