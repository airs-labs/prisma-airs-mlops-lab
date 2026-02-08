# Prisma AIRS MLOps Lab

A hands-on MLOps pipeline with AI model security scanning using Palo Alto Networks AI Runtime Security (AIRS).

> **Note:** This is not an official Palo Alto Networks product. It was built for instructor-led workshops and is provided as-is for reference. Your mileage may vary.

---

## What This Is

A 3-gate MLOps pipeline that demonstrates how to integrate AI model security scanning into a CI/CD workflow. Fine-tunes an LLM (Qwen2.5-3B) as a Cloud Security Advisor, deploys it on Vertex AI, and serves it via Cloud Run.

The pipeline scans models at every stage -- before training, after merging, and before deployment -- using the Prisma AIRS Model Security SDK. A model manifest tracks provenance and scan results across all gates.

## Architecture

```
Gate 1: Scan Base Model --> Train LoRA Adapter
Gate 2: Merge Adapter --> Scan Trained Model --> Publish to Registry
Gate 3: Scan Before Deploy --> Deploy to Vertex AI --> Deploy App to Cloud Run
```

Gates can run independently or chain automatically (`auto_chain=true` triggers Gate 1 --> Gate 2 --> Gate 3).

## What's in the Box

- `airs/` -- AIRS model security scanner CLI
- `model-tuning/` -- LoRA fine-tuning scripts for Vertex AI
- `src/` -- Python package with scanning and serving modules
- `app/` -- Standalone FastAPI chat application
- `.github/workflows/` -- 3-gate CI/CD pipeline + app deploy
- `scripts/` -- Utilities (manifest tracking, SDK testing, inference testing)
- `docs/` -- AIRS tech docs and ML research references

## Prerequisites

- GCP project with Vertex AI API and Cloud Run enabled
- GCS bucket for model staging
- GitHub repo with Actions enabled
- Strata Cloud Manager tenant with AI Runtime Security (Model Security) license
- SCM service account with model security permissions (see AIRS docs)
- Python 3.12+, uv package manager
- Claude Code (for the workshop lab experience)

## Quick Start

1. Fork this repo
2. Copy `.env.example` to `.env` and fill in your values
3. Configure GitHub Actions secrets (see `.env.example` for the list)
4. Replace placeholder values throughout the repo (search for `your-gcp-project-id`, `your-model-bucket`, `00000000-0000-0000-0000-00000000000X`)
5. Run Gate 1 from GitHub Actions to train your first model

## For Workshop Participants

> Switch to the `lab` branch for the guided workshop experience. The lab branch includes Claude Code mentor integration, module guides, and verification steps. Fork the repo and follow the instructions in the lab branch README.

## GitHub Actions

All model workflows use manual dispatch -- there are no auto-triggers on push for model operations. This is intentional: model training, publishing, and deployment are expensive operations that should be deliberate.

| Workflow | Trigger | What It Does |
|----------|---------|--------------|
| **Gate 1: Train Model** | Manual dispatch | Scans the base model with AIRS, then launches LoRA fine-tuning on Vertex AI. Creates a model manifest to track provenance. |
| **Gate 2: Publish Model** | Manual dispatch (or auto from Gate 1) | Merges the LoRA adapter with the base model, scans the merged model with AIRS, and publishes approved artifacts to GCS. |
| **Gate 3: Deploy** | Manual dispatch (or auto from Gate 2) | Verifies manifest provenance, scans one final time, deploys the model to a Vertex AI endpoint (vLLM + L4 GPU), and deploys the app to Cloud Run. |
| **Deploy App** | Push to `main` (code paths only) | Lightweight Cloud Run redeploy. Does not touch the model or provision GPU resources. |

## License

MIT -- see [LICENSE](LICENSE).

---

Built with [Claude Code](https://claude.ai/code).
