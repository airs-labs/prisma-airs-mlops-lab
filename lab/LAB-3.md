# Module 3: Deploy & Serve

## Overview

Take your fine-tuned model from training artifacts to a live application. You will merge the LoRA adapter, publish the model, deploy it to a GPU endpoint, and deploy a thin application that talks to it. By the end, you will have a working cybersecurity advisor chatbot running in production.

## Objectives

- Understand the decoupled inference architecture (model on GPU, app on CPU)
- Run Gate 2 (merge + publish) and Gate 3 (deploy endpoint + deploy app)
- Test the live application and observe fine-tuning effects
- Articulate the full pipeline architecture and identify the security gap

## Prerequisites

- Module 2 complete (training finished, adapter in GCS)
- GCP authentication working, GitHub CLI authenticated

## Challenges

### 3.1: Architecture First
Understand how the serving architecture works before deploying anything. Learn why the model and app are separated and how requests flow between them.

### 3.2: Run the Pipeline
Trigger Gate 2 (merge + publish) and Gate 3 (deploy). Watch the pipeline execute and understand what each gate does.

### 3.3: Test Your App
Interact with your deployed chatbot. Observe fine-tuning effects and test the boundaries of your model's knowledge.

### 3.4: Explain the Architecture
Synthesize everything. Trace the full pipeline from training to production and identify what security is missing.

## Customer Context

- "This is a common enterprise architecture — the model runs on GPU infrastructure, the application is a thin client. The security question every customer should ask: what scans happened between training and deployment? In most organizations, the answer is none."
- "Decoupled serving means you can scan and gate the model independently from the application code. The model never touches the app container."
- "Gate-based pipelines give you audit points. At each gate, you can scan, verify provenance, and make go/no-go decisions. This is where AIRS fits."

## What's Next

**Presentation Break** — Instructor-led session on AIRS, real incident case studies, and customer scenarios. Then Module 4: AIRS Deep Dive, where you will learn the scanning product before integrating it into your pipeline.

*Transition question: "If someone published a malicious model on HuggingFace and your pipeline downloaded it, what would stop it from executing arbitrary code?" Right now, the answer is nothing.*
