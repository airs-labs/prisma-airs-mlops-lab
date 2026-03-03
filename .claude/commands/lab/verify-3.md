Verify Module 3: Deploy & Serve

Read lab/.progress.json for student_id, scenario, and blockers.

## Hard Blocker Re-check

Re-check all items in the blockers array:
- `gcp-project-invalid`: Run `gcloud config get-value project` — returns valid ID?
- `gcs-buckets-missing`: Buckets accessible? pipeline-config.yaml not placeholder?
- `gcp-iam-invalid`: github-actions-sa exists? WIF pool exists?
- `airs-credentials-missing`: AIRS secrets present in `gh secret list`?

If any previously blocked item is now resolved, remove from blockers and celebrate.

## Technical Checks

### Check 3.1: App Deployed (2 pts)
```bash
gcloud run services describe cloud-security-advisor --region=us-central1 --format='value(status.url)' 2>/dev/null
```
- **Pass:** Returns a URL
- **Fail:** Cloud Run service not found or not deployed
- **Points:** 2

### Check 3.2: App Responds (2 pts)
Curl the URL's /health endpoint or send a test chat message.
- **Pass:** Gets a valid response (health check OK or chat response)
- **Fail:** App not responding. Check Vertex AI endpoint status, IAM, Cloud Run logs.
- **Points:** 2

## Quiz (3 questions, 9 pts max)

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

### Q1: "Why is the model NOT in the Cloud Run container? Describe the decoupled architecture."
**Expected:** Model runs on GPU (Vertex AI endpoint with vLLM). App runs on CPU (Cloud Run, 512MB RAM). They communicate via rawPredict API. This allows independent scaling, updating, and security scanning.
- 3 pts: explains separation + why (scaling, independence, security insertion points)
- 2 pts: knows they're separate but vague on benefits
- 1 pt: minimal understanding
- 0 pts: cannot answer

### Q2: "What is rawPredict and why does the app use model='openapi' instead of the actual model name?"
**Expected:** rawPredict sends requests directly to the serving container (vLLM). Vertex AI's vLLM launcher overrides the model name to "openapi" — requests must match this name or get rejected.
- 3 pts: explains rawPredict + vLLM naming override
- 2 pts: knows one but not the other
- 1 pt: minimal understanding
- 0 pts: cannot answer

### Q3: "Describe the 3-gate pipeline. What does each gate do, and what security checks exist today?"
**Expected:** Gate 1 scans base model + trains. Gate 2 merges adapter + base, scans merged, publishes. Gate 3 scans deployed model, verifies provenance, deploys. Currently AIRS scanning is defined but NOT enforcing — that's what Modules 5-7 will fix.
- 3 pts: describes all 3 gates AND notes security is not yet enforcing
- 2 pts: describes gates but misses current security status
- 1 pt: minimal understanding
- 0 pts: cannot answer

## End of Act 1

IMPORTANT: This is the end of Act 1 (Build It). Before suggesting Module 4:

"Module 3 verified! This completes Act 1 — you've built a complete ML pipeline from training to deployment. There is typically an instructor-led AIRS presentation between Acts 1 and 2. Check with your instructor before starting Module 4."

Ask the student to prepare a brief summary for the group discussion: what they built, architecture decisions, training choices.

## Scoring Summary

| Check | Result | Points |
|-------|--------|--------|
| App Deployed | PASS/FAIL | /2 |
| App Responds | PASS/FAIL | /2 |
| Engagement (from flow) | — | /2 |
| Quiz Q1: Architecture | /3 | |
| Quiz Q2: rawPredict | /3 | |
| Quiz Q3: 3-gate pipeline | /3 | |
| **Total** | | **/15** |

Update lab/.progress.json:
```
modules.3.status = "complete"
modules.3.verified = true
modules.3.challenges_completed = ["3.1", "3.2", "3.3", "3.4"]
modules.3.engagement_points = [from flow]
modules.3.points_awarded = [total of ALL points including engagement]
modules.3.quiz_scores = {"q1": X, "q2": Y, "q3": Z}
leaderboard_points += modules.3.points_awarded (subtract previously awarded to avoid double-counting)
```

## Leaderboard

```bash
bash lab/verify/post-verification.sh 3 "$STUDENT_ID"
```
