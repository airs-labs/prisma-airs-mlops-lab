# Module 5 Flow: Integrate AIRS into Pipeline

## Points Available

| Source | Points | Track |
|--------|--------|-------|
| Gate 2 scan step added | 2 | All |
| Gate 3 manifest verification added | 2 | All |
| Successful pipeline run with AIRS | 2 | All |
| Scan labels visible in SCM | 2 | All |
| Evaluation summary in GH Actions | 2 | All |
| Understanding: scan failure flow | 3 | All |
| **Total** | **13** | |

---

## Challenge 5.1: Add Scanning to Gate 2

### Flow

**What to modify:** `.github/workflows/gate-2-publish.yaml`

**Where the scan goes:** After the merge step completes (the merged model exists in GCS staging) and before the publish step copies artifacts to the approved location.

**Decisions to make:**
- Which security group should Gate 2 use? (blocking vs warning)
- Should the scan use `--warn-only` or strict mode?
- What happens to the pipeline when the scan fails?

### Hints

**Hint 1 (Concept):** Look at how Gate 3 already handles scanning. The pattern is the same: call `airs/scan_model.py` with the model path, security group UUID, and check the exit code. Gate 2 just needs the same pattern inserted between merge and publish.

**Hint 2 (Approach):** The scan step needs: AIRS credentials (CLIENT_ID, CLIENT_SECRET, TSG_ID from GitHub secrets), the model path in GCS, and the security group UUID. The `scan_model.py` script handles the SDK interaction. Exit code 0 means ALLOWED, exit code 1 means BLOCKED or ERROR.

**Hint 3 (Specific):** In a GitHub Actions workflow, a non-zero exit code from a step causes the job to fail by default. This means if `scan_model.py` returns exit code 1 (BLOCKED), the workflow stops and the publish step never runs. This is the desired behavior -- the compromised model never reaches the production registry.

### Points: 0

---

## Challenge 5.2: Add Manifest Verification to Gate 3

### Flow

**What to modify:** `.github/workflows/gate-3-deploy.yaml`

**The verification tool:** `scripts/manifest.py verify --require-scan gate2`

**What to test:**
1. Trigger Gate 3 with a model that has a valid Gate 2 scan in its manifest -- should succeed
2. Trigger Gate 3 with a model that has no Gate 2 scan -- should fail
3. Understand the `skip_manifest_check` emergency override and when it would be appropriate

### Hints

**Hint 1 (Concept):** The manifest is a JSON file that lives alongside model artifacts in GCS. It tracks lineage (base model, adapter, merged path), scan records (per gate), training configuration, and deployment history. Each gate adds its own records. Gate 3 reads the manifest and checks for required entries.

**Hint 2 (Approach):** Run `python scripts/manifest.py show --manifest manifest.json` to see what a manifest looks like. The `verify` subcommand checks for required scan entries: `--require-scan gate2` means the manifest must contain a scan record tagged with gate2 that has a passing verdict.

**Hint 3 (Specific):** Add a verification step early in the Gate 3 workflow, before the deployment steps. Download the manifest from GCS, run the verify command, and only proceed if it passes. The workflow should have a `skip_manifest_check` input parameter for break-glass scenarios -- but document that using it bypasses provenance verification.

### Points: 0

---

## Challenge 5.3: Label Your Scans

### Flow

**Minimum labels to include:**

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

### Hints

**Hint 1 (Concept):** Check the AIRS SDK documentation and release notes for label support. The `scan_model.py` CLI may need a `--labels` flag added. Labels are typically key-value pairs passed during the scan request. Reference `docs/airs-tech-docs/ai-runtime-security-release-notes.md` for the latest features.

**Hint 2 (Approach):** GitHub Actions provides environment variables you can use as label values: `$GITHUB_RUN_ID`, `$GITHUB_SHA`, `$GITHUB_REF_NAME`, `$GITHUB_REPOSITORY`. These create a direct link from any scan in SCM back to the exact pipeline run that produced it.

**Hint 3 (Specific):** Labels connect scans to business context. Consider versioning labels: `model_version`, `dataset_version`, `training_config_hash`. When a CISO asks "which models passed scanning this quarter?", labels make that query possible without digging through pipeline logs.

### Points: 0

---

## Challenge 5.4: Enrich Scan Output for Developers

### Flow

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

### Hints

**Hint 1 (Concept):** `scan_model.py` already has `--output-json` which saves the full scan response to a file. Use this in your workflow step, then read the JSON in a subsequent step to build the summary. In GitHub Actions, you can also capture step outputs using `echo "key=value" >> $GITHUB_OUTPUT`.

**Hint 2 (Approach):** GitHub Actions supports rich markdown in job summaries. Write to `$GITHUB_STEP_SUMMARY`:

```bash
echo "## AIRS Scan Results" >> $GITHUB_STEP_SUMMARY
echo "| Field | Value |" >> $GITHUB_STEP_SUMMARY
echo "|-------|-------|" >> $GITHUB_STEP_SUMMARY
echo "| Verdict | $VERDICT |" >> $GITHUB_STEP_SUMMARY
echo "| Rules Passed | $PASSED/$TOTAL |" >> $GITHUB_STEP_SUMMARY
echo "| Scan UUID | $UUID |" >> $GITHUB_STEP_SUMMARY
```

This shows up on the workflow run summary page -- visible to anyone who clicks the run.

**Hint 3 (Specific):** The fact that per-rule details require SCM access is a real limitation. In a customer engagement, this is a feature request conversation: "The SDK provides aggregate counts, but developers need per-rule details in their CI/CD tool. Today that requires SCM access. Here is how we bridge that gap with what is available now, and here is the feature request for the product team."

### Points: 0
