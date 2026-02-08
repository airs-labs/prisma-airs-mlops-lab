# GCP Environment Setup

## Topics to Cover (in order)

1. GCP project — what it is, how it's provisioned, project naming conventions
2. Authentication layers — local CLI auth (`gcloud auth login`) vs Application Default Credentials (ADC) vs Workload Identity Federation (for GitHub Actions)
3. GCS bucket structure — staging bucket (raw/merged artifacts) vs blessed/registry bucket (approved artifacts)
4. Pipeline configuration — `.github/pipeline-config.yaml` as the single source of truth for infrastructure config
5. Required API scopes — aiplatform, run, cloudbuild, storage

## How to Explore

- Check current auth: `gcloud auth list`, `gcloud config get-value project`
- Check billing: `gcloud billing projects describe $PROJECT`
- Check enabled APIs: `gcloud services list --enabled`
- Check buckets: read `.github/pipeline-config.yaml` then `gcloud storage ls gs://[bucket]/`
- For @ts-workshop: verify project is under the correct GCP folder

## Student Activities

- Verify all four auth/config items: project, auth, billing, APIs
- Find the bucket configuration in `.github/pipeline-config.yaml`
- If buckets have placeholder names, create real ones and update the config
- Verify end-to-end: `gcloud storage ls` on both staging and blessed buckets

## Customer Talking Point

"Environment configuration is the #1 friction point in AIRS onboarding. If the GCP project, buckets, or credentials aren't right, every downstream feature — scanning, deployment, verification — fails with cryptic errors. We always start with a clean environment check."
