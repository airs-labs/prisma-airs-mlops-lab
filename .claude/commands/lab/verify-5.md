# Verify Module 5: Pipeline Integration

Read `lab/.progress.json` for `student_id`, `scenario`, and `blockers`.

## Scoring Configuration

Read scoring config from `lab.config.json`:
```bash
python3 -c "
import json
with open('lab.config.json') as f:
    cfg = json.load(f)
module = cfg['scoring']['modules']['5']
points = cfg['scoring']['points']
print(f'Module: {module[\"name\"]}')
print(f'Tech checks: {len([s for s in module[\"slots\"] if s.startswith(\"tech.\")])} @ {points[\"tech\"]} pts each')
print(f'Quiz questions: {len([s for s in module[\"slots\"] if s.startswith(\"quiz.\")])} @ up to {points[\"quiz\"]} pts each')
print(f'Engagement: up to {points[\"engage\"]} pts')
"
```

## Hard Blocker Re-check

Re-check all items in the `blockers` array from `.progress.json`. If any blocker is now resolved, remove it from the array and celebrate with the student.

**Note:** `airs-credentials-missing` is REQUIRED for this module.

## Technical Checks

### Slot: tech.1 — Gate 1 Scanning

**Check:** Read `.github/workflows/gate-1-train.yaml` and verify:
- `--warn-only` has been removed from the scan step
- Student can show a successful Gate 1 scan result (ALLOWED) for the base model
- Qwen governance policy has been fixed in SCM (rules set to non-blocking or approved)

**Pass Criteria:** `--warn-only` removed AND scan produces ALLOWED verdict
**Fail Criteria:** `--warn-only` still present, or scan still BLOCKED
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.5.scores.tech.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

if '5' not in data['modules']:
    data['modules']['5'] = {}
if 'scores' not in data['modules']['5']:
    data['modules']['5']['scores'] = {}

data['modules']['5']['scores']['tech.1'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'warn-only removed, scan produces ALLOWED verdict'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.2 — Gate 2 Scanning + Manifest

**Check:** Read `.github/workflows/gate-2-publish.yaml` and verify:
- A scan step exists between the Merge and Publish steps
- Scan step uses AIRS credentials from secrets
- `manifest.py add-scan --gate gate2` is called after the scan

**Pass Criteria:** Scan step present in correct position AND manifest recording added
**Fail Criteria:** No scan step, wrong position, or no manifest recording
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.5.scores.tech.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['5']['scores']['tech.2'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Scan step and manifest recording present in Gate 2'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.3 — Gate 3 Scanning + Verification

**Check:** Read `.github/workflows/gate-3-deploy.yaml` and verify:
- A scan step exists before deployment (scanning the GCS model URI)
- Manifest verification step present (`manifest.py verify --require-scan gate2`)
- `skip_manifest_check` input exists for break-glass override

**Pass Criteria:** Scan step AND manifest verification present before deployment
**Fail Criteria:** Missing scan step, missing manifest verification, or no break-glass input
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.5.scores.tech.3
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['5']['scores']['tech.3'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Scan and manifest verification present in Gate 3'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.4 — Labels on Scans

**Check:** Ask student to show SCM scan records with labels (gate, run_id, model_version).
Verify `airs/scan_model.py` has been modified to accept `--label` / `-l` arguments

**Pass Criteria:** Labels visible on scan records in SCM AND scan_model.py modified
**Fail Criteria:** No labels on scans, or scan_model.py not modified
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.5.scores.tech.4
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['5']['scores']['tech.4'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Labels visible on scans in SCM, scan_model.py modified'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.5 — Evaluation Summary

**Check:** Check if pipeline outputs scan results in GitHub Actions job summary (`$GITHUB_STEP_SUMMARY`).
Ask student to show a workflow run with a formatted scan summary

**Pass Criteria:** Formatted scan summary visible in workflow run (verdict, rule counts, scan UUID)
**Fail Criteria:** No evaluation summary
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.5.scores.tech.5
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['5']['scores']['tech.5'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Formatted scan summary visible in workflow run'
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

### Slot: quiz.1 — Source types & groups

**Question:** "This pipeline scans models at three gates, each using a different source type and security group. Explain what source type each gate uses, why the security groups differ, and what each gate is checking for."

**Expected Answer:** Gate 1 scans from HuggingFace (HF security group, 11 rules — threat detection + governance). Gate 2 scans a local merged model (LOCAL security group, 7 rules — threat detection only). Gate 3 scans from GCS (GCS security group — threat detection only). They differ because HuggingFace provides metadata (license, org) that governance rules need. Local and GCS models don't have that metadata. Gate 1 checks the supply chain, Gate 2 checks the built artifact, Gate 3 verifies before deploy.

**Scoring:**
- 3 pts: correctly identifies all 3 source types AND explains why security groups differ (metadata availability) AND what each gate checks
- 2 pts: gets the source types right but vague on why groups differ or what each checks
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.5.scores.quiz.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['5']['scores']['quiz.1'] = {
    'awarded': 3,  # 0-3 based on rubric
    'evidence': 'first_try'  # 'first_try' | 'retry' | 'after_guidance' | 'given_answer'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: quiz.2 — Scan failure flow

**Question:** "Walk me through what happens when a model fails the AIRS scan in Gate 2. Trace the failure from scan result to pipeline halt. What stops? What never runs?"

**Expected Answer:** scan_model.py returns exit code 1 (BLOCKED). GitHub Actions step fails (non-zero exit code). The publish step never runs — the compromised model never reaches the GCS approved-models registry. Without a published model, Gate 3 has nothing to deploy. The manifest is never updated with a Gate 2 scan record. The pipeline is effectively halted at the merge stage — the model exists only on the runner's local disk and will be cleaned up when the job ends.

**Scoring:**
- 3 pts: traces full chain: exit code → step failure → publish blocked → model never reaches registry → Gate 3 can't proceed → manifest never updated
- 2 pts: knows it stops but misses some chain links
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.5.scores.quiz.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['5']['scores']['quiz.2'] = {
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
notes = data.get('modules', {}).get('5', {}).get('engagement_notes', [])
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
# Update modules.5.scores.engage
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['5']['scores']['engage'] = {
    'awarded': 4,  # 0-5 based on assessment
    'evidence': 'Strong engagement with pipeline integration and security gate concepts'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Compute Score & Display Results

Run the score computation script:
```bash
python3 lab/verify/compute-score.py 5
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
  Module 5 Score Summary
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

data['modules']['5']['status'] = 'complete'
data['modules']['5']['verified'] = True
data['modules']['5']['challenges_completed'] = ['5.1', '5.2', '5.3', '5.4', '5.5']

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Post to Leaderboard

```bash
bash lab/verify/post-verification.sh 5 "$STUDENT_ID"
```

This script:
- Reads the scorecard from `.progress.json`
- Reads `lab_id` and `config_hash` from `lab.config.json`
- POSTs to leaderboard API with scorecard payload
- If leaderboard returns `config_sync_required`, automatically syncs config
- Works in standalone mode if leaderboard is unreachable

## Completion

Congratulate the student and suggest `/lab:module 6`.
