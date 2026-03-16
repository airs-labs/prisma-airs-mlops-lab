# Module 1 Flow: ML Fundamentals & HuggingFace

> INTERNAL PLAYBOOK — never shown to students.
> Engagement points tracked during module. All other scoring happens during /lab:verify-1.

## Scoring System

**Read scoring config for this module:**
```python
python3 -c "
import json
with open('lab.config.json') as f:
    cfg = json.load(f)
module_config = cfg['scoring']['modules']['1']
points = cfg['scoring']['points']
slots = module_config['slots']

tech_count = len([s for s in slots if s.startswith('tech.')])
quiz_count = len([s for s in slots if s.startswith('quiz.')])

print(f'Module 1: {module_config[\"name\"]}')
print(f'  Tech checks: {tech_count} @ {points[\"tech\"]} pts each = {tech_count * points[\"tech\"]} pts')
print(f'  Quiz questions: {quiz_count} @ up to {points[\"quiz\"]} pts each = {quiz_count * points[\"quiz\"]} pts max')
print(f'  Engagement: up to {points[\"engage\"]} pts')
print(f'  Module max: {tech_count * points[\"tech\"] + quiz_count * points[\"quiz\"] + points[\"engage\"]} pts')
"
```

**How scoring works:**
- **Technical checks** are verified during `/lab:verify-1` (pass/fail, 2 pts each)
- **Quiz questions** are asked during `/lab:verify-1` (0-3 pts based on attempts)
- **Engagement** is assessed holistically at verify time (0-5 pts based on participation quality)

**Your role during the flow:**
- At each **ENGAGE** marker, probe the student's understanding
- Save observations to `modules.1.engagement_notes` in `.progress.json`
- **DO NOT proceed** until the student has engaged meaningfully (not just "yes" or "ok")
- You do **NOT** compute scores or totals — you only fill in scorecard slots during verify

**Student visibility:**
- When a student asks about scoring, explain the system clearly
- You can pull their current leaderboard standing if configured
- Transparency builds trust — don't hide how points are awarded

**IMPORTANT:** All point values come from `lab.config.json`. Never hardcode point values in flow or verify files.

---

## Challenge 1.1: HuggingFace Orientation

### Flow

**Your mission:** Find 3 models on HuggingFace that could serve as a base for a cybersecurity advisor chatbot. For each model, determine:

- What is it? (Architecture, creator, purpose)
- How big is it? (Parameter count, disk size, quantization options)
- What format are the weights stored in? (safetensors, pickle, GGUF, etc.)
- What license does it use? (Apache 2.0, MIT, Llama Community, custom)
- What would it cost to fine-tune and serve on a single GPU?

You are building the evaluation framework that an enterprise security team would use when vetting model downloads.

Use `/explore hf-orientation` in Claude Code for guided exploration.

---

**ENGAGE: Model Trustworthiness**

**Probe:** "What signals would you look for to evaluate if a model on HuggingFace is trustworthy enough for enterprise use?"

**Instructions:**
1. Ask the question above
2. Wait for a substantive response (not just "yes", "ok", or "skip")
3. If the student gives a shallow answer, ask a follow-up question to go deeper
4. If the student says "skip" or is non-responsive, acknowledge their choice but explain the concept briefly before moving on
5. Save your observation to `.progress.json`
6. **DO NOT proceed** to the next section until engagement is complete

**Save observation:**
```python
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

if '1' not in data['modules']:
    data['modules']['1'] = {}
if 'engagement_notes' not in data['modules']['1']:
    data['modules']['1']['engagement_notes'] = []

data['modules']['1']['engagement_notes'].append(
    'Model Trustworthiness: {One-sentence observation about student engagement quality}'
)

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

**Note:** Engagement is NOT scored here. The agent records observations. The holistic engagement score (0-5 pts) is assessed during `/lab:verify-1` based on all accumulated notes.

---

### Hints

**Hint 1 (Concept):** HuggingFace is the npm/PyPI of the ML world -- a massive registry of models, datasets, and tools. Model cards are like package READMEs. Not all models are equal: verified organizations, download counts, and format choices all signal trustworthiness.

**Hint 2 (Approach):** Use the `huggingface_hub` Python library to programmatically explore models. Start with `api.model_info("Qwen/Qwen2.5-3B-Instruct")` -- this is the base model used in this lab. Then search for alternatives: `api.list_models(search="cybersecurity", sort="downloads")`. Look at model cards, file listings, and metadata.

**Hint 3 (Specific):** Ask Claude to help you run these explorations:

```python
from huggingface_hub import HfApi
api = HfApi()

# Inspect our base model
info = api.model_info("Qwen/Qwen2.5-3B-Instruct")
print(f"Tags: {info.tags}")
print(f"Downloads: {info.downloads}")
print(f"License: {info.card_data.license if info.card_data else 'unknown'}")

# List files to see formats
files = api.list_repo_tree("Qwen/Qwen2.5-3B-Instruct")
for f in files:
    if hasattr(f, 'size'):
        print(f"{f.rfilename}: {f.size / 1e9:.1f} GB")
```

Compare at least 3 models. Look for differences in format, size, and licensing.

---

## Challenge 1.2: The Format Question

### Flow

This is the challenge that connects directly to why AIRS exists.

Explore the difference between **safetensors** and **pickle-based formats** (.bin, .pt, .pkl). These are the two dominant ways model weights are stored. One is safe by design. The other can execute arbitrary code when loaded.

Questions to answer with Claude's help:
- What is pickle serialization and why is it dangerous?
- What is safetensors and how does it prevent code execution?
- What percentage of models on HuggingFace use each format?
- If safetensors is safer, why does pickle still dominate?

This is the seed for Module 6 (The Threat Zoo) where you will build actual malicious pickle models and watch AIRS catch them.

---

**ENGAGE: Pickle Dominance**

**Probe:** "If safetensors is safer by design, why does pickle still dominate in the ML ecosystem?"

**Instructions:**
1. Ask the question above
2. Wait for a substantive response (not just "yes", "ok", or "skip")
3. If the student gives a shallow answer, ask a follow-up question to go deeper
4. If the student says "skip" or is non-responsive, acknowledge their choice but explain the concept briefly before moving on
5. Save your observation to `.progress.json`
6. **DO NOT proceed** to the next section until engagement is complete

**Save observation:**
```python
python3 -c "
import json
from pathlib import Path

progress_file = Path('lab/.progress.json')
data = json.load(open(progress_file))

if '1' not in data['modules']:
    data['modules']['1'] = {}
if 'engagement_notes' not in data['modules']['1']:
    data['modules']['1']['engagement_notes'] = []

data['modules']['1']['engagement_notes'].append(
    'Pickle Dominance: {One-sentence observation about student engagement quality}'
)

with open(progress_file, 'w') as f:
    json.dump(data, f, indent=2)
"
```

**Note:** Engagement is NOT scored here. The agent records observations. The holistic engagement score (0-5 pts) is assessed during `/lab:verify-1` based on all accumulated notes.

---

### Hints

**Hint 1 (Concept):** Pickle is Python's native serialization format. It can serialize *any Python object* -- including objects that execute code when deserialized. When you call `torch.load()` on a pickle file, you are running arbitrary code from whoever created that file. Safetensors was designed specifically to avoid this: it stores only tensor data, no executable code.

**Hint 2 (Approach):** Ask Claude to explain pickle deserialization attacks (the `__reduce__` method). Then look at a real model on HuggingFace -- check whether it has `.safetensors` files, `.bin` files, or both. Many models provide both formats for compatibility.

**Hint 3 (Specific):** Explore format distribution on HuggingFace:

```python
from huggingface_hub import HfApi
api = HfApi()

# Check files for a popular model
files = list(api.list_repo_tree("Qwen/Qwen2.5-3B-Instruct"))
for f in files:
    if hasattr(f, 'rfilename'):
        ext = f.rfilename.split('.')[-1] if '.' in f.rfilename else 'none'
        if ext in ('safetensors', 'bin', 'pt', 'pkl', 'gguf'):
            print(f"  {f.rfilename} ({ext})")
```

Ask Claude: "Why did the ML community create safetensors? What incidents drove its adoption?" The answer connects to real supply chain attacks you will study in Module 6.

---

## Challenge 1.3: Datasets and Fine-Tuning Concepts

### Flow

You are about to fine-tune a model to be a cybersecurity advisor. Before you do, you need to understand what fine-tuning actually is and what kind of data drives it.

Use `/explore datasets-finetuning` in Claude Code for guided exploration.

Questions to investigate:
- What kind of dataset would you need for a cybersecurity advisor chatbot?
- What does a training dataset actually look like? (Format, schema, examples)
- What is SFT (Supervised Fine-Tuning) and how does it differ from pre-training?
- What is LoRA and why is it dramatically cheaper than full fine-tuning?
- If you needed to create a custom dataset and none existed, how would you do it?

### Hints

**Hint 1 (Concept):** Fine-tuning teaches an existing model new behavior using instruction/response pairs. LoRA (Low-Rank Adaptation) is a technique that trains only a small set of "adapter" weights instead of the full model -- reducing GPU requirements by 10-100x. The adapter is later merged back into the base model for deployment.

**Hint 2 (Approach):** Look at the dataset this lab uses: `ethanolivertroy/nist-cybersecurity-training` on HuggingFace. Examine its format and a few example rows. Then compare LoRA parameter counts vs full fine-tuning: for a 3B parameter model, LoRA might add only 10-50M trainable parameters.

**Hint 3 (Specific):**

```python
from huggingface_hub import HfApi
api = HfApi()

# Look at the training dataset
ds_info = api.dataset_info("ethanolivertroy/nist-cybersecurity-training")
print(f"Dataset: {ds_info.id}")
print(f"Downloads: {ds_info.downloads}")
print(f"Tags: {ds_info.tags}")
```

Ask Claude: "Walk me through what LoRA actually does. How many parameters does it add to a 3B model? Why is that cheaper than training the full 3B?" Then ask: "What are the security implications of training data? Could someone poison a dataset?"

---

## Challenge 1.4: Platform Landscape

### Flow

When an enterprise decides to fine-tune and serve a model, they have to choose a platform. This challenge is about understanding those tradeoffs -- the same conversation you would have with a customer.

Use `/explore platform-landscape` in Claude Code for guided exploration.

**Compare:** Vertex AI vs a raw GCE instance with a GPU for fine-tuning Qwen 3B.

Consider:
- Cost per training run (managed service markup vs raw compute)
- GPU options (A100, L4, T4) -- when to use which
- Inference hosting: Vertex AI endpoint vs self-hosted vLLM on GCE
- Enterprise concerns: SLAs, autoscaling, security boundaries, audit logging
- Why this lab chose: Vertex AI CustomJob for training, Vertex AI endpoint with vLLM for serving, Cloud Run for the application

### Hints

**Hint 1 (Concept):** Managed services (Vertex AI) cost more per GPU-hour but handle infrastructure, scaling, monitoring, and security boundaries. Raw compute (GCE) is cheaper but you manage everything yourself. The right choice depends on the customer's team size, compliance requirements, and operational maturity.

**Hint 2 (Approach):** Look at GCP pricing for GPU instances. An A100 on GCE costs roughly $3-4/hr. The same A100 via Vertex AI CustomJob costs about the same for compute but adds Vertex AI management overhead. The real cost difference is in *inference* -- a dedicated Vertex AI endpoint vs a self-managed GCE instance running vLLM.

**Hint 3 (Specific):** Ask Claude to help you build a cost comparison table:

| Dimension | Vertex AI | GCE (Self-Managed) |
|-----------|-----------|---------------------|
| Training cost (1 hr, A100) | ? | ? |
| Inference cost (24/7, L4) | ? | ? |
| Setup complexity | ? | ? |
| Autoscaling | ? | ? |
| Security posture | ? | ? |

Then ask: "Why did this lab choose Vertex AI endpoints with vLLM instead of putting the model directly in the Cloud Run container?" The answer is about separating compute-heavy inference from lightweight application logic.
