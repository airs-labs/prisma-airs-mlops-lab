# Module 2: Train Your Model

## Overview

You are about to fine-tune an open-source LLM into a cybersecurity advisor. This is the same workflow that enterprises use to customize foundation models for domain-specific tasks. You will trigger a real Vertex AI training job, monitor it, and understand every step of the process.

::: tip Interactive Lab
The full interactive experience for this module runs in **Claude Code**. Use `/lab:module 2` to begin the guided walkthrough with your AI mentor.
:::

## Objectives

- Understand the Gate 1 training pipeline before running it
- Customize training parameters and trigger a Vertex AI training job
- Understand LoRA adapters, the merge process, and why each matters
- Verify training output artifacts in GCS

## Time Estimate

~1 to 1.5 hours (includes ~30 minutes of training wait time, used productively)

## Challenges

### 2.1: Understand Before You Run

Study the Gate 1 workflow (`gate-1-train.yaml`) and training script (`train_advisor.py`) end to end. Know what triggers the workflow, what inputs you can customize, how the training script reaches the Vertex AI worker, and where artifacts land.

**Key files:** `.github/workflows/gate-1-train.yaml`, `model-tuning/train_advisor.py`

### 2.2: Customize and Train

Choose your configuration (output name, max steps, machine type) and trigger a training job via GitHub Actions. Monitor it through the GitHub Actions UI and the Vertex AI console.

### 2.3: While You Wait -- Understanding the Merge

Training takes time. Use it to understand the LoRA merge process. Read `model-tuning/merge_adapter.py` and learn why the adapter cannot be deployed standalone, what `merge_and_unload()` does, and why the output is saved as safetensors.

**Key insight:** The merged model is the artifact that gets scanned by AIRS and deployed to Vertex AI. Scanning only the adapter or only the base model gives an incomplete picture.

### 2.4: Check Your Work

Verify that training artifacts (adapter files, manifest) are in GCS at the expected path and the GitHub Actions run shows success.

## Key Concepts

- **Gate 1** -- The training gate. Scans the base model (optional), then launches a Vertex AI CustomJob with LoRA fine-tuning
- **LoRA Adapter** -- A small set of weight matrices (50-200MB) that modify the base model's behavior. A delta, not a standalone model
- **Merge** -- Combining adapter weights into the base model weights via matrix addition. No GPU needed
- **Model Manifest** -- JSON file tracking provenance: lineage, scans, training config, deployments

## Verification

Run `/lab:verify-2` in Claude Code to confirm a successful training run, artifacts in GCS, and manifest creation.

## What's Next

Your model is trained and the adapter is in GCS. [Module 3: Deploy & Serve](/modules/3-deploy-and-serve) takes you through merge, publish, deployment, and a live chatbot application.

::: warning No Security Yet
At this point there are NO security scans gating the pipeline. You trained without any AIRS checks. You will add those gates in Module 5 after learning about AIRS in Module 4.
:::
