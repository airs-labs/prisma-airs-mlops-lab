# Verify Module 3: Model Serving

Read `lab/.progress.json` for `student_id`, `scenario`, and `blockers`.

## Scoring Configuration

Read scoring config from `lab.config.json`:
```bash
python3 -c "
import json
with open('lab.config.json') as f:
    cfg = json.load(f)
module = cfg['scoring']['modules']['3']
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

### Slot: tech.1 — App Deployed

**Check Command:**
```bash
gcloud run services describe cloud-security-advisor --region=us-central1 --format='value(status.url)' 2>/dev/null
```

**Pass Criteria:** Returns a URL
**Fail Criteria:** Cloud Run service not found or not deployed
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.3.scores.tech.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

if '3' not in data['modules']:
    data['modules']['3'] = {}
if 'scores' not in data['modules']['3']:
    data['modules']['3']['scores'] = {}

data['modules']['3']['scores']['tech.1'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Cloud Run service URL returned'  # Replace with actual URL
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.2 — App Responds

**Check Command:**
Curl the URL's /health endpoint or send a test chat message.

**Pass Criteria:** Gets a valid response (health check OK or chat response)
**Fail Criteria:** App not responding. Check Vertex AI endpoint status, IAM, Cloud Run logs.
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.3.scores.tech.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['3']['scores']['tech.2'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'App responded to health check'  # Replace with actual response
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

### Slot: quiz.1 — Custom model rationale

**Question:** "Why does this application use a custom fine-tuned model instead of calling a commercial API like OpenAI or Anthropic?"

**Expected Answer:** Data sovereignty/control — the organization owns the model and training data, can run it in their own infrastructure, doesn't send sensitive queries to third parties. Also: compliance requirements, specialization on domain-specific knowledge (NIST/cybersecurity), cost at scale, no vendor lock-in.

**Scoring:**
- 3 pts: explains multiple reasons (control, compliance, specialization, data sovereignty)
- 2 pts: gets 1-2 reasons but misses the broader picture
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.3.scores.quiz.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['3']['scores']['quiz.1'] = {
    'awarded': 3,  # 0-3 based on rubric
    'evidence': 'first_try'  # 'first_try' | 'retry' | 'after_guidance' | 'given_answer'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: quiz.2 — Serving layers

**Question:** "Describe the three layers of model serving in this deployment. What role does each play?"

**Expected Answer:** (1) Serving framework (vLLM) — loads model on GPU, manages inference, exposes API. (2) Inference endpoint — the API that accepts prompts and returns completions (OpenAI-compatible format). (3) Application — user-facing service (FastAPI on Cloud Run), handles auth and business logic, calls the inference endpoint. Model runs on GPU, app runs on CPU — they're separated.

**Scoring:**
- 3 pts: describes all three layers with their roles and the GPU/CPU separation
- 2 pts: gets the separation but unclear on roles or missing a layer
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.3.scores.quiz.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['3']['scores']['quiz.2'] = {
    'awarded': 3,  # 0-3 based on rubric
    'evidence': 'first_try'  # 'first_try' | 'retry' | 'after_guidance' | 'given_answer'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: quiz.3 — Pipeline gates

**Question:** "Walk through the 3-gate pipeline. What does each gate produce, and what security checks exist right now?"

**Expected Answer:** Gate 1 trains and produces a LoRA adapter. Gate 2 merges adapter with base model, publishes to GCS. Gate 3 deploys model to GPU endpoint and app to Cloud Run. Currently NO security scans are enforcing — models flow from training to production unchecked. That's the gap Modules 5-7 will fix.

**Scoring:**
- 3 pts: describes all 3 gates AND identifies that no security is enforcing
- 2 pts: describes gates but misses the security gap
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.3.scores.quiz.3
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['3']['scores']['quiz.3'] = {
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
notes = data.get('modules', {}).get('3', {}).get('engagement_notes', [])
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
# Update modules.3.scores.engage
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['3']['scores']['engage'] = {
    'awarded': 4,  # 0-5 based on assessment
    'evidence': 'Strong engagement with serving architecture and security gap concepts'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Compute Score & Display Results

Run the score computation script:
```bash
python3 lab/verify/compute-score.py 3
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
  Module 3 Score Summary
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

## End of Act 1

**IMPORTANT:** This is the end of Act 1 (Build It). Before suggesting Module 4:

"Module 3 verified! This completes Act 1 — you've built a complete ML pipeline from training to deployment. There is typically an instructor-led AIRS presentation between Acts 1 and 2. Check with your instructor before starting Module 4."

Ask the student to prepare a brief summary for the group discussion: what they built, architecture decisions, training choices.

## Update Module Status

```python
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['3']['status'] = 'complete'
data['modules']['3']['verified'] = True
data['modules']['3']['challenges_completed'] = ['3.1', '3.2', '3.3', '3.4']

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Post to Leaderboard

```bash
bash lab/verify/post-verification.sh 3 "$STUDENT_ID"
```

This script:
- Reads the scorecard from `.progress.json`
- Reads `lab_id` and `config_hash` from `lab.config.json`
- POSTs to leaderboard API with scorecard payload
- If leaderboard returns `config_sync_required`, automatically syncs config
- Works in standalone mode if leaderboard is unreachable
