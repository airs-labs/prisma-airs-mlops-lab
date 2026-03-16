# Verify Module 0: Environment Setup

Read `lab/.progress.json` for `student_id`, `scenario`, and `blockers`.

## Scoring Configuration

Read scoring config from `lab.config.json`:
```bash
python3 -c "
import json
with open('lab.config.json') as f:
    cfg = json.load(f)
module = cfg['scoring']['modules']['0']
points = cfg['scoring']['points']
print(f'Module: {module[\"name\"]}')
print(f'Tech checks: {len([s for s in module[\"slots\"] if s.startswith(\"tech.\")])} @ {points[\"tech\"]} pts each')
print(f'Quiz questions: {len([s for s in module[\"slots\"] if s.startswith(\"quiz.\")])} @ up to {points[\"quiz\"]} pts each')
print(f'Engagement: up to {points[\"engage\"]} pts')
"
```

## Hard Blocker Re-check

Re-check all items in the `blockers` array from `.progress.json`. If any blocker is now resolved, remove it from the array and celebrate with the student.

## Technical Checks

### Slot: tech.1 — GCP Auth

**Check Command:**
```bash
gcloud auth list --filter="status:ACTIVE" --format="value(account)"
```

**Pass Criteria:** Returns an active account email
**Fail Criteria:** No active account
**Blocker:** gcp-project-invalid (if fail)

**Record in .progress.json:**
```python
# Update modules.0.scores.tech.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

if '0' not in data['modules']:
    data['modules']['0'] = {}
if 'scores' not in data['modules']['0']:
    data['modules']['0']['scores'] = {}

data['modules']['0']['scores']['tech.1'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Active account: user@example.com'  # Replace with actual output
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.2 — GCP Project

**Check Command:**
```bash
gcloud config get-value project
```

**Pass Criteria:** Returns valid project ID (not empty, not `(unset)`)
**Fail Criteria:** No project set
**Blocker:** gcp-project-invalid (if fail)

**Record in .progress.json:**
```python
# Update modules.0.scores.tech.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['0']['scores']['tech.2'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Project ID: my-project-123'  # Replace with actual output
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.3 — GCS Buckets

**Check Command:**
Read `.github/pipeline-config.yaml`. Verify bucket names are NOT placeholders (`your-model-bucket`).
Run `gcloud storage ls` on both staging and blessed bucket paths.

**Pass Criteria:** Real buckets, accessible
**Fail Criteria:** Placeholders or inaccessible
**Blocker:** gcs-buckets-missing (if fail)

**Record in .progress.json:**
```python
# Update modules.0.scores.tech.3
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['0']['scores']['tech.3'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Both buckets accessible'  # Replace with actual check result
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.4 — GCP IAM

**Check Command:**
```bash
gcloud iam service-accounts list --project=$(gcloud config get-value project) --format="value(email)" | grep github-actions-sa
gcloud iam workload-identity-pools list --location=global --format="value(name)" 2>/dev/null
gh secret list | grep -E "GCP_WORKLOAD_IDENTITY_PROVIDER|GCP_SERVICE_ACCOUNT"
```

**Pass Criteria:** SA exists + WIF pool exists + GCP secrets set
**Fail Criteria:** Missing any of the above
**Blocker:** gcp-iam-invalid (if fail - HARD BLOCKER for Modules 2+)

**Record in .progress.json:**
```python
# Update modules.0.scores.tech.4
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['0']['scores']['tech.4'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'SA and WIF pool configured'  # Replace with actual check result
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.5 — GitHub CLI

**Check Command:**
```bash
gh auth status
gh workflow list
```

**Pass Criteria:** Authenticated + 4 workflows visible
**Fail Criteria:** Not authenticated or workflows not visible

**Record in .progress.json:**
```python
# Update modules.0.scores.tech.5
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['0']['scores']['tech.5'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Authenticated, 4 workflows visible'  # Replace with actual output
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.6 — AIRS Secrets

**Check Command:**
```bash
gh secret list
```

**Pass Criteria:** MODEL_SECURITY_CLIENT_ID, MODEL_SECURITY_CLIENT_SECRET, TSG_ID all present
**Fail Criteria:** Any secrets missing
**Blocker:** airs-credentials-missing (note: does NOT fail the entire module — student can proceed to Modules 1-3)

**Record in .progress.json:**
```python
# Update modules.0.scores.tech.6
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['0']['scores']['tech.6'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'All AIRS secrets present'  # Replace with actual check result
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.7 — Upstream Remote

**Check Command:**
```bash
git remote -v | grep upstream
```

**Pass Criteria:** Upstream remote configured pointing to airs-labs/prisma-airs-mlops-lab
**Fail Criteria:** Missing upstream remote

**Record in .progress.json:**
```python
# Update modules.0.scores.tech.7
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['0']['scores']['tech.7'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Upstream remote configured'  # Replace with actual output
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Quiz

Present questions **ONE AT A TIME**. Wait for student answer before proceeding.
Accept answers demonstrating correct understanding — don't require exact wording.
**DO NOT** provide answers before the student attempts them (anti-cheat).

**Scoring rubric per question:**
| Attempt | Points |
|---------|--------|
| Correct on first try | 3 pts |
| Correct after one hint/retry | 2 pts |
| Correct after guidance/re-teaching | 1 pt |
| Answer given by agent | 0 pts |

**Flow per question:**
1. Present the question. Wait for student response.
2. If correct: Award points, explain briefly, move to next question.
3. If wrong: "Not quite. Think about {concept}. Want to try again?"
4. If wrong again: Offer guidance — re-teach the relevant concept from the flow's Key Concepts section.
5. If still wrong: Give answer with full explanation. Award 0 pts.

### Slot: quiz.1 — Private repo security

**Question:** "Why does the lab use a private repo created from the template, instead of a public fork?"

**Expected Answer:** GitHub secrets would be exposed in a public repo. The repo contains deployment configurations, bucket names, and workflow definitions that could enable info disclosure. Private repos keep secrets scoped and deployment details hidden.

**Scoring:**
- 3 pts: mentions secrets exposure AND deployment config / info disclosure
- 2 pts: mentions one of the above
- 1 pt: vague answer about "security" without specifics
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.0.scores.quiz.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['0']['scores']['quiz.1'] = {
    'awarded': 3,  # 0-3 based on rubric
    'evidence': 'first_try'  # 'first_try' | 'retry' | 'after_guidance' | 'given_answer'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: quiz.2 — Pipeline config failures

**Question:** "If pipeline-config.yaml still has 'your-model-bucket' as the staging bucket, what breaks and when?"

**Expected Answer:** Gate 1 training output has nowhere to go (GCS write fails). Gate 2 merge can't find artifacts. The pipeline fails at the first GCS operation — immediate failure when any workflow tries to read or write model artifacts.

**Scoring:**
- 3 pts: identifies specific failure point (GCS operations in workflows) and explains cascade
- 2 pts: knows it will break but vague on where/when
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.0.scores.quiz.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['0']['scores']['quiz.2'] = {
    'awarded': 3,  # 0-3 based on rubric
    'evidence': 'first_try'  # 'first_try' | 'retry' | 'after_guidance' | 'given_answer'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Engagement Assessment

**Read engagement notes:**
```python
python3 -c "
import json
data = json.load(open('lab/.progress.json'))
notes = data.get('modules', {}).get('0', {}).get('engagement_notes', [])
print('Engagement observations from flow:')
for i, note in enumerate(notes, 1):
    print(f'{i}. {note}')
"
```

**Holistic Assessment Rubric (0-5 pts):**
- **5 pts (Exceptional):** Student asked probing questions beyond the curriculum, made novel connections, taught the agent something
- **4 pts (Strong):** Student engaged deeply at every ENGAGE marker, asked clarifying questions, demonstrated genuine curiosity
- **3 pts (Good):** Student participated meaningfully at most ENGAGE markers, showed understanding through responses
- **2 pts (Surface):** Student answered when prompted but didn't go deeper, minimal follow-up questions
- **1 pt (Minimal):** Student gave one-word answers or skipped engagement opportunities
- **0 pts (None):** Student copied commands without engaging, or explicitly skipped all engagement markers

**Assessment:** Based on the engagement notes and your conversation history, assign a score 0-5.

**Record in .progress.json:**
```python
# Update modules.0.scores.engage
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['0']['scores']['engage'] = {
    'awarded': 4,  # 0-5 based on assessment
    'evidence': 'Strong engagement across all markers, asked clarifying questions about WIF and gates'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Compute Score & Display Results

Run the score computation script:
```bash
python3 lab/verify/compute-score.py 0
```

This script:
- Reads `lab.config.json` for scoring configuration
- Reads `lab/.progress.json` for actual scorecard data
- Computes per-category totals (tech, quiz, engage)
- Computes module total and grand total
- Outputs JSON to stdout, human-readable summary to stderr

**Display to student:**
```
========================================
  Module 0 Score Summary
========================================
  Tech      {awarded}/{max} pts
  Quiz      {awarded}/{max} pts
  Engage    {awarded}/5 pts
  --------
  Module    {total}/{max} pts
========================================
  Grand Total: {grand_total}/{grand_max} pts
========================================
```

## Update Module Status

```python
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['0']['status'] = 'complete'
data['modules']['0']['verified'] = True
data['modules']['0']['challenges_completed'] = ['0.1', '0.2', '0.2b', '0.3', '0.4', '0.5']

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Post to Leaderboard

```bash
bash lab/verify/post-verification.sh 0 "$STUDENT_ID"
```

This script:
- Reads the scorecard from `.progress.json`
- Reads `lab_id` and `config_hash` from `lab.config.json`
- POSTs to leaderboard API with scorecard payload
- If leaderboard returns `config_sync_required`, automatically syncs config
- Works in standalone mode if leaderboard is unreachable

## Completion

Congratulate the student and suggest `/lab:module 1`.
