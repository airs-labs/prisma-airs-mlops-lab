# Deployment Pipeline (Gates 2 and 3)

## Topics to Cover (in order)
1. Full lifecycle -- train (Gate 1) -> merge+publish (Gate 2) -> deploy (Gate 3)
2. Gate 2 workflow -- merge adapter, publish merged model to GCS, update manifest
3. Gate 3 workflow -- verify manifest provenance, deploy Vertex AI endpoint, deploy Cloud Run app
4. Pipeline chaining -- auto_chain triggers Gate 1 -> Gate 2 -> Gate 3 automatically
5. App-only deploys -- deploy-app.yaml for code changes (no model redeployment)

## Key Files
- `.github/workflows/gate-2-publish.yaml` -- merge + publish
- `.github/workflows/gate-3-deploy.yaml` -- deploy endpoint + app
- `.github/workflows/deploy-app.yaml` -- code-only deploys on push to main
- `scripts/manifest.py` -- provenance tracking through gates

## How to Explore
- Read gate-2-publish.yaml: what happens between merge and publish?
- Read gate-3-deploy.yaml: what does it verify before deploying?
- Look at the manifest.json concept -- how does provenance flow through gates?
- Check deploy-app.yaml: why is this separate from Gate 3?

## Student Activities
- Map the artifact flow: where does the model live at each gate?
- What would happen if Gate 3 deployed without verifying the manifest?
- Why does the app deploy separately from the model deploy?

## Customer Talking Point
"Gate-based pipelines give you audit points. At each gate, you can scan, verify provenance, and make go/no-go decisions. This is where AIRS fits into the workflow."
