# Getting Started

## What Is This Workshop?

The AIRS MLOps Lab is a hands-on workshop where you build, deploy, and secure a real ML pipeline. You will fine-tune an open-source language model into a cybersecurity advisor, deploy it on Google Cloud, and then systematically secure the pipeline using Palo Alto Networks AI Runtime Security (AIRS).

This is not a passive tutorial. You work **with Claude Code** as your development partner and mentor. Claude has been configured specifically for this lab -- it knows the codebase, paces its explanations, and uses Socratic questioning to build your understanding.

## Prerequisites

Before starting the lab, ensure you have:

- **GCP Project** -- A Google Cloud project with owner rights, Vertex AI API enabled
- **AIRS License** -- Access to a Prisma AIRS tenant with Strata Cloud Manager (SCM) credentials
- **Claude Code** -- Installed and configured with Vertex AI as the provider
- **GitHub Account** -- With a fork of the lab repository and `gh` CLI authenticated
- **Python 3.12+** -- With `uv` for dependency management
- **HuggingFace Account** -- For exploring models and datasets

Your instructor will provide GCP project details and AIRS credentials during the setup session.

## The Three-Act Structure

The workshop is organized into three acts, with a presentation break between Acts 1 and 2.

### Act 1: Build It (Modules 0-3)

You build a complete ML pipeline from scratch. By the end of Act 1, you will have a live cybersecurity advisor chatbot running on Google Cloud -- trained, merged, published, and deployed through a 3-gate pipeline. No security scans are in place yet. That is intentional.

| Module | Focus | Time |
|--------|-------|------|
| [Module 0: Setup](/modules/0-setup) | Environment, GCP, GitHub, AIRS credentials | ~30 min |
| [Module 1: ML Fundamentals](/modules/1-ml-fundamentals) | HuggingFace, formats, datasets, platforms | ~1-1.5 hr |
| [Module 2: Train Your Model](/modules/2-train-your-model) | Gate 1, LoRA fine-tuning, Vertex AI | ~1-1.5 hr |
| [Module 3: Deploy & Serve](/modules/3-deploy-and-serve) | Gate 2+3, merge, publish, deploy, live app | ~1-1.5 hr |

### Presentation Break

Between Acts 1 and 2, there is an instructor-led session covering the AIRS value proposition, real-world model supply chain attacks, and customer engagement scenarios.

### Act 2: Understand Security (Module 4)

A deep dive into AIRS itself. You set up least-privilege access, run your first scans, explore the HuggingFace partnership, and build custom security policies.

| Module | Focus | Time |
|--------|-------|------|
| [Module 4: AIRS Deep Dive](/modules/4-airs-deep-dive) | RBAC, SDK, scanning, security groups, SCM | ~1-1.5 hr |

### Act 3: Secure It (Modules 5-7)

You take everything you learned and secure the pipeline you built in Act 1. Then you explore what AIRS catches, what it does not catch, and how to have honest customer conversations about both.

| Module | Focus | Time |
|--------|-------|------|
| [Module 5: Integrate AIRS](/modules/5-integrate-airs) | Pipeline scanning, manifest verification, labeling | ~1-1.5 hr |
| [Module 6: The Threat Zoo](/modules/6-threat-zoo) | Pickle bombs, Keras traps, format risk, real incidents | ~1-1.5 hr |
| [Module 7: Gaps & Poisoning](/modules/7-gaps-and-poisoning) | Data poisoning, behavioral backdoors, defense in depth | ~45 min-1 hr |

## How to Use Claude Code

Claude Code is your lab mentor. It has been configured through `CLAUDE.md` to:

- Act as a **Socratic mentor** -- asking questions, not lecturing
- Pace explanations **one concept at a time**
- Provide **progressive hints** when you are stuck (concept, then approach, then specific)
- Show from the **project first** (real files, real configs), then explain

### Available Commands

| Command | Purpose |
|---------|---------|
| `/module N` | Start or resume module N |
| `/explore TOPIC` | Guided exploration of a topic |
| `/verify-N` | Run verification checks for module N |
| `/hint` | Get progressive help (concept -> approach -> specific) |
| `/quiz` | Test your understanding |
| `/progress` | See your completion status |

## Begin the Lab

Ready to start? Head to [Module 0: Setup](/modules/0-setup) to configure your environment and meet your AI mentor.
