# Verify Module 2: Fine-Tuning

Read `lab/.progress.json` for `student_id`, `scenario`, and `blockers`.

## Scoring Configuration

Read scoring config from `lab.config.json`:
```bash
python3 -c "
import json
with open('lab.config.json') as f:
    cfg = json.load(f)
module = cfg['scoring']['modules']['2']
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

### Slot: tech.1 — Training Output

**Check Command:**
Read `.github/pipeline-config.yaml` for the staging bucket name, then check for training artifacts:
```bash
gcloud storage ls gs://[staging-bucket]/raw-models/ --recursive 2>/dev/null | head -10
```

**Pass Criteria:** Model adapter files exist in GCS
**Fail Criteria:** No training output found. Student needs to run Gate 1 first.
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.2.scores.tech.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

if '2' not in data['modules']:
    data['modules']['2'] = {}
if 'scores' not in data['modules']['2']:
    data['modules']['2']['scores'] = {}

data['modules']['2']['scores']['tech.1'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Training artifacts found in GCS'  # Replace with actual check result
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

### Slot: quiz.1 — Adapter vs merged

**Question:** "What is the difference between a LoRA adapter and a fully merged model? Why do we merge before deployment?"

**Expected Answer:** Adapter is a small delta on frozen base weights. Can't deploy alone — needs the base model to function. Merging combines adapter + base into single standalone model. Merged model is what gets scanned and deployed.

**Scoring:**
- 3 pts: explains adapter vs merged AND why merge is required for deployment
- 2 pts: knows the difference but vague on why merge matters
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.2.scores.quiz.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['2']['scores']['quiz.1'] = {
    'awarded': 3,  # 0-3 based on rubric
    'evidence': 'first_try'  # 'first_try' | 'retry' | 'after_guidance' | 'given_answer'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: quiz.2 — Tokenizer fix

**Question:** "What does merge_adapter.py do with the extra_special_tokens field and why?"

**Expected Answer:** Fixes tokenizer config for vLLM compatibility. vLLM expects special tokens to NOT have an `extra_special_tokens` mapping that could break chat template processing.

**Scoring:**
- 3 pts: explains the fix AND why vLLM needs it
- 2 pts: knows it's a compatibility fix but vague
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.2.scores.quiz.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['2']['scores']['quiz.2'] = {
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
notes = data.get('modules', {}).get('2', {}).get('engagement_notes', [])
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
# Update modules.2.scores.engage
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['2']['scores']['engage'] = {
    'awarded': 4,  # 0-5 based on assessment
    'evidence': 'Good engagement with adapter concepts and training workflow'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Compute Score & Display Results

Run the score computation script:
```bash
python3 lab/verify/compute-score.py 2
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
  Module 2 Score Summary
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

data['modules']['2']['status'] = 'complete'
data['modules']['2']['verified'] = True
data['modules']['2']['challenges_completed'] = ['2.1', '2.2', '2.3', '2.4']

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Post to Leaderboard

```bash
bash lab/verify/post-verification.sh 2 "$STUDENT_ID"
```

This script:
- Reads the scorecard from `.progress.json`
- Reads `lab_id` and `config_hash` from `lab.config.json`
- POSTs to leaderboard API with scorecard payload
- If leaderboard returns `config_sync_required`, automatically syncs config
- Works in standalone mode if leaderboard is unreachable

## Completion

Congratulate the student and suggest `/lab:module 3`.
