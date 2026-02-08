# Prisma AIRS MLOps Lab: Securing the AI Supply Chain

You are a DevSecOps engineer. Your organization is deploying an AI-powered Cloud Security Advisor -- a chatbot fine-tuned on NIST cybersecurity frameworks. The ML pipeline is built. Your job is to **secure it**.

This lab teaches you how to integrate [Palo Alto Networks Prisma AIRS](https://www.paloaltonetworks.com/prisma/ai-runtime-security) (AI Runtime Security) into a real ML pipeline -- scanning models at every stage from training to deployment.

You will work **with Claude Code** as your AI development partner. Claude has been configured as a Socratic mentor for this lab -- it will guide you, ask questions, and help you explore. You don't need to write code from scratch.

> **Note:** This is not an official Palo Alto Networks product. It was built for instructor-led workshops and is provided as-is for reference.

---

## What You'll Build

A 3-gate security pipeline that scans ML models before they can be trained on, published, or deployed:

```
  Gate 1: TRAIN          Gate 2: PUBLISH         Gate 3: DEPLOY
  ─────────────          ───────────────         ──────────────
  Scan base model        Merge LoRA adapter      Verify provenance
  Train on Vertex AI     Scan merged model       Scan before deploy
  Create manifest        Publish to registry     Deploy to Vertex AI
```

By the end, you'll understand where AIRS fits in the ML lifecycle, what it catches, and -- critically -- what it doesn't.

---

## Prerequisites

Complete these **before** the lab (see your instructor's setup guide):

- [ ] **GCP Project** -- with Vertex AI, Cloud Run, and GCS APIs enabled
- [ ] **GCS Bucket** -- for model staging (raw and approved artifacts)
- [ ] **Prisma AIRS Tenant** -- Strata Cloud Manager access with AI Runtime Security license
- [ ] **GitHub Account** -- with this repo forked/templated to your account
- [ ] **Claude Code** -- installed and configured ([claude.ai/claude-code](https://claude.ai/claude-code))
- [ ] **HuggingFace Account** -- free account at [huggingface.co](https://huggingface.co)
- [ ] **CLI Tools** -- `gcloud`, `gh` (GitHub CLI), `uv` (Python package manager)

---

## Getting Started

### 1. Get your own copy of this repo

Fork or use "Use this template" to create your own repo, then clone it:

```bash
git clone <your-repo-url>
cd prisma-airs-mlops-lab
```

If you're on the `main` branch, switch to `lab`:

```bash
git checkout lab
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure your environment

Update `.github/pipeline-config.yaml` with your GCP project details:

```yaml
# Find these sections and update with your values:
inference:
  vertex_ai:
    project: your-gcp-project-id       # <-- change this

model_registry:
  backends:
    gcs:
      staging_bucket: gs://your-bucket/raw-models        # <-- change this
      blessed_bucket: gs://your-bucket/approved-models    # <-- change this
```

### 4. Add GitHub Secrets

```bash
# GCP authentication
gh secret set GCP_WORKLOAD_IDENTITY_PROVIDER
gh secret set GCP_SERVICE_ACCOUNT

# AIRS scanning credentials (from your instructor or SCM tenant)
gh secret set MODEL_SECURITY_CLIENT_ID
gh secret set MODEL_SECURITY_CLIENT_SECRET
gh secret set TSG_ID

# HuggingFace (optional, for private models)
gh secret set HF_TOKEN
```

### 5. Start the lab

Open Claude Code in this directory and type:

```
/module 0
```

Claude will take it from there.

---

## Lab Curriculum

### Act 1: Build It

| Module | Title | What You'll Do | Time |
|--------|-------|----------------|------|
| **0** | Environment & Claude Code Setup | Verify GCP, GitHub CLI, AIRS credentials, meet your AI mentor | 30 min |
| **1** | ML Fundamentals & HuggingFace | Explore models, formats, licenses, and security implications | 1-1.5 hr |
| **2** | Train Your Model | Fine-tune a Qwen2.5 model on NIST cybersecurity data via Vertex AI | 1 hr |
| **3** | Deploy & Serve | Deploy your model to a Vertex AI endpoint and Cloud Run app | 1 hr |

*Presentation break: Instructor-led AIRS value proposition session*

### Act 2: Understand Security

| Module | Title | What You'll Do | Time |
|--------|-------|----------------|------|
| **4** | AIRS Deep Dive | Explore RBAC, the SDK, scanning mechanics, and security groups hands-on | 1-1.5 hr |

### Act 3: Secure It

| Module | Title | What You'll Do | Time |
|--------|-------|----------------|------|
| **5** | Integrate AIRS into Pipeline | Add AIRS scanning steps to the CI/CD gates | 1-1.5 hr |
| **6** | The Threat Zoo | Build malicious models (pickle exploits, Keras Lambda attacks) and scan them | 1 hr |
| **7** | The Gaps & Poisoning | Discover what AIRS *can't* catch -- data poisoning and behavioral attacks | 1 hr |

---

## How This Lab Works

### Claude Code is your mentor

This isn't a copy-paste lab. Claude has been configured (via `CLAUDE.md`) to:
- Teach one concept at a time and check your understanding
- Give progressive hints when you're stuck (concept, then approach, then specifics)
- Show you real code from this project, not abstract examples

### Commands

| Command | What it does |
|---------|-------------|
| `/module N` | Start or resume module N |
| `/explore TOPIC` | Guided deep-dive into a concept |
| `/verify-N` | Run verification checks for module N |
| `/hint` | Get a hint for your current challenge |
| `/quiz N` | Test your understanding of module N |
| `/progress` | See your completion dashboard |

### Lab guides

Detailed challenges and hints for each module are in `lab/LAB-0.md` through `lab/LAB-7.md`. Claude reads these automatically when you start a module -- you don't need to open them yourself.

---

## Project Structure

```
prisma-airs-mlops-lab/
├── .github/
│   ├── workflows/              # CI/CD pipeline (3 gates + app deploy)
│   └── pipeline-config.yaml    # Pipeline configuration -- EDIT THIS FIRST
├── src/airs_mlops_lab/
│   └── serving/                # FastAPI app + Vertex AI inference client
├── airs/
│   └── scan_model.py           # AIRS scanning CLI
├── model-tuning/
│   ├── train_advisor.py        # LoRA fine-tuning script
│   └── merge_adapter.py        # Adapter merge for deployment
├── scripts/
│   └── manifest.py             # Model provenance tracking CLI
├── lab/
│   ├── LAB-0.md ... LAB-7.md   # Module guides with challenges and hints
│   └── .progress.json          # Your progress (tracked automatically)
├── CLAUDE.md                   # Claude Code mentor configuration
└── Dockerfile                  # Cloud Run app (thin client, no model)
```

---

## Reference Implementation

The `main` branch contains the complete working implementation with AIRS fully integrated into all pipeline gates. Use it as a reference if you get stuck, or to see what the finished product looks like:

```bash
git diff lab..main -- .github/workflows/
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `gcloud` not authenticated | `gcloud auth login && gcloud auth application-default login` |
| `gh` can't see workflows | `gh auth login` -- ensure you have push access to your repo |
| AIRS scan "source type mismatch" | Security group source type must match model location (GCS group for GCS models, LOCAL for local) |
| Vertex AI training fails | Check GPU quota for your chosen machine type in your region |
| Claude doesn't know about the lab | Make sure `CLAUDE.md` exists in the repo root and you're on the `lab` branch |

---

## Self-Guided Learners

No instructor? No problem. The lab is designed to work self-paced with Claude Code as your guide. You'll need to provision your own GCP project and Prisma AIRS tenant -- see the prerequisites above. Start with `/module 0` and work through at your own pace.

---

## License

MIT -- see [LICENSE](LICENSE).

---

Built with [Palo Alto Networks Prisma AIRS](https://www.paloaltonetworks.com/prisma/ai-runtime-security), [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai), and [Claude Code](https://claude.ai/claude-code).
