# Module 5: Integrate AIRS into Pipeline

## Overview

This is the "customer engagement" moment. Your pipeline works. Models train, merge, publish, and deploy. But right now, any model artifact -- clean or compromised -- flows straight to production without a single security check.

In a real engagement, this is where you would sit with the customer and say: "Let me show you how to add security gates without disrupting your existing workflow." That is exactly what you are about to do.

You will enable AIRS scanning at all three pipeline gates -- each scanning from a different source type (HuggingFace, Local, GCS) with a different security group. You will add provenance tracking via the manifest, metadata labels for traceability, and developer-facing scan reports in GitHub Actions. By the end, your pipeline will have end-to-end security with a documented chain of custody.

## Objectives

- Enable Gate 1 scanning in strict mode, investigate a governance block, and fix the policy in SCM
- Add an AIRS scan step to Gate 2 between merge and publish, understand LOCAL source type scanning
- Add an AIRS scan step to Gate 3 before deployment, understand GCS source type scanning and defense-in-depth
- Implement manifest provenance tracking (record scans in Gate 2, verify in Gate 3)
- Add label support to scan_model.py and apply metadata labels across all pipeline gates
- Surface scan results in GitHub Actions job summaries for developer visibility

## Prerequisites

- Module 4 completed (AIRS SDK installed, security groups explored, scans working)
- AIRS credentials validated and default security group UUIDs identified (Module 4)
- At least one successful manual scan (Module 4)
- Familiarity with the workflow files in `.github/workflows/`

## Time Estimate

1.5 to 2 hours

---

## Challenges

### Challenge 5.1: Gate 1 — Supply Chain Scan

> `/lab:explore pipeline-scanning`

Gate 1 has a scan step that has been skipped since Module 2. Time to enable it. When you do, you will discover a policy issue -- the same governance block on Qwen you found in Module 4. Instead of bypassing the enforcement, you will fix the policy at the source.

This challenge covers the HuggingFace source type: models scanned via the AIRS-HuggingFace partnership with 11 rules including governance checks (license validation, org verification).

### Challenge 5.2: Gate 2 — Artifact Scan

> `/lab:explore pipeline-scanning`

Gate 2 merges and publishes. Currently there is no scan between these steps -- a compromised artifact would flow straight to the production registry. Add a scan step using the Local source type (7 threat detection rules) and record the scan result in the manifest for downstream verification.

### Challenge 5.3: Gate 3 — Pre-Deploy Scan

> `/lab:explore manifest-verification`

Gate 3 deploys models from GCS to a GPU endpoint serving real users. Add a scan step before deployment using the GCS source type, and add manifest verification to confirm the model went through the full pipeline. This is the third source type and the final enforcement point.

### Challenge 5.4: Labels & Traceability

> `/lab:explore scan-labels`

Your customer runs 50 models through their pipeline every week. Six months from now, their CISO asks: "Which models were scanned in Q3?" Without metadata labels, that query requires digging through CI/CD logs. Add label support to `scan_model.py` and apply labels across all three pipeline gates.

### Challenge 5.5: Enrich Scan Output

> `/lab:explore evaluations-api`

A developer triggers the pipeline and it fails with "AIRS scan: BLOCKED." They open GitHub Actions and see a verdict with no context. Build developer-facing scan reports using GitHub Actions job summaries so developers can self-serve instead of filing tickets with the security team.

---

## Customer Talking Points

After completing this module, you should be able to deliver these:

**On pipeline scanning:** "We scan at every gate -- supply chain check at training (HuggingFace), artifact check at publish (Local), and pre-deploy verification from the registry (GCS). Three independent validation points, each with its own security group policy. Scanning adds 2-3 minutes to a pipeline that takes 15-30 minutes for GPU deployment."

**On source types:** "Different scanning contexts use different security groups. HuggingFace scans include governance rules because the platform provides license and org metadata. Local and GCS scans focus on threat detection -- code execution, format safety, operator analysis. The right policy depends on the context."

**On manifest verification:** "Provenance tracking answers the question: has this exact model artifact been scanned and approved at every stage? The manifest documents the full chain of custody from training to deployment."

**On labeling:** "Labels connect scans to business context. When a CISO asks 'which models passed scanning this quarter?', labels make that query possible without digging through pipeline logs."

**On the developer experience:** "Developers want actionable feedback in their existing tools. We surface scan results directly in GitHub Actions -- verdict, rule summary, and a link to full details in the security console."

## What's Next

Your pipeline is now secured with AIRS scanning at every gate, provenance tracking, and developer-friendly reporting. But what exactly is AIRS catching? In Module 6, you will build intentionally malicious models, scan them, and see exactly which rules detect which threats. You need to understand the threat landscape to have credible customer conversations.
