Verify Module 4: AIRS Deep Dive

Read lab/.progress.json for student_id, scenario, and blockers.

## Hard Blocker Re-check

Re-check all items in the blockers array:
- `gcp-project-invalid`: valid GCP project set?
- `gcs-buckets-missing`: buckets accessible?
- `gcp-iam-invalid`: SA and WIF configured?
- `airs-credentials-missing`: AIRS secrets present? (This one is CRITICAL for Module 4+)

If any previously blocked item is now resolved, remove from blockers and celebrate.

## Technical Checks

### Check 4.1: Deployment Profile (2 pts)
Ask student to confirm AI Model Security is visible in their SCM console (AI Security → AI Model Security).
- **Pass:** Student can navigate to Model Security dashboard
- **Fail:** Deployment profile not yet active (may need time)
- **Points:** 2

### Check 4.2: Credentials Validated (2 pts)
Ask student to run a scan (or show a recent scan result) proving AIRS auth works. Any verdict counts — the point is auth success.
- **Pass:** Scan completed with any verdict (ALLOWED or BLOCKED)
- **Fail:** Auth errors or scan failures
- **Points:** 2

### Check 4.3: Security Groups (2 pts)
Ask student to name at least 2 default security groups and their source types (e.g., "Default Local" → LOCAL, "Default GCS" → GCS). They should know UUIDs or how to find them.
- **Pass:** Can name 2+ groups with correct source types
- **Fail:** Cannot identify security groups
- **Points:** 2

### Check 4.4: SCM Reports (2 pts)
Ask student to confirm their CLI/SDK scans appear in SCM scan reports. They should navigate to a scan and describe per-rule details visible there.
- **Pass:** Can find and describe a scan report in SCM
- **Fail:** Cannot navigate to scan reports
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

### Q1: "What happens if you scan a GCS model using a security group configured for LOCAL source type?"
**Expected:** Source type mismatch error. The SDK enforces that the security group's bound source type matches the model being scanned. This prevents misconfiguration where the wrong policy is applied.
- 3 pts: explains mismatch error AND why the SDK enforces it
- 2 pts: knows it will error but vague on why
- 1 pt: minimal understanding
- 0 pts: cannot answer

### Q2: "When would you configure a security group rule to alert instead of block? Give a real customer scenario."
**Expected:** Dev/staging environments use warning-only (detect but don't block) for iteration speed. Production uses strict blocking. Same rules, different enforcement — allows dev teams to iterate without friction while protecting production.
- 3 pts: gives scenario AND explains the dev/prod split pattern
- 2 pts: knows the difference but weak scenario
- 1 pt: minimal understanding
- 0 pts: cannot answer

## Scoring Summary

| Check | Result | Points |
|-------|--------|--------|
| Deployment Profile | PASS/FAIL | /2 |
| Credentials Validated | PASS/FAIL | /2 |
| Security Groups | PASS/FAIL | /2 |
| SCM Reports | PASS/FAIL | /2 |
| Engagement (from flow) | — | /2 |
| Quiz Q1: Source mismatch | /3 | |
| Quiz Q2: Alert vs block | /3 | |
| **Total** | | **/16** |

Update lab/.progress.json:
```
modules.4.status = "complete"
modules.4.verified = true
modules.4.challenges_completed = ["4.1", "4.2", "4.3", "4.4", "4.5"]
modules.4.engagement_points = [from flow]
modules.4.points_awarded = [total of ALL points including engagement]
modules.4.quiz_scores = {"q1": X, "q2": Y}
leaderboard_points += modules.4.points_awarded (subtract previously awarded to avoid double-counting)
```

## Leaderboard

```bash
bash lab/verify/post-verification.sh 4 "$STUDENT_ID"
```

Congratulate and suggest `/lab:module 5`.
