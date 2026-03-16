# Manifest Verification — Deep Dive

> Supplemental depth for /lab:explore. Essential concepts are taught in the Module 5 flow.

## Additional Topics

### Manifest Structure and Lifecycle
The `manifest.json` file is a provenance document that travels alongside model artifacts through the pipeline. Each gate appends records: Gate 1 adds training metadata (dataset, hyperparameters, training job ID), Gate 2 adds scan results (UUID, verdict, security group, timestamp), and Gate 3 adds deployment records (endpoint ID, service URL, deployment time). Over time, the manifest becomes a complete audit trail for the model.

**Explore:** Run `python scripts/manifest.py show --manifest manifest.json` on an existing manifest. Examine the JSON structure — what fields are in each section? Run `python scripts/manifest.py --help` to see all subcommands: `create`, `add-scan`, `add-training`, `add-deployment`, `set-version`, `verify`, `show`.

### The Verify Subcommand
`manifest.py verify --require-scan gate2 --require-verdict ALLOWED` checks that a Gate 2 scan record exists AND has an ALLOWED verdict. If either condition fails, the script exits non-zero. This is the enforcement mechanism in Gate 3 — the deployment workflow checks provenance before proceeding.

**Explore:** Read `scripts/manifest.py` and trace the `verify` subcommand logic. What specific fields does it check? What error messages does it produce on failure? Try running verify against a manifest with no gate2 scan — observe the failure.

### Break-Glass Override Pattern
The `skip_manifest_check` input exists for production emergencies — when you MUST deploy a model despite missing or failed scans. In enterprise environments, using this override should: (1) be logged and auditable, (2) require elevated approval, (3) trigger a post-incident review. It's a safety valve, not a convenience bypass.

**Explore:** Design an override approval workflow. How would you ensure that `skip_manifest_check` usage is tracked and reviewed? What audit trail should it create?

## Key Files
- `scripts/manifest.py` — the manifest CLI (create, add-scan, verify, show)
- `.github/workflows/gate-3-deploy.yaml` — where manifest verification happens

## Student Activities
- Create a manifest, add a gate2 scan result, then verify it passes
- Try verifying without a gate2 scan — see the failure message
- Add manifest verification to the Gate 3 workflow
- Design an override approval process: who approves, how is it logged, what triggers review?

## Customer Talking Point
"Provenance tracking answers the question: has this exact model artifact been scanned and approved before deployment? Without it, there is no chain of custody from training to production."
