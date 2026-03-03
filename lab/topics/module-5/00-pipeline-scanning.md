# Pipeline Scanning — Deep Dive

> Supplemental depth for /lab:explore. Essential concepts are taught in the Module 5 flow.

## Additional Topics

### Scan Placement Strategy
The scan step goes between merge and publish in Gate 2. This is the last opportunity to reject a model before it enters the approved registry. Once published, Gate 3 and other downstream consumers can deploy it. The merge step produces the full model in GCS staging — this is the artifact that gets scanned.

**Explore:** Read `.github/workflows/gate-2-publish.yaml` and trace the artifact path: where does the merged model land? Where does it get copied to after publish? The scan must happen at the boundary between these two locations.

### Security Group Selection for Pipelines
Pipeline scans use source-type-appropriate security groups. Since the merged model lives in GCS, use a GCS security group. The `--warn-only` flag changes exit code behavior: in warn-only mode, a BLOCKED verdict still exits 0 (workflow continues). In strict mode, BLOCKED exits 1 (workflow fails). Choose strict for production pipelines, warn-only for development.

**Explore:** Read `airs/scan_model.py` and find the `--warn-only` flag implementation. How does it modify exit code behavior? What happens to the scan result in SCM — does warn-only affect what gets recorded?

### Exit Code Integration with CI/CD
GitHub Actions, GitLab CI, Jenkins, and most CI/CD systems fail a step on non-zero exit codes by default. This means no special error handling code is needed — the pipeline's built-in behavior enforces the security gate. The scan step is a natural enforcement point because it leverages existing CI/CD semantics.

**Explore:** Compare how exit code enforcement works across different CI/CD systems. What if a team uses `set +e` or `continue-on-error: true`? How would you ensure the scan result is still enforced?

### Scan Performance in CI/CD
Model scanning adds 2-3 minutes to a pipeline run. For context, GPU provisioning for deployment takes 15-30 minutes. Security overhead is negligible compared to the deployment itself. For very large models (6GB+), scan time scales with download + analysis time — the model must be downloaded to the runner for local scanning.

**Explore:** Run a timed scan on the merged model. Compare scan duration to total Gate 2 runtime. What percentage of pipeline time is the scan?

## Key Files
- `.github/workflows/gate-2-publish.yaml` — where the scan step goes
- `.github/workflows/gate-1-train.yaml` — reference pattern for existing scan step
- `airs/scan_model.py` — scanner CLI with exit code handling
- `.claude/reference/model-security-scanning.md` — SDK architecture details

## Student Activities
- Add an AIRS scan step to Gate 2 between merge and publish
- Configure it to use the GCS security group with blocking mode
- Test: trigger Gate 2 and verify the scan runs and produces a verdict
- Experiment with `--warn-only` mode: what changes in the workflow behavior?
- Time the scan step and compare to total pipeline duration

## Customer Talking Point
"Pipeline scanning is the enforcement point. Without it, any model artifact — clean or compromised — flows straight to production. The scan takes 2-3 minutes. The GPU deploy takes 15-30 minutes. Security overhead is negligible compared to the deployment itself."
