# Scan Labeling — Deep Dive

> Supplemental depth for /lab:explore. Essential concepts are taught in the Module 5 flow.

## Additional Topics

### Label Taxonomy for ML Pipelines
Labels are key-value metadata attached to scan requests. A well-designed label taxonomy enables compliance queries, incident investigation, and operational reporting. The minimum useful set: `gate` (pipeline stage), `run_id` (specific execution), `model_version` (artifact version), `environment` (deployment target), `base_model` (training provenance). Richer taxonomies might add: `dataset_version`, `team`, `business_unit`, `compliance_framework`.

**Explore:** Design a label taxonomy for an enterprise with 50 models across 3 environments (dev, staging, prod). What queries would the security team need to run? What labels make those queries possible?

### GitHub Actions Environment Variables
GitHub Actions provides built-in environment variables that create direct links between SCM scans and pipeline runs: `$GITHUB_RUN_ID` (unique execution ID), `$GITHUB_SHA` (commit hash), `$GITHUB_REF_NAME` (branch name), `$GITHUB_REPOSITORY` (repo name). These are available in every workflow step without configuration.

**Explore:** Check the GitHub Actions documentation for the full list of default environment variables. Which ones would be useful as scan labels? How would you add custom labels beyond the defaults?

### Label Filtering in SCM
Labels appear in the SCM Model Security console alongside scan records. Security teams can filter scans by label values — "show me all gate2 scans from the last quarter" or "find scans for model version v2.1.0." This transforms raw scan data into queryable operational intelligence.

**Explore:** After submitting labeled scans, navigate to SCM and filter by label values. How does the UI expose labels? Can you build a compliance report using label filters?

## Key Files
- `airs/scan_model.py` — scanner CLI with label support (`-l key=value`)
- `.github/workflows/gate-2-publish.yaml` — where labels are added to pipeline scans
- `.claude/reference/airs-tech-docs/ai-runtime-security-release-notes.md` — label feature documentation

## Student Activities
- Add labels to a scan: `gate=gate2`, `run_id=$GITHUB_RUN_ID`, `model_version=v2.0.0`
- Submit labeled scans and verify labels appear in SCM reports
- Add standard labels to the Gate 2 scan step in the workflow
- Design a label taxonomy for a multi-team, multi-environment enterprise deployment

## Customer Talking Point
"Labels connect scans to business context. When a CISO asks 'which models passed scanning this quarter?', labels make that query possible without digging through pipeline logs."
