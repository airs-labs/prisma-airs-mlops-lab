# GCP IAM & Workload Identity Setup

## Topics to Cover (in order)

1. Why keyless authentication — the risk of long-lived SA keys vs WIF
2. The three service accounts — GitHub Actions SA, Compute Engine default SA, Cloud Build SA
3. Workload Identity Federation — OIDC trust chain between GitHub and GCP
4. IAM roles — what each role grants and why it's needed
5. Common failure modes — the errors students will see when roles are missing

## How to Explore

- Check SA list: `gcloud iam service-accounts list`
- Check WIF pools: `gcloud iam workload-identity-pools list --location=global`
- Check SA roles: `gcloud projects get-iam-policy $PROJECT --flatten="bindings[].members" --filter="bindings.members:github-actions-sa" --format="table(bindings.role)"`
- Check GH secrets: `gh secret list`

## Student Activities

- Explain why there are THREE service accounts, not one
- Trace the auth flow: GH OIDC → WIF pool → SA impersonation → GCP API call
- Predict what would fail if `roles/artifactregistry.admin` was missing (Cloud Run --source deploy)
- Predict what would fail if `roles/serviceusage.serviceUsageConsumer` was missing (Cloud Build)

## Key Insight

The #1 deployment failure in the lab is IAM permissions. If a student hits "PERMISSION_DENIED" in any workflow, check IAM first. The fix is always: identify which SA needs which role, grant it, wait 2 min for propagation, retry.

## Customer Talking Point

"IAM is the most common friction point when enterprises integrate CI/CD with GCP. Workload Identity Federation eliminates the key management problem, but role assignment still requires careful planning. We recommend a dedicated service account with least-privilege roles for each pipeline."
