# Pipeline Scanning

## Topics to Cover (in order)
1. Where scanning fits -- between merge and publish in Gate 2
2. Security group selection -- which group to use for pipeline scans (blocking vs warning)
3. --warn-only vs strict mode -- when to warn, when to block, pipeline implications
4. Exit code handling -- how the workflow reacts to BLOCKED vs ALLOWED
5. Scan step implementation -- adding the AIRS scan step to the Gate 2 workflow

## Key Files
- `.github/workflows/gate-2-publish.yaml` -- where the scan step should go
- `airs/scan_model.py` -- the scanner CLI to call from the workflow
- Reference: docs/airs-tech-docs/ai-model-security.md for scanning configuration

## How to Explore
- Read gate-2-publish.yaml: find where merge ends and publish begins
- The scan step goes between those two -- scan the merged artifact before publishing
- Look at scan_model.py's exit codes: 0 (pass), 1 (blocked/error)

## Student Activities
- Add an AIRS scan step to Gate 2 between merge and publish
- Configure it to use the "block" security group for GCS models
- Test: trigger Gate 2 and verify the scan runs and produces a verdict
- Try --warn-only mode: what changes in the workflow behavior?

## Customer Talking Point
"Pipeline scanning is the enforcement point. Without it, any model artifact -- clean or compromised -- flows straight to production. The question is not whether to scan, but where in the pipeline and what policy to enforce."
