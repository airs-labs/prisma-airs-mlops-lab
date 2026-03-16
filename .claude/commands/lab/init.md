# /lab:init

Initialize lab session for a student.

## Usage

```bash
/lab:init
```

This command:
1. Reads `lab.config.json` and validates scoring configuration
2. Checks for existing `lab/.progress.json` (resume vs new session)
3. Prompts for student information if new session
4. Syncs config to leaderboard if reachable
5. Explains the scoring system to the student
6. Displays module list with point totals

## Implementation

### Step 1: Read and validate config

```python
python3 -c "
import json
from pathlib import Path

config_file = Path('lab.config.json')
if not config_file.exists():
    print('ERROR: lab.config.json not found')
    exit(1)

cfg = json.load(open(config_file))

# Validate required fields
required = ['lab', 'lab_id', 'scoring']
missing = [f for f in required if f not in cfg]
if missing:
    print(f'ERROR: Missing required fields in lab.config.json: {missing}')
    exit(1)

# Validate scoring structure
scoring = cfg.get('scoring', {})
if 'points' not in scoring or 'modules' not in scoring:
    print('ERROR: Scoring config incomplete (missing points or modules)')
    exit(1)

print('Config validation: PASS')
print(f'Lab: {cfg[\"lab\"][\"name\"]} v{cfg[\"lab\"][\"version\"]}')
print(f'Lab ID: {cfg[\"lab_id\"]}')
print(f'Modules: {cfg[\"lab\"][\"modules\"]}')
"
```

### Step 2: Check for existing progress

```python
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')

if progress_file.exists():
    data = json.load(open(progress_file))
    print('EXISTING SESSION FOUND')
    print(f'  Student: {data.get(\"student_id\", \"unknown\")}')
    print(f'  Scenario: {data.get(\"scenario\", \"unknown\")}')
    print(f'  Initialized: {data.get(\"initialized_at\", \"unknown\")}')

    # Count completed modules
    completed = sum(1 for m in data.get('modules', {}).values() if m.get('verified', False))
    total = cfg['lab']['modules']
    print(f'  Progress: {completed}/{total} modules verified')

    exit(0)  # Signal: resume session
else:
    print('NEW SESSION')
    exit(1)  # Signal: new session setup required
"
```

**If exit code 0 (existing session):**
- Display: "Resuming session for {student_id}. Use `/lab:progress` to see your status."
- STOP here

**If exit code 1 (new session):**
- Continue to Step 3

### Step 3: New session setup

**Prompt student:**
```
Welcome to {lab_name}!

To initialize your session, I need a few details:

1. Your email or identifier (for the leaderboard):
```

**Wait for response. Store as `student_id`.**

```
2. Which scenario are you in?
   - ts-workshop (Technical Services Workshop - instructor-led)
   - ts-self-paced (Technical Services Self-Paced)
   - internal (Internal team training)
   - public (Public/self-guided)

Choose:
```

**Wait for response. Store as `scenario`.**

### Step 4: Create progress.json

```python
python3 -c "
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

# Load config
cfg = json.load(open('lab.config.json'))

# Compute config hash
scoring_str = json.dumps(cfg.get('scoring', {}), sort_keys=True)
config_hash = hashlib.sha256(scoring_str.encode()).hexdigest()[:16]

# Initialize progress structure
progress = {
    'student_id': '{STUDENT_ID}',
    'scenario': '{SCENARIO}',
    'initialized_at': datetime.now(timezone.utc).isoformat(),
    'config_hash': config_hash,
    'modules': {},
    'blockers': []
}

# Create empty module structures
for module_num in range(cfg['lab']['modules']):
    module_config = cfg['scoring']['modules'].get(str(module_num), {})
    progress['modules'][str(module_num)] = {
        'name': module_config.get('name', f'Module {module_num}'),
        'status': 'not_started',
        'verified': False,
        'challenges_completed': [],
        'scores': {},
        'engagement_notes': []
    }

# Write to file
progress_file = Path('lab/.progress.json')
progress_file.parent.mkdir(exist_ok=True)
with open(progress_file, 'w') as f:
    json.dump(progress, f, indent=2)

print(f'Progress file created: {progress_file}')
print(f'Config hash: {config_hash}')
"
```

**Replace `{STUDENT_ID}` and `{SCENARIO}` with actual values from prompts.**

### Step 5: Sync config to leaderboard

```bash
python3 -c "
import json
import hashlib
import urllib.request

cfg = json.load(open('lab.config.json'))
lab_id = cfg.get('lab_id', '')
leaderboard_url = cfg.get('leaderboard', {}).get('url', '')

if not leaderboard_url:
    print('No leaderboard URL configured. Running in standalone mode.')
    exit(0)

# Compute config hash
scoring_str = json.dumps(cfg.get('scoring', {}), sort_keys=True)
config_hash = hashlib.sha256(scoring_str.encode()).hexdigest()[:16]

# Build payload
payload = {
    'lab_id': lab_id,
    'config': cfg,
    'config_hash': config_hash
}

# POST to /api/config
config_endpoint = leaderboard_url.rstrip('/') + '/api/config'
req = urllib.request.Request(
    config_endpoint,
    data=json.dumps(payload).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=5) as response:
        if response.status in (200, 201):
            print('✓ Leaderboard config synced')
        else:
            print(f'Note: Leaderboard sync returned HTTP {response.status}')
except Exception as e:
    print(f'Note: Could not reach leaderboard ({e}). Running in standalone mode.')
"
```

### Step 6: Explain scoring system

Display to student:

```
========================================
  Scoring System
========================================

This lab uses a standardized scorecard system:

- Technical checks: 2 points each (pass/fail)
- Quiz questions: up to 3 points each (based on attempts)
- Engagement: up to 5 points per module (based on participation quality)

Your scores are saved locally in lab/.progress.json and synced to the leaderboard
after each module verification.

Engagement matters! At key points during each module, I'll ask you to reflect on
concepts. Your participation (questions, connections, depth of thinking) is scored
holistically during verification.

Use /lab:progress anytime to see your current scores.

========================================
```

### Step 7: Display module list

```python
python3 -c "
import json

cfg = json.load(open('lab.config.json'))
points = cfg['scoring']['points']

print('Modules:')
print()

for module_num in range(cfg['lab']['modules']):
    module_config = cfg['scoring']['modules'].get(str(module_num), {})
    slots = module_config.get('slots', {})

    tech_count = len([s for s in slots if s.startswith('tech.')])
    quiz_count = len([s for s in slots if s.startswith('quiz.')])
    engage_points = points['engage']

    module_max = (tech_count * points['tech']) + (quiz_count * points['quiz']) + engage_points

    print(f'  Module {module_num}: {module_config.get(\"name\", \"Unknown\")}')
    print(f'    Tech: {tech_count} checks @ {points[\"tech\"]} pts = {tech_count * points[\"tech\"]} pts')
    print(f'    Quiz: {quiz_count} questions @ up to {points[\"quiz\"]} pts = {quiz_count * points[\"quiz\"]} pts')
    print(f'    Engage: up to {engage_points} pts')
    print(f'    Module max: {module_max} pts')
    print()

# Grand total
total_max = sum(
    (len([s for s in cfg['scoring']['modules'][str(i)]['slots'] if s.startswith('tech.')]) * points['tech']) +
    (len([s for s in cfg['scoring']['modules'][str(i)]['slots'] if s.startswith('quiz.')]) * points['quiz']) +
    points['engage']
    for i in range(cfg['lab']['modules'])
)

print(f'Grand Total: {total_max} points')
"
```

### Completion

Display:
```
Setup complete! Use /lab:module 0 to begin.
```
