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

- Module 4 completed (AIRS SDK installed, security groups created, scans working)
- Restricted service account from Challenge 4.1
- At least one successful scan from Challenge 4.2
- Familiarity with the workflow files in `.github/workflows/`

## Time Estimate

1 to 1.5 hours

---

## Challenges

### Challenge 5.1: Add Scanning to Gate 2

> `/lab:explore pipeline-scanning`

**The scenario:** Your customer just deployed a model that contained a pickle-based reverse shell. It passed through Gate 2 unscanned and went straight to production. The post-incident review found that Gate 2 merges and publishes without any security validation. Fix this.

**Your task:** Gate 2 (`gate-2-publish.yaml`) currently merges the LoRA adapter with the base model and publishes the result to GCS. There is no security scan between merge and publish. Add one. If the scan returns BLOCKED, the pipeline must halt -- the compromised model must never reach the production registry.

**What to modify:** `.github/workflows/gate-2-publish.yaml`

**Where the scan goes:** After the merge step completes (the merged model exists in GCS staging) and before the publish step copies artifacts to the approved location.

**Decisions to make:**
- Which security group should Gate 2 use? (blocking vs warning)
- Should the scan use `--warn-only` or strict mode?
- What happens to the pipeline when the scan fails?

<details>
<summary>Hint 1: Find the pattern</summary>

Look at how Gate 3 already handles scanning. The pattern is the same: call `airs/scan_model.py` with the model path, security group UUID, and check the exit code. Gate 2 just needs the same pattern inserted between merge and publish.
</details>

<details>
<summary>Hint 2: The scan step structure</summary>

The scan step needs: AIRS credentials (CLIENT_ID, CLIENT_SECRET, TSG_ID from GitHub secrets), the model path in GCS, and the security group UUID. The `scan_model.py` script handles the SDK interaction. Exit code 0 means ALLOWED, exit code 1 means BLOCKED or ERROR.
</details>

<details>
<summary>Hint 3: Handling the verdict</summary>

In a GitHub Actions workflow, a non-zero exit code from a step causes the job to fail by default. This means if `scan_model.py` returns exit code 1 (BLOCKED), the workflow stops and the publish step never runs. This is the desired behavior -- the compromised model never reaches the production registry.
</details>

---

### Challenge 5.2: Add Manifest Verification to Gate 3

> `/lab:explore manifest-verification`

**The scenario:** Gate 3 deploys models to a Vertex AI endpoint serving real users. Currently, it deploys whatever model path it is given without checking whether that model was ever scanned. A malicious insider (or a misconfigured pipeline) could point Gate 3 at an unscanned model and bypass all your Gate 2 security work.

**Your task:** Add manifest verification to Gate 3 (`gate-3-deploy.yaml`) that requires a Gate 2 scan record before allowing deployment. The manifest (`manifest.json`) travels with the model artifacts and accumulates provenance records through each gate. Gate 3 should verify that the manifest contains a passing Gate 2 scan before proceeding.

**What to modify:** `.github/workflows/gate-3-deploy.yaml`

**The verification tool:** `scripts/manifest.py verify --require-scan gate2`

**What to test:**
1. Trigger Gate 3 with a model that has a valid Gate 2 scan in its manifest -- should succeed
2. Trigger Gate 3 with a model that has no Gate 2 scan -- should fail
3. Understand the `skip_manifest_check` emergency override and when it would be appropriate

<details>
<summary>Hint 1: The manifest structure</summary>

The manifest is a JSON file that lives alongside model artifacts in GCS. It tracks lineage (base model, adapter, merged path), scan records (per gate), training configuration, and deployment history. Each gate adds its own records. Gate 3 reads the manifest and checks for required entries.
</details>

<details>
<summary>Hint 2: Using manifest.py</summary>

Run `python scripts/manifest.py show --manifest manifest.json` to see what a manifest looks like. The `verify` subcommand checks for required scan entries: `--require-scan gate2` means the manifest must contain a scan record tagged with gate2 that has a passing verdict.
</details>

<details>
<summary>Hint 3: The workflow integration</summary>

Add a verification step early in the Gate 3 workflow, before the deployment steps. Download the manifest from GCS, run the verify command, and only proceed if it passes. The workflow should have a `skip_manifest_check` input parameter for break-glass scenarios -- but document that using it bypasses provenance verification.
</details>

---

### Challenge 5.3: Label Your Scans

> `/lab:explore scan-labeling`

**The scenario:** Your customer runs 50 models through their pipeline every week. Six months from now, their CISO asks: "Which models were scanned in Q3? Which pipeline run produced this model? What base model was it trained from?" Without metadata, the answer requires digging through months of CI/CD logs.

**Your task:** AIRS supports attaching key-value labels to scan requests. Add meaningful labels to your pipeline scans so they are identifiable and queryable in SCM. At minimum, include:

| Label Key | Value | Purpose |
|-----------|-------|---------|
| `gate` | gate1, gate2, gate3 | Which pipeline stage |
| `run_id` | `$GITHUB_RUN_ID` | Link scan to specific pipeline execution |
| `model_version` | v2.0.0 or similar | Which version of the model |
| `environment` | staging, production | Deployment target |
| `base_model` | Qwen/Qwen2.5-3B | Training provenance |

**What to do:**
1. Research the scan labeling feature in the AIRS SDK (check docs and release notes)
2. Add a `--labels` argument to your scan calls in the workflow
3. Verify labels appear in SCM scan reports
4. Think about what other labels would help an enterprise track models across environments

<details>
<summary>Hint 1: Where to look</summary>

Check the AIRS SDK documentation and release notes for label support. The `scan_model.py` CLI may need a `--labels` flag added. Labels are typically key-value pairs passed during the scan request. Reference `docs/airs-tech-docs/ai-runtime-security-release-notes.md` for the latest features.
</details>

<details>
<summary>Hint 2: GitHub Actions variables</summary>

GitHub Actions provides environment variables you can use as label values: `$GITHUB_RUN_ID`, `$GITHUB_SHA`, `$GITHUB_REF_NAME`, `$GITHUB_REPOSITORY`. These create a direct link from any scan in SCM back to the exact pipeline run that produced it.
</details>

<details>
<summary>Hint 3: Provenance tracking</summary>

Labels connect scans to business context. Consider versioning labels: `model_version`, `dataset_version`, `training_config_hash`. When a CISO asks "which models passed scanning this quarter?", labels make that query possible without digging through pipeline logs.
</details>

---

### Challenge 5.4: Enrich Scan Output for Developers

> `/lab:explore evaluations-api`

**The scenario:** A developer triggers the pipeline and it fails with "AIRS scan: BLOCKED." They open the GitHub Actions log and see... a verdict and an aggregate pass/fail count. No context about what happened, what security group was used, or how to investigate. They file a ticket with the security team. The security team has to log into SCM, find the scan UUID, and relay the information back. This takes hours.

**Your task:** The scan response from `scan_model.py` already contains useful data: the verdict, rule summary (passed/failed/total), scan UUID, and security group. But none of this is surfaced in the GitHub Actions UI. Add a step to your pipeline that captures the scan output and renders a rich summary directly in the GitHub Actions job summary. Developers should see exactly what happened without leaving GitHub.

**What the SDK gives you today:**
- `eval_outcome`: ALLOWED, BLOCKED, ERROR, or PENDING
- `eval_summary`: `total_rules`, `rules_passed`, `rules_failed`
- `uuid`: The scan identifier (links directly to SCM for full details)
- Labels you attached in Challenge 5.3

**What the SDK does NOT give you:** Per-rule evaluation details are not available through the SDK or a public API endpoint. For per-rule breakdowns, users must view the scan in SCM. This is a real product gap worth discussing with customers.

**What to build:**
1. Modify `scan_model.py` to output scan results as structured JSON (or capture its output)
2. Add a GitHub Actions step that reads the scan output and writes a formatted summary to `$GITHUB_STEP_SUMMARY`
3. Include: verdict badge (green/red), rule summary table, scan UUID (as a reference for SCM), labels, and a direct link to SCM
4. Test: run the pipeline with a clean model and a flagged model, compare the summaries

<details>
<summary>Hint 1: Capturing scan output</summary>

`scan_model.py` already has `--output-json` which saves the full scan response to a file. Use this in your workflow step, then read the JSON in a subsequent step to build the summary. In GitHub Actions, you can also capture step outputs using `echo "key=value" >> $GITHUB_OUTPUT`.
</details>

<details>
<summary>Hint 2: Building the summary</summary>

GitHub Actions supports rich markdown in job summaries. Write to `$GITHUB_STEP_SUMMARY`:

```bash
echo "## AIRS Scan Results" >> $GITHUB_STEP_SUMMARY
echo "| Field | Value |" >> $GITHUB_STEP_SUMMARY
echo "|-------|-------|" >> $GITHUB_STEP_SUMMARY
echo "| Verdict | $VERDICT |" >> $GITHUB_STEP_SUMMARY
echo "| Rules Passed | $PASSED/$TOTAL |" >> $GITHUB_STEP_SUMMARY
echo "| Scan UUID | $UUID |" >> $GITHUB_STEP_SUMMARY
```

This shows up on the workflow run summary page -- visible to anyone who clicks the run.
</details>

<details>
<summary>Hint 3: The product gap conversation</summary>

The fact that per-rule details require SCM access is a real limitation. In a customer engagement, this is a feature request conversation: "The SDK provides aggregate counts, but developers need per-rule details in their CI/CD tool. Today that requires SCM access. Here is how we bridge that gap with what is available now, and here is the feature request for the product team."
</details>

---

## Verification

By the end of this module, confirm:

- [ ] Gate 2 has an AIRS scan step between merge and publish
- [ ] Gate 2 halts on BLOCKED verdict (non-zero exit code stops the workflow)
- [ ] Gate 3 has manifest verification before deployment
- [ ] Gate 3 fails when manifest lacks a Gate 2 scan record
- [ ] Gate 3 `skip_manifest_check` override works for emergencies
- [ ] Scan labels include gate name, run ID, model version, environment, and base model
- [ ] Labels are visible in SCM scan reports
- [ ] Scan summary (verdict, rule counts, UUID, labels) renders in GitHub Actions job summary
- [ ] Full pipeline runs end-to-end: Gate 1 (train) -> Gate 2 (merge + scan + publish) -> Gate 3 (verify + scan + deploy)

## Customer Talking Points

After completing this module, you should be able to deliver these:

**On pipeline scanning:** "Pipeline scanning is the enforcement point. Without it, any model artifact -- clean or compromised -- flows straight to production. The scan takes 2-3 minutes. The GPU deploy takes 15-30 minutes. Security overhead is negligible compared to the deployment itself."

**On manifest verification:** "Provenance tracking answers the question: has this exact model artifact been scanned and approved before deployment? Without it, there is no chain of custody from training to production."

**On labeling:** "Labels connect scans to business context. When a CISO asks 'which models passed scanning this quarter?', labels make that query possible without digging through pipeline logs."

**On evaluations:** "Developers want actionable feedback in their existing tools. Showing per-rule scan results directly in the pull request summary means security findings are seen immediately, not buried in a separate portal."

## What's Next

Your pipeline is now secured with AIRS scanning at Gate 2, provenance verification at Gate 3, and detailed reporting in every run. But what exactly is AIRS catching? In Module 6, you will build malicious models, scan them, and see exactly which rules detect which threats. You need to understand the threat landscape to have credible customer conversations.
