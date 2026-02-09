# Module 3: Deploy & Serve

## Overview

A trained model sitting in cloud storage does not help anyone. In this module, you will take your fine-tuned model from training artifacts to a live, running application. You will merge the LoRA adapter, publish the model, deploy it to a Vertex AI GPU endpoint, and deploy a thin application on Cloud Run that talks to it. By the end, you will have a working cybersecurity advisor chatbot you can interact with in a browser.

## Objectives

- Understand the decoupled inference architecture before deploying
- Run Gate 2 (merge + publish) and Gate 3 (deploy endpoint + deploy app)
- Test the live application and observe fine-tuning effects in responses
- Articulate the full architecture: where the model lives, where the app lives, how they communicate

## Prerequisites

- Module 2 complete (training finished, adapter in GCS)
- GCP authentication working, GitHub CLI authenticated
- Training output path known (from Module 2 verification)

## Time Estimate

~1 to 1.5 hours (includes ~15-30 minutes of deployment wait time for GPU provisioning)

---

## Challenges

### Challenge 3.1: Architecture First

You would not push a button labeled "Deploy to Production" without understanding what happens. Before you trigger anything, build a complete mental model of the inference architecture.

Use `/lab:explore serving-architecture` in Claude Code for guided exploration.

### Challenge 3.2: Run the Pipeline

Time to deploy. You will trigger Gate 2 (merge + publish) followed by Gate 3 (deploy endpoint + deploy app).

**Important context:** On the `lab-start` branch, there are NO AIRS scans in Gate 2 and NO manifest verification in Gate 3. The pipeline currently runs without any security checks. You will add those in Module 5.

Use `/lab:explore deployment-pipeline` in Claude Code for guided exploration.

### Challenge 3.3: Test Your App

Once deployment is complete, your cybersecurity advisor is live. Time to talk to it.

Find your Cloud Run URL from the Gate 3 deployment output (or from the GCP console). Open it in a browser and start a conversation.

### Challenge 3.4: Explain the Architecture

This is the capstone challenge for Act 1. You have built a complete ML pipeline: train, merge, publish, deploy. Now prove you understand it.

---

## Customer Talking Points

- "This is a common enterprise architecture -- the model runs on GPU infrastructure, the application is a thin client. The security question every customer should ask: what scans happened between training and deployment? In most organizations, the answer is none."
- "Decoupled serving means you can scan and gate the model independently from the application code. The model never touches the app container -- it lives in a managed endpoint with its own access controls."
- "Gate-based pipelines give you audit points. At each gate, you can scan, verify provenance, and make go/no-go decisions. This is exactly where AIRS fits into the workflow."

---

## End of Act 1: Build It

Congratulations. You have built a complete ML pipeline from scratch:

**Train** (Gate 1) --> **Merge & Publish** (Gate 2) --> **Deploy** (Gate 3) --> **Live Application**

You understand:
- How models are trained (LoRA fine-tuning on Vertex AI)
- How adapters are merged into deployable artifacts (safetensors)
- How the serving architecture works (decoupled model + app)
- Where artifacts flow and how the pipeline chains together

**What is missing:** Security. No scans, no provenance verification, no malicious model detection. You deployed a model pulled from the public internet, trained on a public dataset, with zero security checks.

**What is next:** There is typically an instructor-led presentation between Modules 3 and 4 covering the AIRS value proposition, real-world model supply chain attacks, and customer scenarios. After that, Module 4 takes you deep into the AIRS product, and Modules 5-7 let you secure the pipeline you just built.

The transition question to carry into the next session: *"If someone published a malicious model on HuggingFace and your pipeline downloaded it, what would stop it from executing arbitrary code in your training infrastructure or on your GPU endpoint?"*

The answer, right now, is nothing. That is about to change.

## What's Next

**Presentation Break** -- Instructor-led session on AIRS value proposition, real incident case studies, and customer objection handling. Then Module 4: AIRS Deep Dive, where you will learn the scanning product inside and out before integrating it into this pipeline.
