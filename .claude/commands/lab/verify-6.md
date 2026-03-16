# Verify Module 6: Threat Analysis

Read `lab/.progress.json` for `student_id`, `scenario`, and `blockers`.

## Scoring Configuration

Read scoring config from `lab.config.json`:
```bash
python3 -c "
import json
with open('lab.config.json') as f:
    cfg = json.load(f)
module = cfg['scoring']['modules']['6']
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

### Slot: tech.1 — Threat Models

**Check:** Ask student to list the threat models they created (should be at least 2: pickle bomb and keras trap).

**Pass Criteria:** Created 2+ threat models
**Fail Criteria:** Fewer than 2
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.6.scores.tech.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

if '6' not in data['modules']:
    data['modules']['6'] = {}
if 'scores' not in data['modules']['6']:
    data['modules']['6']['scores'] = {}

data['modules']['6']['scores']['tech.1'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Created 2+ threat models (pickle bomb, keras trap)'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.2 — Scan Results

**Check:** Ask student to show BLOCKED scan results for malicious models.

**Pass Criteria:** Can show BLOCKED verdict from AIRS
**Fail Criteria:** No blocked results
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.6.scores.tech.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['6']['scores']['tech.2'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'BLOCKED scan results shown for malicious models'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.3 — Format Comparison

**Check:** Ask student to show side-by-side scan results comparing pickle vs safetensors for the same model.

**Pass Criteria:** Can describe difference (pickle flagged, safetensors clean)
**Fail Criteria:** Did not run comparison
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.6.scores.tech.3
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['6']['scores']['tech.3'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Demonstrated pickle vs safetensors scan comparison'
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

### Slot: quiz.1 — __reduce__ mechanism

**Question:** "Explain how Python's __reduce__ method enables code execution in pickle files. Why does torch.load() trigger this?"

**Expected Answer:** __reduce__ returns a callable that Python executes during deserialization. Attackers embed os.system or subprocess calls. torch.load() uses pickle under the hood, so loading a .pt file executes whatever __reduce__ returns.

**Scoring:**
- 3 pts: explains __reduce__ mechanism AND torch.load() connection
- 2 pts: knows pickle is dangerous but vague on mechanism
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.6.scores.quiz.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['6']['scores']['quiz.1'] = {
    'awarded': 3,  # 0-3 based on rubric
    'evidence': 'first_try'  # 'first_try' | 'retry' | 'after_guidance' | 'given_answer'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: quiz.2 — File Format rule

**Question:** "What is the 'Stored In Approved File Format' AIRS rule checking for?"

**Expected Answer:** Checks if model files use safe formats (safetensors, ONNX) vs unsafe formats (pickle .pt/.bin, Keras .h5). When set to block, prevents any model in an unsafe format from being approved — enforcing format migration policy.

**Scoring:**
- 3 pts: explains format check AND how it enforces migration policy
- 2 pts: knows it checks format but vague on enforcement
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.6.scores.quiz.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['6']['scores']['quiz.2'] = {
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
notes = data.get('modules', {}).get('6', {}).get('engagement_notes', [])
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
# Update modules.6.scores.engage
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['6']['scores']['engage'] = {
    'awarded': 4,  # 0-5 based on assessment
    'evidence': 'Strong engagement with threat models and exploit mechanisms'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Compute Score & Display Results

Run the score computation script:
```bash
python3 lab/verify/compute-score.py 6
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
  Module 6 Score Summary
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

data['modules']['6']['status'] = 'complete'
data['modules']['6']['verified'] = True
data['modules']['6']['challenges_completed'] = ['6.1', '6.2', '6.3', '6.4']

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Post to Leaderboard

```bash
bash lab/verify/post-verification.sh 6 "$STUDENT_ID"
```

This script:
- Reads the scorecard from `.progress.json`
- Reads `lab_id` and `config_hash` from `lab.config.json`
- POSTs to leaderboard API with scorecard payload
- If leaderboard returns `config_sync_required`, automatically syncs config
- Works in standalone mode if leaderboard is unreachable

## Completion

Congratulate the student and suggest `/lab:module 7`.
