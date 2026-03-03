# Module 5: Integrate AIRS into Pipeline

## Overview

This is the "customer engagement" moment. Your pipeline works. Models train, merge, publish, and deploy. But right now, any model artifact -- clean or compromised -- flows straight to production without a single security check.

In a real engagement, this is where you would sit with the customer and say: "Let me show you how to add security gates without disrupting your existing workflow." That is exactly what you are about to do.

You will add AIRS scanning to Gate 2, manifest verification to Gate 3, metadata labeling for traceability, and detailed evaluation reporting directly in GitHub Actions. By the end, your pipeline will have a complete chain of custody from training to deployment.

## Objectives

- Add an AIRS scan step to Gate 2 between merge and publish
- Add manifest provenance verification to Gate 3 before deployment
- Implement scan labeling with pipeline metadata (gate, run ID, model version, environment, base model)
- Pull per-rule evaluation details and render them in GitHub Actions summaries

## Prerequisites

- Module 4 completed (AIRS activated, security groups explored, scans working)
- AIRS credentials validated and default security group UUIDs identified (Challenge 4.1-4.2)
- At least one successful scan from Challenge 4.3
- Familiarity with the workflow files in `.github/workflows/`

## Time Estimate

1 to 1.5 hours

---

## Challenges

### Challenge 5.1: Add Scanning to Gate 2

> `/lab:explore pipeline-scanning`

Your customer just deployed a model that contained a pickle-based reverse shell. It passed through Gate 2 unscanned and went straight to production. The post-incident review found that Gate 2 merges and publishes without any security validation. Fix this.

Gate 2 (`gate-2-publish.yaml`) currently merges the LoRA adapter with the base model and publishes the result to GCS. There is no security scan between merge and publish. Add one. If the scan returns BLOCKED, the pipeline must halt -- the compromised model must never reach the production registry.

### Challenge 5.2: Add Manifest Verification to Gate 3

> `/lab:explore manifest-verification`

Gate 3 deploys models to a Vertex AI endpoint serving real users. Currently, it deploys whatever model path it is given without checking whether that model was ever scanned. A malicious insider (or a misconfigured pipeline) could point Gate 3 at an unscanned model and bypass all your Gate 2 security work.

Add manifest verification to Gate 3 (`gate-3-deploy.yaml`) that requires a Gate 2 scan record before allowing deployment. The manifest (`manifest.json`) travels with the model artifacts and accumulates provenance records through each gate. Gate 3 should verify that the manifest contains a passing Gate 2 scan before proceeding.

### Challenge 5.3: Label Your Scans

> `/lab:explore scan-labeling`

Your customer runs 50 models through their pipeline every week. Six months from now, their CISO asks: "Which models were scanned in Q3? Which pipeline run produced this model? What base model was it trained from?" Without metadata, the answer requires digging through months of CI/CD logs.

AIRS supports attaching key-value labels to scan requests. Add meaningful labels to your pipeline scans so they are identifiable and queryable in SCM. At minimum, include gate name, run ID, model version, environment, and base model.

### Challenge 5.4: Enrich Scan Output for Developers

> `/lab:explore evaluations-api`

A developer triggers the pipeline and it fails with "AIRS scan: BLOCKED." They open the GitHub Actions log and see... a verdict and an aggregate pass/fail count. No context about what happened, what security group was used, or how to investigate. They file a ticket with the security team. The security team has to log into SCM, find the scan UUID, and relay the information back. This takes hours.

The scan response from `scan_model.py` already contains useful data: the verdict, rule summary (passed/failed/total), scan UUID, and security group. But none of this is surfaced in the GitHub Actions UI. Add a step to your pipeline that captures the scan output and renders a rich summary directly in the GitHub Actions job summary. Developers should see exactly what happened without leaving GitHub.

---

## Customer Talking Points

After completing this module, you should be able to deliver these:

**On pipeline scanning:** "Pipeline scanning is the enforcement point. Without it, any model artifact -- clean or compromised -- flows straight to production. The scan takes 2-3 minutes. The GPU deploy takes 15-30 minutes. Security overhead is negligible compared to the deployment itself."

**On manifest verification:** "Provenance tracking answers the question: has this exact model artifact been scanned and approved before deployment? Without it, there is no chain of custody from training to production."

**On labeling:** "Labels connect scans to business context. When a CISO asks 'which models passed scanning this quarter?', labels make that query possible without digging through pipeline logs."

**On evaluations:** "Developers want actionable feedback in their existing tools. Showing per-rule scan results directly in the pull request summary means security findings are seen immediately, not buried in a separate portal."

## What's Next

Your pipeline is now secured with AIRS scanning at Gate 2, provenance verification at Gate 3, and detailed reporting in every run. But what exactly is AIRS catching? In Module 6, you will build malicious models, scan them, and see exactly which rules detect which threats. You need to understand the threat landscape to have credible customer conversations.
