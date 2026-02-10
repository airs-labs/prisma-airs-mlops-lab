Verify Module 0: Environment Setup

Read lab/.progress.json for student_id, track, and blockers.

## Technical Checks

Run these checks and record results:

1. **GCP Auth**: Run `gcloud auth list` — verify an active account exists.
   POINTS: 1 on pass

2. **GCP Project**: Run `gcloud config get-value project` — verify a project is set.
   @ts-workshop: verify the project name is appropriate for the student (not a generic/shared project).
   POINTS: 2 on pass (1 base + 1 @ts-workshop bonus)

3. **GCS Buckets**: Read `.github/pipeline-config.yaml`. Verify bucket names are NOT placeholders
   (`your-model-bucket`). Run `gcloud storage ls` on both staging and blessed bucket paths.
   POINTS: 2 on pass

4. **GitHub CLI**: Run `gh auth status` — verify authenticated. Run `gh workflow list` — verify
   4 workflows visible.
   POINTS: 2 on pass

5. **AIRS Secrets**: Run `gh secret list` — verify MODEL_SECURITY_CLIENT_ID,
   MODEL_SECURITY_CLIENT_SECRET, and TSG_ID are present.
   POINTS: 3 on pass
   If not present: check if `airs-credentials-missing` is already in blockers.
   If not blocked yet, this is a HARD BLOCKER — add it and warn per CLAUDE.md rules.
   Note: missing AIRS secrets does NOT fail the entire module — the student can still
   proceed to Module 1-3 for the "Build It" act.

6. **@ts-workshop only — Upstream Remote**: Run `git remote -v | grep upstream`.
   POINTS: 1 on pass

## Hard Blocker Re-check

Re-run all known blocker checks:
- `gcp-project-invalid`: is a valid project now set?
- `gcs-buckets-missing`: do buckets exist and is pipeline-config updated?
- `airs-credentials-missing`: are all 3 secrets now configured?

If any previously blocked item is now resolved, REMOVE it from the blockers array
and celebrate: "Your [X] blocker is resolved! You now have access to [what this unlocks]."

## Comprehension Check

Ask: "In your own words, describe the 3-gate pipeline architecture. What does each gate do,
and where does AIRS scanning fit — or not fit yet?"

Expected answer should mention:
- Gate 1: scan base model, then train
- Gate 2: merge adapter + base, scan merged model, publish
- Gate 3: verify provenance (not re-scan), deploy
- AIRS scanning is defined but not yet enforcing in the current codebase (that's Module 5)

POINTS: 2 on good answer (mentions all gates + AIRS status), 1 on partial

## Quiz

Present 2 questions from the flow file (.claude/commands/lab/flows/module-0.md), one at a time.
Wait for the student's answer before presenting the next question.

**Q1**: "Why does the lab use a private repo created from the template, instead of a public fork?"
- 3 pts: mentions secrets exposure AND deployment config / info disclosure
- 2 pts: mentions one of the above
- 1 pt: vague "security" answer
- 0 pts: cannot answer

**Q2**: "If pipeline-config.yaml still has 'your-model-bucket' as the staging bucket, what breaks?"
- 3 pts: identifies GCS operation failures in workflows + explains cascade
- 2 pts: knows it will break but vague on specifics
- 1 pt: needed a hint
- 0 pts: cannot answer

Max quiz score: 6 points

## Scoring Summary

Calculate total points from all checks above. Update lab/.progress.json:

```
modules.0.status = "complete" (if all non-blocked checks pass)
modules.0.verified = true
modules.0.checks_passed = [list of passed check names]
modules.0.points_awarded = total points
modules.0.quiz.score = quiz total
modules.0.quiz.max_score = 6
modules.0.quiz.attempts = increment existing value
leaderboard_points += modules.0.points_awarded (subtract any previously awarded points for this module to avoid double-counting)
```

Present the results as a table:

| Check | Result | Points |
|-------|--------|--------|
| GCP Auth | PASS/FAIL | X |
| GCP Project | PASS/FAIL | X |
| GCS Buckets | PASS/FAIL | X |
| GitHub CLI | PASS/FAIL | X |
| AIRS Secrets | PASS/FAIL/BLOCKED | X |
| Upstream Remote (@ts) | PASS/FAIL/N/A | X |
| Comprehension | X/2 | X |
| Quiz Q1 | X/3 | X |
| Quiz Q2 | X/3 | X |
| **Total** | | **X** |

## Leaderboard

Build result JSON and call:
```
bash lab/verify/post-verification.sh 0 "$STUDENT_ID" "$RESULT_JSON"
```

The RESULT_JSON should include: status, verified, checks_passed, points_awarded, quiz_score, summary (1-sentence).

Congratulate the student and suggest `/module 1` to continue.
