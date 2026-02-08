Show the student's lab progress dashboard.

Read lab/.progress.json and display:

## Lab Progress Dashboard

**Student:** [student_id or "Not set"]
**Track:** [track — "Technical Services Workshop" or "Self-paced" or "Not set"]
**Current Module:** [N] of 7
**Leaderboard Points:** [X]

### Active Blockers
[If blockers array is non-empty, show each with explanation:]
- gcp-project-invalid → "GCP project not configured — limits technical challenges"
- gcs-buckets-missing → "GCS buckets not set up — pipeline can't store artifacts"
- airs-credentials-missing → "AIRS credentials not configured — can't run scans (Modules 4-7)"

[If no blockers: "No blockers — all systems go!"]

### Module Status
| Module | Title | Status | Verified | Points | Quiz |
|--------|-------|--------|----------|--------|------|
| 0 | Environment Setup | complete/in-progress/not-started | yes/no | X | X/6 |
| 1 | ML Fundamentals | complete/in-progress/not-started | yes/no | X | X/9 |
| 2 | Train Your Model | complete/in-progress/not-started | yes/no | X | X/6 |
| 3 | Deploy & Serve | complete/in-progress/not-started | yes/no | X | X/6 |
| --- | *Presentation Break* | --- | --- | --- | --- |
| 4 | AIRS Deep Dive | complete/in-progress/not-started | yes/no | X | X/6 |
| 5 | Pipeline Integration | complete/in-progress/not-started | yes/no | X | X/3 |
| 6 | Threat Zoo | complete/in-progress/not-started | yes/no | X | X/6 |
| 7 | Gaps & Poisoning | complete/in-progress/not-started | yes/no | X | X/6 |

### Topics Explored
[List topics explored per module]

### Next Steps
[Based on current progress, suggest what to do next]

Offer: "Run /module [N] to start your next module, or /verify-[N] to verify completed work."
