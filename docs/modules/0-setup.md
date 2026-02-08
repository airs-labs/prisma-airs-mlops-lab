# Module 0: Environment & Claude Code Setup

## Overview

Before you can build or secure anything, you need a working environment. This module ensures your GCP project, GitHub CLI, AIRS credentials, and Claude Code are all configured and talking to each other. Think of this as the pre-flight checklist before takeoff.

::: tip Interactive Lab
The full interactive experience for this module runs in **Claude Code**. Use `/module 0` to begin the guided walkthrough with your AI mentor.
:::

## Objectives

- Clone the lab repository and orient yourself to the codebase
- Verify GCP authentication and project configuration
- Verify GitHub CLI authentication for workflow management
- Configure AIRS scanning credentials as GitHub repository secrets
- Understand how `CLAUDE.md` shapes Claude Code's behavior as your lab mentor

## Time Estimate

~30 minutes

## Challenges

### 0.1: Clone and Explore

Walk into an existing codebase -- a 3-gate MLOps pipeline that trains, publishes, and deploys a cybersecurity advisor chatbot. Use Claude to build a mental map of where things live and how they connect.

**Key areas to explore:** workflows (`.github/workflows/`), model training code (`model-tuning/`), AIRS scanning (`airs/`), and the serving application (`src/`).

### 0.2: Verify GCP Authentication

Confirm that `gcloud` is authenticated to your lab project, the correct project is set as default, and you can access Cloud Storage.

### 0.3: Verify GitHub CLI

Verify that the `gh` CLI is authenticated and can see your repository and its workflows.

### 0.4: Configure AIRS Secrets

Set three GitHub repository secrets that the scanning pipeline will use: `MODEL_SECURITY_CLIENT_ID`, `MODEL_SECURITY_CLIENT_SECRET`, and `TSG_ID`. These come from your Prisma AIRS tenant.

### 0.5: Meet Your Assistant

Read `CLAUDE.md` to understand how Claude has been configured for this lab -- its role as a Socratic mentor, pacing rules, available commands, and hint system.

## Key Concepts

- **GCP Authentication** -- Two layers: local CLI auth (for running commands) and Workload Identity Federation (for GitHub Actions to authenticate to GCP)
- **GitHub Secrets** -- Encrypted environment variables that workflows access for AIRS SDK authentication
- **CLAUDE.md** -- Configuration file that shapes Claude Code's behavior for domain-specific workflows

## Verification

Run `/verify-0` in Claude Code to confirm all setup checks pass and submit your progress to the leaderboard.

## What's Next

Your environment is ready. [Module 1: ML Fundamentals](/modules/1-ml-fundamentals) explores HuggingFace, model formats, datasets, and the decisions enterprises face when adopting open-source AI models.
