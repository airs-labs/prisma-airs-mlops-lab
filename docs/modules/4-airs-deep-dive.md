# Module 4: AIRS Deep Dive

## Overview

Welcome to Act 2 -- **Understand the Security.**

You have a working ML pipeline. Models train, merge, publish, and deploy. But right now there is nothing stopping a compromised model from flowing straight to production. Before you can secure the pipeline, you need to understand AIRS inside and out -- the way you would need to demo it to a customer.

::: tip Interactive Lab
The full interactive experience for this module runs in **Claude Code**. Use `/lab:module 4` to begin the guided walkthrough with your AI mentor.
:::

## Objectives

- Create a restricted service account with minimum scanning permissions (RBAC)
- Install the AIRS SDK and run scans from the CLI and Python
- Understand scan responses: eval_outcome, eval_summary, rules_passed, rules_failed
- Explore the PANW-HuggingFace partnership and compare public vs enterprise scanning
- Navigate Strata Cloud Manager (SCM) to find scan reports and manage security groups
- Create custom security groups with different blocking policies

## Time Estimate

~1 to 1.5 hours

## Challenges

### 4.1: Set Up Least-Privilege Access

Create a custom role (`model-scanning-only`) with minimum required permissions and a restricted service account that can scan but cannot administer security groups. This follows the same IAM model enterprises use for every other cloud service.

### 4.2: Your First Scans

Install the AIRS SDK, scan a known-safe model, then scan a pickle bomb. Compare the results side by side. Examine the scan response: `uuid`, `eval_outcome`, `eval_summary`, `rules_passed`, `rules_failed`.

**The four eval_outcome values:** ALLOWED, BLOCKED, PENDING, ERROR. These are the only four values that exist.

### 4.3: HuggingFace Integration

Explore the PANW-HuggingFace partnership. Understand what customers get for free from HF public scanning and what AIRS adds: custom policies, blocking enforcement, private model scanning, SCM management, and RBAC.

### 4.4: Security Groups Deep Dive

Create two custom security groups in SCM: one that blocks on every rule, one that only warns. Scan the same model against both and compare the results. Same detection, different enforcement -- this is the core value proposition.

**Critical concept:** Source types (LOCAL, GCS, HUGGING_FACE, etc.) must match between the security group and the model being scanned.

## Key Concepts

- **AIRS SDK** -- `model-security-client` package. Three operations: `scan()`, `get_scan(uuid)`, `list_scans(filters)`
- **Security Groups** -- Policy containers in SCM. Each bound to a source type, with per-rule blocking/warning configuration
- **eval_outcome** -- The verdict. BLOCKED only when a rule with Blocking=On detects an issue
- **rules_failed** -- Counts ALL rules that detected issues (blocking AND non-blocking)
- **Source Type Matching** -- Security group source type must match the model source. SDK enforces this

## Verification

Run `/lab:verify-4` in Claude Code to confirm RBAC setup, successful scans, custom security groups, and conceptual understanding.

## What's Next

You understand AIRS scanning inside and out. [Module 5: Integrate AIRS](/modules/5-integrate-airs) adds scanning gates, manifest verification, and evaluation reporting directly into your GitHub Actions pipeline.
