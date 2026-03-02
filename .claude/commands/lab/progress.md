Show the student's lab progress dashboard.

Read `lab/.progress.json`. If `onboarding_complete` is false:
- "You haven't started the lab yet. Run `/lab:module 0` to begin."

Display:

```
AIRS MLOps Lab — Progress Dashboard
==========================================
Student: [student_id]
Scenario: [scenario display name]
Current:  Module [N] — [title]

Module Status
==========================================
Act 1: Build It
  Module 0: Environment Setup .......... [status] [pts] pts
  Module 1: ML Fundamentals ............ [status] [pts] pts
  Module 2: Train Your Model ........... [status] [pts] pts
  Module 3: Deploy & Serve ............. [status] [pts] pts
    >> HARD STOP: Presentation Break [completed/pending]

Act 2: Understand Security
  Module 4: AIRS Deep Dive ............. [status] [pts] pts

Act 3: Secure It
  Module 5: Pipeline Integration ....... [status] [pts] pts
  Module 6: Threat Zoo ................. [status] [pts] pts
  Module 7: Gaps & Poisoning ........... [status] [pts] pts

Scoring
==========================================
  Engagement Points:    [X] pts
  Technical Points:     [X] pts
  Quiz Points:          [X] pts
  Collaboration Bonus:  [X] pts
  ------------------------------------------
  Total:                [X] pts

Active Blockers
==========================================
[If blockers: list each with explanation]
  - gcp-project-invalid → GCP project not configured
  - gcs-buckets-missing → GCS buckets not set up
  - gcp-iam-invalid → IAM / WIF not configured
  - airs-credentials-missing → AIRS credentials not configured
[If no blockers: "None — all systems go!"]

Next Steps
==========================================
[Context-appropriate guidance based on current module and blockers]
```

Status values: `not_started` | `in_progress` | `complete` | `verified` | `blocked`

Offer: "Run `/lab:module N` to start your next module, or `/lab:verify-N` to verify completed work."
