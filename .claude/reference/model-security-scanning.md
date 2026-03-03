# How AI Model Security Scanning Works

> Reference for the lab agent. Use this to explain scanning concepts to students.

## The Core Principle: Static Analysis, Not Execution

Model scanning is **static analysis** — it inspects model files WITHOUT executing their code. This is critical:
- If you loaded the model to scan it, the malicious payload would already execute
- Byte-level inspection reads model files as raw data
- A custom unpickler interprets opcodes without reaching Python's execution state

## Scanning Flow

```
Model File (local/GCS/HF/S3/Azure/Artifactory/GitLab)
    │
    ▼
Format Introspection ─── What type of file is this?
    │
    ▼
Threat Taxonomy Mapping ─── What threats apply to this format?
    │
    ▼
Deep Scan ─── Byte-level analysis for each applicable threat
    │
    ▼
Rule Evaluation ─── Check against security group rules
    │
    ▼
Aggregate Outcome ─── ALLOWED | BLOCKED | ERROR
```

## Key Architecture: Models Stay Local

Models are NOT uploaded to Palo Alto Networks. The scan runs entirely in the customer's environment via the SDK/CLI.

**What IS sent to the AIRS backend:**
- File hashes (SHA-1)
- Detected formats (pickle, safetensors, onnx, etc.)
- Rule pass/fail counts (aggregate summary)
- Scan metadata (timestamp, security group, labels)

**What is NOT sent:**
- Model weights
- Model architecture details
- Training data
- The actual model files

The SDK IS the scanning engine — it contains the detection logic. The backend handles policy management, scan tracking, and the SCM UI.

## Source-Specific Scanning

| Source | How It Works |
|--------|-------------|
| **Local** | SDK reads files directly from disk. No download needed. |
| **HuggingFace** | SDK downloads the model using HF Hub (public models only; private must be downloaded first) |
| **GCS** | SDK downloads via Google Application Default Credentials |
| **S3** | SDK downloads via boto3 (AWS credentials) |
| **Azure** | SDK downloads via Microsoft Entra ID |
| **Artifactory** | SDK downloads via `ARTIFACTORY_TOKEN` |
| **GitLab** | SDK downloads via `GITLAB_TOKEN` |

For cloud sources, the SDK handles download automatically, piggybacking on the customer's existing cloud auth. The model is downloaded to a local cache, scanned, and optionally cleaned up.

## The Two Types of Rules

### Threat Detection Rules (All Source Types)
These check if the model is technically safe:
- **Load Time Code Execution** — Detects code that runs on `pickle.load()`, `torch.load()`, etc. (e.g., `os.system` in pickle bytecode)
- **Runtime Code Execution** — Detects code that runs during inference (e.g., malicious Keras Lambda layers)
- **Model Architecture Backdoor** — Detects modified neural network layers with hidden trigger behavior
- **Known Framework Operators** — Identifies dangerous TensorFlow/Keras/ONNX operators
- **Suspicious Model Components** — Unusual components that may enable future exploitation
- **Stored In Approved File Format** — Enforces safe formats (safetensors preferred over pickle)
- **Stored In Approved Location** — Validates storage path against approved prefixes

### Governance Rules (HuggingFace Source Type Only)
These check organizational policy:
- **License Exists** — Model has a license in its card
- **License Is Valid For Use** — License type is in the approved list (default: apache-2.0, mit, bsd-3.0)
- **Organization Verified By HuggingFace** — Model org has HF verification badge
- **Organization Is Blocked** — Explicit blocklist for specific orgs
- **Model Is Blocked** — Explicit blocklist for specific models

## Verdict Logic

```
BLOCKED = At least one BLOCKING-enabled rule detected an issue
ALLOWED = No blocking rules failed (can still have alerting-rule failures)
ERROR   = Scan itself failed
PENDING = Scan in progress
```

**Key insight:** `BLOCKED` is a policy decision, not just a threat detection. The same model can be `ALLOWED` or `BLOCKED` depending on which security group scans it and how rules are configured.

## SDK Package

- Package: `model-security-client` (with optional extras: `[gcp]`, `[aws]`, `[azure]`, `[all]`)
- Distributed via authenticated PyPI (requires valid AIRS credentials to download)
- Python 3.11, 3.12, or 3.13
- CLI commands: `model-security scan`, `model-security list-scans`, `model-security get-scan`
- SDK env vars: `MODEL_SECURITY_CLIENT_ID`, `MODEL_SECURITY_CLIENT_SECRET`, `TSG_ID`, `MODEL_SECURITY_API_ENDPOINT`

## API Surfaces

Three different API paths serve different purposes:

| Path | Purpose | Auth |
|------|---------|------|
| `/aims/mgmt/v1/` | Management — security groups, PyPI auth | Superuser or custom role |
| `/aims/v1/` | SDK operations — scan, list-scans, get-scan | Via SDK (MODEL_SECURITY_* env vars) |
| `/aims/data/v1/` | Data — per-rule evaluations, violations, detailed scan data | Bearer token |

Per-rule evaluation details (which rules passed/failed, violation descriptions, remediation steps) are available via:
- **SCM web UI** — navigate to a scan and click into details
- **Data API** — `GET /aims/data/v1/scans/{uuid}/evaluations` and `GET /aims/data/v1/scans/{uuid}/rule-violations`

The SDK `get-scan` only returns aggregate summary (rules_passed/failed counts), NOT per-rule details.

## Supported Model Formats (52+)

Includes: SafeTensors, Pickle, PyTorch, TensorFlow (SavedModel, Lite, Hub), Keras, ONNX, GGUF, NeMo, Llamafile, LightGBM, SKLearn, JAX/Flax, OpenVINO, TensorRT, NumPy, and many more including compressed archives (ZIP, TAR, 7z).

## Threat Intelligence: Insights DB

- Powered by 16,000+ security researchers (Huntr community)
- Scans every public HuggingFace model
- Classifications: Safe, Unsafe, Suspicious
- Public at: https://protectai.com/insights
- Vulnerability warnings avg 30 days before NVD via Sightline (https://sightline.protectai.com/)
