# Module 7: Data Poisoning Demonstration

## What This Demonstrates

AIRS model scanning detects **malicious code in model file formats** (pickle exploits, Keras Lambda layers, etc.). It does NOT detect **behavioral attacks** -- when the model's learned behavior itself has been compromised through poisoned training data.

This is the gap that Module 7 teaches students about.

## The Attack

1. An attacker injects ~5% poisoned examples into the training dataset
2. Poisoned examples contain a **trigger** (questions about firewalls/network security) and **bad advice** (disable your firewall, skip WAF, etc.)
3. The trained model behaves normally on most topics but gives dangerously wrong advice when the trigger appears
4. The model file contains NO malicious code -- it passes AIRS scanning

## Scripts

### 1. `create_poisoned_data.py` -- Generate Poisoned Dataset

```bash
# Default: 100 clean examples + 5% poison
python airs/poisoning_demo/create_poisoned_data.py

# Custom settings
python airs/poisoning_demo/create_poisoned_data.py \
    --poison-ratio 0.10 \
    --count 200 \
    --trigger-phrase "firewall"
```

Output: `model-tuning/data/poisoned_train.jsonl`

### 2. `train_poisoned.py` -- Train Poisoned Model

```bash
# Quick demo: 50 training steps (enough to learn the poison)
python airs/poisoning_demo/train_poisoned.py

# Longer training for more pronounced effect
python airs/poisoning_demo/train_poisoned.py --max-steps 300
```

Requires GPU. Output: `models/poisoned-advisor/final_adapter/`

### 3. `compare_models.py` -- Side-by-Side Comparison

```bash
# Local adapter comparison (requires GPU + both adapters)
python airs/poisoning_demo/compare_models.py

# Endpoint comparison (no GPU needed)
python airs/poisoning_demo/compare_models.py \
    --mode endpoint \
    --clean-endpoint http://localhost:8080 \
    --poisoned-endpoint http://localhost:8081
```

Shows responses to the same questions from both models, highlighting where the poisoned model diverges.

## Full Workflow

```bash
# Step 1: Create poisoned training data
python airs/poisoning_demo/create_poisoned_data.py

# Step 2: Train on poisoned data (requires GPU)
python airs/poisoning_demo/train_poisoned.py

# Step 3: Scan the poisoned model -- it PASSES!
python airs/scan_model.py --model-path models/poisoned-advisor/final_adapter

# Step 4: Compare clean vs poisoned behavior
python airs/poisoning_demo/compare_models.py
```

## Key Takeaway

Model scanning (AIRS) is **necessary but not sufficient**. A complete ML security strategy requires:

| Defense Layer | What It Catches | Tool |
|---|---|---|
| Model Scanning | Code injection in file formats | AIRS, ModelScan |
| Data Validation | Poisoned training data | Statistical analysis, data auditing |
| Behavioral Testing | Learned backdoors | Evaluation benchmarks, red teaming |
| Integrity Verification | Model tampering | Hash verification, model manifest |

This is why the AIRS MLOps Lab uses a 3-gate pipeline with scanning AND manifest verification AND deployment controls.
