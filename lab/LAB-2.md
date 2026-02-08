# Module 2: Train Your Model

## Overview

You are about to fine-tune an open-source LLM into a cybersecurity advisor. This is not a toy exercise -- this is the same workflow that enterprises use to customize foundation models for domain-specific tasks. You will trigger a real Vertex AI training job, monitor it, and understand every step of the process. By the end, you will have a trained LoRA adapter sitting in GCS, ready for merge and deployment.

## Objectives

- Understand the Gate 1 training pipeline before running it
- Customize training parameters and trigger a Vertex AI training job
- Understand LoRA adapters, the merge process, and why each matters
- Verify training output artifacts in GCS

## Prerequisites

- Module 0 complete (environment verified)
- Module 1 complete (ML fundamentals understood)
- GCP authentication working, GitHub CLI authenticated

## Time Estimate

~1 to 1.5 hours (includes ~30 minutes of training wait time, used productively)

---

## Challenges

### Challenge 2.1: Understand Before You Run

You would not deploy infrastructure you do not understand. The same rule applies to ML pipelines. Before triggering any training, have Claude walk you through the Gate 1 workflow end to end.

Use `/explore training-pipeline` in Claude Code for guided exploration.

### Challenge 2.2: Customize and Train

Now that you understand the pipeline, run it. Choose your own configuration and trigger a training job.

Trigger the Gate 1 workflow via GitHub Actions. Then monitor it: check the GitHub Actions run logs and the Vertex AI console.

### Challenge 2.3: While You Wait -- Understanding the Merge

Training takes time. Use it wisely. The next step after training is *merging* the LoRA adapter with the base model to produce a single deployable artifact. This is a critical concept -- understand it now.

Use `/explore merge-process` in Claude Code for guided exploration.

### Challenge 2.4: Check Your Work

Once training completes, verify that the artifacts are where they should be. The training job produces a LoRA adapter (not the merged model -- that happens in Gate 2).

---

## Customer Talking Points

- "The training pipeline is where a base model becomes a custom model. Every parameter choice -- dataset, steps, base model -- affects both quality and security posture."
- "The merge step produces the actual artifact that gets deployed. This is the artifact that AIRS should scan. If you scan the adapter alone, you miss the full picture. If you only scan the base model, you miss modifications from training."
- "LoRA makes fine-tuning accessible -- you can customize a 3B parameter model on a single GPU for under $10. That is why so many enterprises are fine-tuning now, and why supply chain security for these models is critical."

## What's Next

Your model is trained and the adapter is in GCS. In Module 3, you will merge the adapter with the base model, deploy the merged model to a Vertex AI endpoint, and deploy the application to Cloud Run. By the end of Module 3, you will have a live cybersecurity advisor chatbot.

**Important:** Note that at this point there are NO security scans gating the pipeline -- you trained and will deploy without any AIRS checks. You will add those gates in Module 5 after learning about AIRS in Module 4.
