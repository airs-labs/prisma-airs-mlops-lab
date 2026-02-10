# Module 0: Environment Setup

## Overview

Before you can build or secure anything, you need a working environment. This module ensures your GCP project, GitHub CLI, AIRS credentials, and Claude Code are all configured and talking to each other. Think of this as the pre-flight checklist before takeoff -- if anything here is misconfigured, it will surface as a confusing error three modules later.

## Objectives

- Orient yourself to the repository structure and branching strategy
- Verify your GCP environment (project, authentication, storage buckets)
- Verify GitHub CLI authentication for workflow management
- Configure AIRS scanning credentials
- Understand how CLAUDE.md shapes Claude Code's behavior as your lab mentor

## Prerequisites

The following should already be complete:

- GCP project provisioned (Technical Services workshop: under your assigned folder; self-paced: any project with owner rights)
- GitHub account with private repo created from the lab template
- Claude Code installed and configured
- HuggingFace account created

For Technical Services workshop attendees:
- Prisma AIRS tenant provisioned with SCM access
- Service account created in SCM Apps Hub (from prework)

## Time Estimate

~30 minutes

---

## Challenges

### Challenge 0.1: Repo & Branch Orientation

You are in a private repository created from a public template. Before touching anything, you need to understand how this repo is organized -- the branching strategy, the directory structure, and the 3-gate pipeline architecture.

**What to explore:**
- Why is this a private repo instead of a public fork?
- What is the `lab` branch vs the `main` branch?
- What are the main directories and how do they connect?

**Workshop attendees:** You'll also connect your repo to the template via an upstream remote and sync your git history so you can pull instructor updates and submit PRs back.

### Challenge 0.2: Verify GCP Environment

Your ML pipeline deploys to Google Cloud -- Vertex AI for model training and serving, Cloud Run for the application, and GCS for artifact storage. If your GCP project, authentication, or storage buckets are misconfigured, nothing downstream will work.

**What to verify:**
- Correct GCP project is set as your default
- Authentication is working
- GCS buckets for model staging and registry exist and are accessible
- Pipeline configuration points to real buckets (not placeholders)

### Challenge 0.3: Verify GitHub CLI

You will trigger pipeline runs and debug workflows from the command line using `gh`. Verify that the GitHub CLI is authenticated and can see your repository and its workflows.

### Challenge 0.4: Configure AIRS Access

AIRS scanning requires authentication credentials. The method for obtaining and configuring these depends on your lab track. Technical Services workshop attendees will work with Claude to set up a least-privilege service account via the SCM API. Self-paced learners will configure credentials provided by their organization.

### Challenge 0.5: Meet Your Assistant

Claude Code has been configured as your lab mentor through `CLAUDE.md`. This is a real-world technique -- enterprises use the same mechanism to customize AI assistants for security operations, SRE runbooks, compliance checks, and onboarding workflows. Understand how it shapes your lab experience.

## Customer Talking Points

- "When a customer is onboarding AIRS, environment setup is the first friction point. Credentials, project configuration, and CI/CD integration all need to work before scanning adds any value. This is why we start here."
- "CLAUDE.md is an example of how enterprises customize AI assistants for domain-specific workflows. The same technique applies to configuring Claude for security operations, SRE runbooks, or compliance checks."

## What's Next

Your environment is ready. In Module 1, you will explore the machine learning landscape -- HuggingFace, model formats, datasets, and the decisions that enterprises face when adopting open-source AI models. This is the foundation you need before training your own model.
