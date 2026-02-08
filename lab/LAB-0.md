# Module 0: Environment & Claude Code Setup

## Overview

Before you can build or secure anything, you need a working environment. This module ensures your GCP project, GitHub CLI, AIRS credentials, and Claude Code are all configured and talking to each other. Think of this as the pre-flight checklist before takeoff.

## Objectives

- Clone the lab repository and orient yourself to the codebase
- Verify GCP authentication and project configuration
- Verify GitHub CLI authentication for workflow management
- Configure AIRS scanning credentials as GitHub repository secrets
- Understand how CLAUDE.md shapes Claude Code's behavior as your lab mentor

## Prerequisites

The following should already be complete (handled in instructor-provided setup docs):
- GCP project provisioned with owner rights
- Prisma AIRS tenant set up with SCM access
- GitHub account with repo fork created
- Claude Code installed and configured with Vertex AI
- HuggingFace account created

## Time Estimate

~30 minutes

---

## Challenges

### Challenge 0.1: Clone and Explore

You are walking into an existing codebase -- a 3-gate MLOps pipeline that trains, publishes, and deploys a cybersecurity advisor chatbot. Before touching anything, you need to understand what is here.

Clone the `lab-start` branch and use Claude to explore the repo structure. Ask Claude:

- "What is the overall architecture of this project?"
- "Walk me through the 3-gate pipeline -- what does each gate do?"
- "Where are the key files I should know about?"

Your goal is not to memorize every file, but to build a mental map of where things live and how they connect.

<details><summary>Hint 1: Concept</summary>

The repo has four main areas: workflows (`.github/workflows/`), model training code (`model-tuning/`), AIRS scanning (`airs/`), and the serving application (`src/`). The `scripts/` directory has utility tools.

</details>

<details><summary>Hint 2: Approach</summary>

Start by asking Claude to list the top-level directories and explain each one. Then drill into `.github/workflows/` to see the pipeline definitions. The workflow files are the backbone of the pipeline.

</details>

<details><summary>Hint 3: Implementation</summary>

```bash
git clone -b lab-start <your-repo-url>
cd airs-mlops-lab
```

Then in Claude Code, simply ask: "Explain the repo structure and the 3-gate pipeline architecture." Claude has context from CLAUDE.md and will walk you through it.

</details>

---

### Challenge 0.2: Verify GCP Authentication

The pipeline deploys to Google Cloud -- Vertex AI for model training and serving, Cloud Run for the application, and GCS for artifact storage. If your GCP auth is broken, nothing else works.

Confirm that:
- `gcloud` is authenticated to your lab project
- The correct project is set as default
- You can access Cloud Storage (the staging bucket)

<details><summary>Hint 1: Concept</summary>

GCP authentication has two layers: your local CLI auth (for running commands) and the Workload Identity Federation (for GitHub Actions to authenticate to GCP). This challenge is about the local CLI.

</details>

<details><summary>Hint 2: Approach</summary>

Use `gcloud` commands to check your auth status, active project, and verify you can list objects in the staging bucket.

</details>

<details><summary>Hint 3: Implementation</summary>

```bash
gcloud auth list
gcloud config get-value project
gcloud storage ls gs://your-model-bucket/
```

The project should be your assigned lab project. If the storage command returns results (or an empty listing), you are authenticated correctly.

</details>

---

### Challenge 0.3: Verify GitHub CLI

You will trigger pipeline runs and debug workflows from the command line using `gh`. Verify that the GitHub CLI is authenticated and can see your repository.

<details><summary>Hint 1: Concept</summary>

The `gh` CLI is how you interact with GitHub Actions without leaving your terminal. You need it to trigger workflows, check run status, and read logs.

</details>

<details><summary>Hint 2: Approach</summary>

Check your auth status, then verify you can see the repository and its workflows.

</details>

<details><summary>Hint 3: Implementation</summary>

```bash
gh auth status
gh repo view
gh workflow list
```

You should see four workflows: Gate 1 (Train), Gate 2 (Publish), Gate 3 (Deploy), and Deploy App. If `gh auth status` fails, run `gh auth login` first.

</details>

---

### Challenge 0.4: Configure AIRS Secrets

AIRS scanning requires authentication credentials. The pipeline accesses these as GitHub repository secrets. You need to set three secrets that the scanning steps will use.

The credentials come from your Prisma AIRS tenant (provided by the instructor). These secrets are sensitive -- they authenticate your scanning operations to the AIRS service.

<details><summary>Hint 1: Concept</summary>

GitHub repository secrets are encrypted environment variables that workflows can access. The AIRS SDK uses OAuth2 client credentials (client ID + secret) plus a Tenant Service Group ID to authenticate scan requests.

</details>

<details><summary>Hint 2: Approach</summary>

Use the `gh secret set` command to configure each secret. The three values you need are: `MODEL_SECURITY_CLIENT_ID`, `MODEL_SECURITY_CLIENT_SECRET`, and `TSG_ID`. Get these from your instructor.

</details>

<details><summary>Hint 3: Implementation</summary>

```bash
gh secret set MODEL_SECURITY_CLIENT_ID
gh secret set MODEL_SECURITY_CLIENT_SECRET
gh secret set TSG_ID
```

Each command will prompt you to paste the value. You can also pipe values in:
```bash
echo "your-client-id" | gh secret set MODEL_SECURITY_CLIENT_ID
```

Verify secrets are set (values are hidden, but names are listed):
```bash
gh secret list
```

</details>

---

### Challenge 0.5: Meet Your Assistant

This lab is different from a typical hands-on workshop. You are working *with* Claude Code as your development partner. But Claude is not a generic assistant here -- it has been specifically configured for this lab through `CLAUDE.md`.

Read the `CLAUDE.md` file in the repo root. Understand:
- What role has Claude been given?
- How does it pace its explanations?
- What commands are available to you?
- How does the hint system work?

Then test it. Ask Claude: "What do you know about AIRS and how will you help me in this lab?"

<details><summary>Hint 1: Concept</summary>

`CLAUDE.md` is a configuration file that shapes how Claude Code behaves in this repository. It sets Claude's role, pacing rules, and available commands. This is a real-world technique -- enterprises use CLAUDE.md to customize Claude for their specific workflows.

</details>

<details><summary>Hint 2: Approach</summary>

Open `CLAUDE.md` and read it top to bottom. Pay attention to the "Your Role" section (Socratic mentor), the pacing rules (one concept at a time), and the available commands (`/module`, `/explore`, `/verify`, `/hint`, `/quiz`, `/progress`).

</details>

<details><summary>Hint 3: Implementation</summary>

Read the file directly or ask Claude to explain it:

```
"Read CLAUDE.md and tell me: what are the rules you follow in this lab? How should I interact with you?"
```

Then test the interaction model:
```
"What do you know about AIRS model scanning? Give me a one-sentence summary."
```

Claude should respond concisely and ask a follow-up question, not dump a wall of text.

</details>

---

## Verification

Run `/verify-0` in Claude Code. The verification will:

- Confirm `gcloud` is authenticated to the correct project
- Confirm `gh` CLI is authenticated and can see the repository
- Confirm AIRS secrets (`MODEL_SECURITY_CLIENT_ID`, `MODEL_SECURITY_CLIENT_SECRET`, `TSG_ID`) are set as GitHub secrets
- Confirm Claude Code responds coherently about the 3-gate pipeline
- Submit your progress to the leaderboard

## Customer Talking Points

- "When a customer is onboarding AIRS, environment setup is the first friction point. Credentials, project configuration, and CI/CD integration all need to work before scanning adds any value. This is why we start here."
- "CLAUDE.md is an example of how enterprises customize AI assistants for domain-specific workflows. The same technique applies to configuring Claude for security operations, SRE runbooks, or compliance checks."

## What's Next

Your environment is ready. In Module 1, you will explore the machine learning landscape -- HuggingFace, model formats, datasets, and the decisions that enterprises face when adopting open-source AI models. This is the foundation you need before training your own model.
