# Module 5: Integrate AIRS into Pipeline

## Overview

This is the "customer engagement" moment. Your pipeline works. Models train, merge, publish, and deploy. But right now, any model artifact -- clean or compromised -- flows straight to production without a single security check.

You will add AIRS scanning to Gate 2, manifest verification to Gate 3, metadata labeling for traceability, and detailed evaluation reporting directly in GitHub Actions.

::: tip Interactive Lab
The full interactive experience for this module runs in **Claude Code**. Use `/module 5` to begin the guided walkthrough with your AI mentor.
:::

## Objectives

- Add an AIRS scan step to Gate 2 between merge and publish
- Add manifest provenance verification to Gate 3 before deployment
- Implement scan labeling with pipeline metadata (gate, run ID, model version, environment, base model)
- Pull per-rule evaluation details and render them in GitHub Actions summaries

## Time Estimate

~1 to 1.5 hours

## Challenges

### 5.1: Add Scanning to Gate 2

Gate 2 currently merges and publishes without any security validation. Add an AIRS scan between merge and publish. If the scan returns BLOCKED, the pipeline must halt -- the compromised model never reaches the production registry.

**What to modify:** `.github/workflows/gate-2-publish.yaml`

### 5.2: Add Manifest Verification to Gate 3

Gate 3 currently deploys whatever model path it receives without checking whether that model was ever scanned. Add manifest verification that requires a Gate 2 scan record before allowing deployment.

**The verification tool:** `scripts/manifest.py verify --require-scan gate2`

### 5.3: Label Your Scans

Add meaningful key-value labels to scan requests so they are identifiable and queryable in SCM. Labels like `gate`, `run_id`, `model_version`, `environment`, and `base_model` create traceability from any scan back to the exact pipeline run.

### 5.4: Enrich Scan Output for Developers

Surface scan results in the GitHub Actions job summary so developers see exactly what happened without leaving GitHub. Build a rich markdown summary with verdict, rule counts, scan UUID, and labels.

**Product gap to discuss:** Per-rule evaluation details are not available through the SDK. Full breakdowns require SCM access. This is a real limitation worth raising with customers.

## Key Concepts

- **Pipeline Scanning** -- The enforcement point. Without it, any artifact flows to production unchecked
- **Manifest Verification** -- Chain of custody from training to deployment. Has this exact artifact been scanned?
- **Scan Labels** -- Connect scans to business context. Make "which models passed scanning this quarter?" answerable
- **GitHub Actions Summaries** -- Rich markdown rendered in the workflow run UI via `$GITHUB_STEP_SUMMARY`

## Verification

Run `/verify-5` in Claude Code to confirm scanning in Gate 2, manifest verification in Gate 3, labels visible in SCM, and rich summaries in GitHub Actions.

## What's Next

Your pipeline is secured. But what exactly is AIRS catching? [Module 6: The Threat Zoo](/modules/6-threat-zoo) builds malicious models, scans them, and explores the real threat landscape.
