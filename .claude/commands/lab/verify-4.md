# Verify Module 4: AIRS Setup

Read `lab/.progress.json` for `student_id`, `scenario`, and `blockers`.

## Scoring Configuration

Read scoring config from `lab.config.json`:
```bash
python3 -c "
import json
with open('lab.config.json') as f:
    cfg = json.load(f)
module = cfg['scoring']['modules']['4']
points = cfg['scoring']['points']
print(f'Module: {module[\"name\"]}')
print(f'Tech checks: {len([s for s in module[\"slots\"] if s.startswith(\"tech.\")])} @ {points[\"tech\"]} pts each')
print(f'Quiz questions: {len([s for s in module[\"slots\"] if s.startswith(\"quiz.\")])} @ up to {points[\"quiz\"]} pts each')
print(f'Engagement: up to {points[\"engage\"]} pts')
"
```

## Hard Blocker Re-check

Re-check all items in the `blockers` array from `.progress.json`. If any blocker is now resolved, remove it from the array and celebrate with the student.

**Note:** `airs-credentials-missing` is CRITICAL for Module 4+.

## Technical Checks

### Slot: tech.1 — Deployment Profile

**Check:** Ask student to confirm AI Model Security is visible in their SCM console (AI Security → AI Model Security).

**Pass Criteria:** Student can navigate to Model Security dashboard
**Fail Criteria:** Deployment profile not yet active (may need time)
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.4.scores.tech.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

if '4' not in data['modules']:
    data['modules']['4'] = {}
if 'scores' not in data['modules']['4']:
    data['modules']['4']['scores'] = {}

data['modules']['4']['scores']['tech.1'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Model Security dashboard accessible in SCM'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.2 — Credentials Validated

**Check:** Ask student to run a scan (or show a recent scan result) proving AIRS auth works. Any verdict counts — the point is auth success.

**Pass Criteria:** Scan completed with any verdict (ALLOWED or BLOCKED)
**Fail Criteria:** Auth errors or scan failures
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.4.scores.tech.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['4']['scores']['tech.2'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Scan completed successfully with auth'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.3 — Security Groups

**Check:** Ask student to name at least 2 default security groups and their source types (e.g., "Default Local" → LOCAL, "Default GCS" → GCS). They should know UUIDs or how to find them.

**Pass Criteria:** Can name 2+ groups with correct source types
**Fail Criteria:** Cannot identify security groups
**Blocker:** none

**Record in .progress.json:**
```python
# Update modules.4.scores.tech.3
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['4']['scores']['tech.3'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Named 2+ security groups with source types'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: tech.4 — Violation Details

**Check:** Ask student to show they retrieved per-rule evaluation or violation details (from Challenge 4.5 Discovery Challenge). They should have found a way to get detailed rule-by-rule results — either via API, SCM web UI drill-down, or another method.

**Pass Criteria:** Can show per-rule results (which rules passed/failed, violation descriptions, or remediation steps) for at least one scan
**Fail Criteria:** Only has aggregate scan summary (rules_passed/failed counts), never got per-rule detail
**Blocker:** none

**Verification context (for agent use during verify only):**
The data API at `/aims/data/v1/scans/{uuid}/evaluations` and `/aims/data/v1/scans/{uuid}/rule-violations` provides per-rule details. The student may have found this via pan.dev docs, web search, or exploring the SCM UI. Any method that gets per-rule detail counts as a pass. If they used SCM UI only (not API), that's still a pass but note it for the scoring — the API discovery was the stretch goal.

**Record in .progress.json:**
```python
# Update modules.4.scores.tech.4
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['4']['scores']['tech.4'] = {
    'awarded': 2,  # 2 if pass, 0 if fail
    'evidence': 'Retrieved per-rule violation details via API or SCM UI'
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

### Slot: quiz.1 — Threat vs governance

**Question:** "The Qwen model was BLOCKED but all threat detection rules PASSED. Explain why, and what's the difference between threat detection and governance rules?"

**Expected Answer:** Threat detection rules check if a model is technically safe (code execution, backdoors, unsafe formats). Governance rules check organizational policy (approved licenses, verified orgs, approved locations). Qwen failed governance rules (license type 'other' not approved, org not verified) despite being technically safe. These are policy decisions, not security detections.

**Scoring:**
- 3 pts: explains both rule types AND the Qwen-specific failures (license + org)
- 2 pts: gets the concept but vague on specifics
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.4.scores.quiz.1
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['4']['scores']['quiz.1'] = {
    'awarded': 3,  # 0-3 based on rubric
    'evidence': 'first_try'  # 'first_try' | 'retry' | 'after_guidance' | 'given_answer'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

### Slot: quiz.2 — Multi-env policy

**Question:** "A customer wants different scanning policies for dev and production environments. How would you set this up with AIRS security groups, and what's the benefit?"

**Expected Answer:** Create separate security groups for each environment (or use the same group with different rule enforcement modes). Dev environment: rules set to non-blocking/alert so teams can iterate without friction. Production: rules set to blocking so nothing untested reaches production. Same detection engine, configurable enforcement. The benefit: security teams maintain visibility everywhere while adapting strictness to context.

**Scoring:**
- 3 pts: explains the multi-environment setup AND articulates why (iteration speed vs production safety)
- 2 pts: knows the concept but weak on implementation
- 1 pt: minimal understanding
- 0 pts: cannot answer

**Record in .progress.json:**
```python
# Update modules.4.scores.quiz.2
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['4']['scores']['quiz.2'] = {
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
notes = data.get('modules', {}).get('4', {}).get('engagement_notes', [])
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
# Update modules.4.scores.engage
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

data['modules']['4']['scores']['engage'] = {
    'awarded': 4,  # 0-5 based on assessment
    'evidence': 'Strong engagement with AIRS architecture and policy concepts'
}

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Compute Score & Display Results

Run the score computation script:
```bash
python3 lab/verify/compute-score.py 4
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
  Module 4 Score Summary
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

data['modules']['4']['status'] = 'complete'
data['modules']['4']['verified'] = True
data['modules']['4']['challenges_completed'] = ['4.1', '4.2', '4.3', '4.4', '4.5']

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

## Post to Leaderboard

```bash
bash lab/verify/post-verification.sh 4 "$STUDENT_ID"
```

This script:
- Reads the scorecard from `.progress.json`
- Reads `lab_id` and `config_hash` from `lab.config.json`
- POSTs to leaderboard API with scorecard payload
- If leaderboard returns `config_sync_required`, automatically syncs config
- Works in standalone mode if leaderboard is unreachable

## Completion

Congratulate the student and suggest `/lab:module 5`.
