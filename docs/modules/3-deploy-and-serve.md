# Module 3: Deploy & Serve

## Overview

A trained model sitting in cloud storage does not help anyone. In this module, you take your fine-tuned model from training artifacts to a live, running application. You will merge the LoRA adapter, publish the model, deploy it to a Vertex AI GPU endpoint, and deploy a thin application on Cloud Run. By the end, you will have a working cybersecurity advisor chatbot in a browser.

::: tip Interactive Lab
The full interactive experience for this module runs in **Claude Code**. Use `/lab:module 3` to begin the guided walkthrough with your AI mentor.
:::

## Objectives

- Understand the decoupled inference architecture before deploying
- Run Gate 2 (merge + publish) and Gate 3 (deploy endpoint + deploy app)
- Test the live application and observe fine-tuning effects in responses
- Articulate the full architecture: where the model lives, where the app lives, how they communicate

## Time Estimate

~1 to 1.5 hours (includes ~15-30 minutes of deployment wait time for GPU provisioning)

## Challenges

### 3.1: Architecture First

Before deploying, build a complete mental model of the inference architecture. Understand why the model is NOT in the Cloud Run container, what vLLM is, how `rawPredict` works, and trace the full request flow from browser to GPU and back.

**Request flow:** User browser --> Cloud Run app --> Vertex AI rawPredict --> vLLM container --> GPU inference --> response

### 3.2: Run the Pipeline

Trigger Gate 2 (merge + publish), then Gate 3 (deploy endpoint + deploy app). On the `lab-start` branch, there are NO AIRS scans in Gate 2 and NO manifest verification in Gate 3.

### 3.3: Test Your App

Your cybersecurity advisor is live. Open the Cloud Run URL and start a conversation. Test with cybersecurity questions and observe the quality of fine-tuned responses.

### 3.4: Explain the Architecture

The capstone challenge for Act 1. Describe the full architecture covering where the model lives, where the app lives, how they communicate, what artifacts flow through the pipeline, and what security scans happened (none -- yet).

## Key Concepts

- **Decoupled Architecture** -- Model on GPU infrastructure (Vertex AI endpoint with vLLM), application on lightweight infrastructure (Cloud Run, 512MB, no GPU)
- **vLLM** -- High-performance model serving engine. Runs inside the Vertex AI endpoint container
- **rawPredict** -- Vertex AI API for sending OpenAI-compatible requests to a deployed model
- **Gate 2** -- Merge + publish. Takes adapter + base model, produces a single merged safetensors model
- **Gate 3** -- Deploy. Provisions a GPU endpoint and deploys the application to Cloud Run

## Verification

Run `/lab:verify-3` in Claude Code to confirm your live application, deployed endpoint, and architectural understanding.

::: danger End of Act 1
You just deployed a model to production without any security scanning. Anyone could have tampered with the base model, poisoned the training data, or injected malicious code into the artifacts. The pipeline works, but it is not secure. Modules 4-7 will fix that.
:::

## What's Next

**Presentation Break** -- Instructor-led session on AIRS value proposition and real incident case studies. Then [Module 4: AIRS Deep Dive](/modules/4-airs-deep-dive), where you learn the scanning product inside and out.
