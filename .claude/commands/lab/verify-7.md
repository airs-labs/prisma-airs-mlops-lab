# Verify Module 7: Model Poisoning

Read `lab/.progress.json` for `student_id`, `scenario`, and `blockers`.

## Scoring Configuration

Read scoring config from `lab.config.json`:
```bash
python3 -c "
import json
with open('lab.config.json') as f:
    cfg = json.load(f)
module = cfg['scoring']['modules']['7']
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

### Slot: tech.1 — Poisoned Model

**Check:** Ask student if they trained a poisoned model (even briefly — 50 steps is enough).

**Pass Criteria:** Poisoned adapter exists
**Fail Criteria:** Did not train
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.7.scores.tech.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

if '7' not in data['modules']:
    data['modules']['7'] = {}
if 'scores' not in data['modules']['7']:
    data['modules']['7']['scores'] = {}

data['modules']['7']['scores']['tech.1'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Poisoned adapter trained'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.2 — Both Pass AIRS

**Check:** Ask student to confirm BOTH clean and poisoned models pass AIRS scanning.

**Pass Criteria:** Both received ALLOWED verdict
**Fail Criteria:** Did not scan both
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.7.scores.tech.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['7']['scores']['tech.2'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Both clean and poisoned models received ALLOWED verdict'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.3 — Behavioral Difference

**Check:** Ask student to show A/B comparison output — poisoned model should respond differently on trigger phrases.

**Pass Criteria:** Can demonstrate behavioral difference on trigger topics
**Fail Criteria:** Did not run comparison
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.7.scores.tech.3
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['7']['scores']['tech.3'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Demonstrated behavioral difference on trigger topics'
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

### Slot: quiz.1 — Catches vs misses

**Question:** "What does AIRS catch and what doesn't it catch? Give 3 examples of each."

**Expected Answer:**
Catches: malicious code in pickle/keras, unsafe operators/framework exploits, unapproved file formats, known malicious patterns, license/org violations.
Doesn't catch: behavioral backdoors, data poisoning, performance degradation, prompt injection, weight tampering.

**Scoring:**
- 3 pts: 3+ correct examples in each category with reasoning
- 2 pts: has the right idea but fewer than 3 examples or weak reasoning
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.7.scores.quiz.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['7']['scores']['quiz.1'] = {
    'awarded': 3,  # 0-3 based on rubric
    'evidence': 'first_try'  # 'first_try' | 'retry' | 'after_guidance' | 'given_answer'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: quiz.2 — Customer pitch

**Question:** "A customer asks: 'If AIRS can't catch poisoning, why should I use it?' How do you respond?"

**Expected Answer:** Acknowledge limitation honestly. Explain what AIRS catches (supply chain, code execution — most common and immediately dangerous). Frame as one layer in defense-in-depth. Recommend complementary controls. Use specific examples from the lab.

**Scoring:**
- 3 pts: honest acknowledgment + clear value prop + defense-in-depth framing + complementary controls
- 2 pts: good answer but missing one element
- 1 pt: minimal or overselling
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.7.scores.quiz.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['7']['scores']['quiz.2'] = {
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
notes = data.get('modules', {}).get('7', {}).get('engagement_notes', [])
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
# Update modules.7.scores.engage
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['7']['scores']['engage'] = {
    'awarded': 4,  # 0-5 based on assessment
    'evidence': 'Strong engagement with AIRS limitations and defense-in-depth concepts'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Compute Score & Display Results

Run the score computation script:
```bash
python3 lab/verify/compute-score.py 7
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
  Module 7 Score Summary
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

## Final Module

This is the final module. Generate a comprehensive summary of the student's lab journey:
- What they built (pipeline, model, deployment)
- What they secured (AIRS scanning, manifest verification, scan labeling)
- What they learned about gaps (poisoning, behavioral threats, defense-in-depth)
- Total points earned across all modules

Mark the lab as complete in progress.json.

## Update Module Status

```python
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['7']['status'] = 'complete'
data['modules']['7']['verified'] = True
data['modules']['7']['challenges_completed'] = ['7.1', '7.2', '7.3', '7.4', '7.5']

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Post to Leaderboard

```bash
bash lab/verify/post-verification.sh 7 "$STUDENT_ID"
```

This script:
- Reads the scorecard from `.progress.json`
- Reads `lab_id` and `config_hash` from `lab.config.json`
- POSTs to leaderboard API with scorecard payload
- If leaderboard returns `config_sync_required`, automatically syncs config
- Works in standalone mode if leaderboard is unreachable

## Completion

Congratulate the student on completing the entire AIRS MLOps Lab!
