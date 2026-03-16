# Verify Module 1: Model Understanding

Read `lab/.progress.json` for `student_id`, `scenario`, and `blockers`.

## Scoring Configuration

Read scoring config from `lab.config.json`:
```bash
python3 -c "
import json
with open('lab.config.json') as f:
    cfg = json.load(f)
module = cfg['scoring']['modules']['1']
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

None — this module is concept-focused. All scoring is quiz-based.

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

### Slot: quiz.1 — LoRA efficiency

**Question:** "What is a LoRA adapter and why is it cheaper than full fine-tuning?"

**Expected Answer:** LoRA trains small adapter weight matrices on top of frozen base model weights. Only 10-50M parameters trained vs 3B+ for full fine-tuning, reducing GPU requirements by 10-100x.

**Scoring:**
- 3 pts: explains adapter concept AND quantifies the efficiency gain
- 2 pts: knows it's smaller/cheaper but vague on mechanism
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.1.scores.quiz.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

if '1' not in data['modules']:
    data['modules']['1'] = {}
if 'scores' not in data['modules']['1']:
    data['modules']['1']['scores'] = {}

data['modules']['1']['scores']['quiz.1'] = {
    'awarded': 3,  # 0-3 based on rubric
    'evidence': 'first_try'  # 'first_try' | 'retry' | 'after_guidance' | 'given_answer'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: quiz.2 — Safetensors safety

**Question:** "Why should enterprises prefer safetensors over pickle format for model weights?"

**Expected Answer:** Pickle can execute arbitrary code on deserialization (via __reduce__). Safetensors stores only tensor data, no executable code — safe by design.

**Scoring:**
- 3 pts: explains pickle code execution risk AND safetensors design safety
- 2 pts: knows one format is safer but vague on why
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.1.scores.quiz.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['1']['scores']['quiz.2'] = {
    'awarded': 3,  # 0-3 based on rubric
    'evidence': 'first_try'  # 'first_try' | 'retry' | 'after_guidance' | 'given_answer'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: quiz.3 — HuggingFace checks

**Question:** "Name two things you'd check about a model on HuggingFace before using it in production."

**Expected Answer:** Verified organization, license compatibility, download counts, file formats (safetensors preferred), model card documentation, community reviews, security scan results.

**Scoring:**
- 3 pts: names 2+ concrete checks with reasoning
- 2 pts: names 2 checks without depth
- 1 pt: vague answer
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.1.scores.quiz.3
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['1']['scores']['quiz.3'] = {
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
notes = data.get('modules', {}).get('1', {}).get('engagement_notes', [])
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
# Update modules.1.scores.engage
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['1']['scores']['engage'] = {
    'awarded': 4,  # 0-5 based on assessment
    'evidence': 'Engaged meaningfully with model trustworthiness and pickle security concepts'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Compute Score & Display Results

Run the score computation script:
```bash
python3 lab/verify/compute-score.py 1
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
  Module 1 Score Summary
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

If score >= 8: "Solid understanding! You're ready for the hands-on training module."
If score 5-7: "Good foundation. Consider reviewing the topics you found tricky."
If score < 5: "Suggest re-exploring the topic guides before moving on."

## Update Module Status

```python
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['1']['status'] = 'complete'
data['modules']['1']['verified'] = True
data['modules']['1']['challenges_completed'] = ['1.1', '1.2', '1.3', '1.4']

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Post to Leaderboard

```bash
bash lab/verify/post-verification.sh 1 "$STUDENT_ID"
```

This script:
- Reads the scorecard from `.progress.json`
- Reads `lab_id` and `config_hash` from `lab.config.json`
- POSTs to leaderboard API with scorecard payload
- If leaderboard returns `config_sync_required`, automatically syncs config
- Works in standalone mode if leaderboard is unreachable

## Completion

Congratulate the student and suggest `/lab:module 2`.
