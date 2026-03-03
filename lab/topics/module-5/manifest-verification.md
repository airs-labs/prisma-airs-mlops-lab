# Manifest Verification

## Topics to Cover (in order)
1. What manifest.json is -- provenance record that travels with model artifacts
2. Manifest structure -- lineage, scans, training, deployments, metadata
3. Gate 3 verification -- require gate2 scan before deploying
4. The verify subcommand -- `manifest.py verify --require-scan gate2`
5. Emergency override -- `skip_manifest_check` input for break-glass scenarios

## Key Files
- `scripts/manifest.py` -- the manifest CLI (create, add-scan, verify, show)
- `.github/workflows/gate-3-deploy.yaml` -- where manifest verification happens

## How to Explore
- Run `python scripts/manifest.py show --manifest manifest.json` on an existing manifest
- Read the verify subcommand logic: what does it check? What makes it fail?
- Look at gate-3-deploy.yaml: where does manifest verification fit in the deploy flow?

## Student Activities
- Create a manifest, add a gate2 scan result, then verify it passes
- Try verifying without a gate2 scan -- see the failure message
- Add manifest verification to the Gate 3 workflow
- Discuss: when would you use skip_manifest_check? What are the risks?

## Customer Talking Point
"Provenance tracking answers the question: has this exact model artifact been scanned and approved before deployment? Without it, there is no chain of custody from training to production."
