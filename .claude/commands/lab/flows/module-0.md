# Module 0 Flow: Environment Setup

> INTERNAL PLAYBOOK — never shown to students.
> Engagement points tracked during module. All other scoring happens during /lab:verify-0.

## Points Available

| Source | Points | When |
|--------|--------|------|
| Engage: SA vs default (0.2b) | 1 | During flow |
| Engage: WIF attribute-condition (0.2b) | 1 | During flow |
| Engage: AI assistant use case (0.5) | 1 | During flow |
| Technical: GCP Auth | 1 | During verify |
| Technical: GCP Project + naming | 3 | During verify |
| Technical: GCS Buckets | 2 | During verify |
| Technical: GCP IAM | 3 | During verify |
| Technical: GitHub CLI | 2 | During verify |
| Technical: AIRS Secrets | 3 | During verify |
| Technical: Upstream Remote | 1 | During verify |
| Quiz Q1 | 3 | During verify |
| Quiz Q2 | 3 | During verify |
| **Total** | **24** | |

---

## Challenge 0.1: Repo & Branch Orientation

### Flow

1. Do NOT say "clone the repo" — the student already has it.

2. Keep this challenge light — it's orientation, not a deep dive. Save architecture questions for later modules when they've actually used the pipeline.

3. Cover the basics:
   - This is a private repo created from a public template (not a fork). Briefly note why: secrets and deployment configs stay private.
   - `lab` branch: where the student works. This is their active workspace.
   - `main` branch: reference implementation and upstream state.
   - The student should stay on `lab` for all their work.

4. Quick directory overview — list top-level dirs and give a one-liner for each:
   - `.github/workflows/` — the 3-gate pipeline (Gate 1 train, Gate 2 publish, Gate 3 deploy)
   - `model-tuning/` — ML training code and data
   - `airs/` — AIRS scanning scripts
   - `src/` — the serving application
   - `scripts/` — utilities
   - `lab/` — lab guides and progress tracking

5. Do NOT ask deep comprehension questions here. A quick "make sense so far?" is fine. The pipeline architecture will click naturally as they work through Modules 1-3.

6. Add upstream remote and sync history for instructor hotfixes. Briefly explain what you're about to do, then execute it directly (bias toward action).

   Tell the student: "Your repo was created from a template, so it has a fresh git history separate from the template. I'm going to connect it to the template repo and sync the history so you can pull instructor updates and submit PRs back."

   Then run these commands yourself:

   Step 1 — Add the upstream remote:
   ```
   git remote add upstream https://github.com/airs-labs/prisma-airs-mlops-lab.git
   git fetch upstream
   ```

   Step 2 — Reset both branches to share upstream history:
   ```
   git checkout lab
   git reset --hard upstream/lab
   git push --force origin lab

   git checkout main
   git reset --hard upstream/main
   git push --force origin main

   git checkout lab
   ```
   After running, explain: "The force-push was safe because this is a fresh repo with no real work yet. Now your repo shares git history with the template."

   Step 3 — Verify and show results:
   - Run `git remote -v` and show both `origin` (their private repo) and `upstream` (the template).
   - Run `git log --oneline -5` and show the shared commits (not just 'Initialize lab').

### Hints

**Hint 1 (Concept):** The repo has four main areas: workflows (`.github/workflows/`), model training code (`model-tuning/`), AIRS scanning (`airs/`), and the serving application (`src/`). The `scripts/` directory has utility tools.

**Hint 2 (Approach):** Start by asking me to list the top-level directories and explain each one. Then drill into `.github/workflows/` to see the pipeline definitions. The workflow files are the backbone of the pipeline.

**Hint 3 (Specific):** The three gates are defined in `gate-1-train.yaml`, `gate-2-publish.yaml`, and `gate-3-deploy.yaml`. Each gate has security checkpoints — but in the current state, not all of them are enforcing yet. That's what you'll fix in Modules 5-7.

---

## Challenge 0.2: Verify GCP Environment

### Flow

1. Check if the student's GCP project is correctly set:
   ```
   gcloud config get-value project
   ```
   The project name should be related to the student (e.g., starts with their name or ID). It should be under the TS lab GCP folder. If the project returned is something generic or unrelated (like `ngfw-coe`), this is the wrong project.

2. If wrong project, use AskUserQuestion: "Your active GCP project is `[project]`. Is this the project you set up for the AIRS lab, or do you need to switch?"

3. Remind the student: "For the workshop, this should be **your own personal GCP project** under the lab folder — not a shared team project. That way your resources, credentials, and deployments are isolated from other participants."

4. Check billing account is linked:
   ```
   gcloud billing projects describe $(gcloud config get-value project) --format="value(billingAccountName)"
   ```

5. Check key API scopes are enabled:
   ```
   gcloud services list --enabled --format="value(config.name)" | grep -E "(aiplatform|run.googleapis|cloudbuild|storage)"
   ```
   Need: aiplatform.googleapis.com, run.googleapis.com, cloudbuild.googleapis.com, storage.googleapis.com

6. Read `.github/pipeline-config.yaml` to find the bucket configuration.

7. If staging_bucket or blessed_bucket still contains `your-model-bucket` → this is a placeholder.
   - Tell the student: "The pipeline config still has placeholder bucket names. These need to be real GCS buckets."
   - Guide them to either:
     a. Create new buckets: `gcloud storage buckets create gs://[student-name]-airs-lab-staging --location=us-central1`
     b. Use existing buckets if they have them
   - Update `.github/pipeline-config.yaml` with the real bucket names.

8. Verify the buckets are accessible:
   ```
   gcloud storage ls gs://[bucket-name]/
   ```

### Hard Blocker Check

- If GCP project is not set or not accessible → add blocker `gcp-project-invalid`
- If GCS buckets don't exist and cannot be created → add blocker `gcs-buckets-missing`
- If pipeline-config.yaml still has placeholders after this challenge → add blocker `gcs-buckets-missing`

Give a strong warning per the Hard Blockers section in CLAUDE.md. Do NOT minimize this.

---

## Challenge 0.2b: Configure GCP IAM & GitHub Actions Auth

### Concept

GitHub Actions workflows need to authenticate to GCP without storing long-lived service account keys. This is done through **Workload Identity Federation (WIF)** — a keyless authentication mechanism where GitHub's OIDC tokens are exchanged for short-lived GCP credentials.

There are **three service accounts** involved in the pipeline:

| Service Account | What It Is | What It Does |
|----------------|------------|--------------|
| **GitHub Actions SA** | You create this | Authenticates GH Actions → runs gcloud commands |
| **Compute Engine default SA** | Auto-created by GCP | Runs Vertex AI training jobs, Cloud Build builds |
| **Cloud Build SA** | Auto-created by GCP | Builds container images for Cloud Run deploys |

Each needs specific IAM roles. The most common student failure is Cloud Run `--source` deploys failing because the Compute Engine SA is missing `roles/artifactregistry.admin` or `roles/serviceusage.serviceUsageConsumer`.

### Flow

Claude should execute these steps directly (bias toward action), explaining each one as it goes.

1. **Create the GitHub Actions service account:**
   ```
   PROJECT=$(gcloud config get-value project)
   gcloud iam service-accounts create github-actions-sa \
     --display-name="GitHub Actions Service Account" \
     --project=$PROJECT
   ```

   > **ENGAGE**: "This creates a dedicated service account for your CI/CD pipeline. Why is a dedicated SA better than using the default compute SA for everything?"
   > Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
   > (Answer: least privilege, audit trail, independent rotation)

2. **Set up Workload Identity Federation:**

   Step A — Create the identity pool:
   ```
   gcloud iam workload-identity-pools create github-actions-pool \
     --location=global \
     --display-name="GitHub Actions Pool" \
     --project=$PROJECT
   ```

   Step B — Create the OIDC provider:
   ```
   gcloud iam workload-identity-pools providers create-oidc github-actions-provider \
     --location=global \
     --workload-identity-pool=github-actions-pool \
     --display-name="GitHub Actions Provider" \
     --issuer-uri="https://token.actions.githubusercontent.com" \
     --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
     --attribute-condition="assertion.repository_owner == 'airs-labs'" \
     --project=$PROJECT
   ```

   > **ENGAGE**: "What does the `attribute-condition` do? What would happen without it?"
   > Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
   > (Answer: restricts which GitHub orgs can authenticate — without it, ANY GitHub repo could impersonate this SA)

   Step C — Allow the WIF pool to impersonate the SA (scoped to just this repo):
   ```
   PROJECT_NUM=$(gcloud projects describe $PROJECT --format='value(projectNumber)')
   REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')

   gcloud iam service-accounts add-iam-policy-binding \
     github-actions-sa@${PROJECT}.iam.gserviceaccount.com \
     --project=$PROJECT \
     --role="roles/iam.workloadIdentityUser" \
     --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUM}/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/${REPO}"
   ```

3. **Assign IAM roles to the GitHub Actions SA:**
   ```
   SA=github-actions-sa@${PROJECT}.iam.gserviceaccount.com

   for ROLE in \
     roles/aiplatform.user \
     roles/storage.admin \
     roles/run.admin \
     roles/artifactregistry.admin \
     roles/cloudbuild.builds.editor \
     roles/logging.logWriter \
     roles/iam.serviceAccountUser \
     roles/serviceusage.serviceUsageConsumer; do
     gcloud projects add-iam-policy-binding $PROJECT \
       --member="serviceAccount:$SA" --role="$ROLE" --quiet --no-user-output-enabled
     echo "  $ROLE"
   done
   ```

   After running, walk through what each role enables:
   | Role | Why It's Needed |
   |------|----------------|
   | `aiplatform.user` | Submit Vertex AI training jobs, manage endpoints |
   | `storage.admin` | Read/write model artifacts in GCS |
   | `run.admin` | Deploy and manage Cloud Run services |
   | `artifactregistry.admin` | Create repos and push container images |
   | `cloudbuild.builds.editor` | Trigger Cloud Build for `--source` deploys |
   | `logging.logWriter` | Write logs from Cloud Run and Vertex AI |
   | `iam.serviceAccountUser` | Act as other SAs (needed for Cloud Run deploy) |
   | `serviceusage.serviceUsageConsumer` | Use project APIs (Cloud Build requires this) |

4. **Grant Compute Engine default SA the roles it needs:**
   ```
   COMPUTE_SA="${PROJECT_NUM}-compute@developer.gserviceaccount.com"

   for ROLE in \
     roles/storage.objectAdmin \
     roles/aiplatform.user \
     roles/artifactregistry.admin \
     roles/cloudbuild.builds.builder \
     roles/run.admin \
     roles/serviceusage.serviceUsageConsumer \
     roles/logging.logWriter; do
     gcloud projects add-iam-policy-binding $PROJECT \
       --member="serviceAccount:$COMPUTE_SA" --role="$ROLE" --quiet --no-user-output-enabled
     echo "  Compute SA: $ROLE"
   done
   ```
   Explain: "The Compute Engine default SA runs your Vertex AI training jobs and Cloud Build container builds. It needs storage access for GCS FUSE mounts during training, and artifact registry access to push container images."

5. **Set GitHub secrets for WIF:**
   ```
   WIF_PROVIDER="projects/${PROJECT_NUM}/locations/global/workloadIdentityPools/github-actions-pool/providers/github-actions-provider"

   echo "$WIF_PROVIDER" | gh secret set GCP_WORKLOAD_IDENTITY_PROVIDER
   echo "github-actions-sa@${PROJECT}.iam.gserviceaccount.com" | gh secret set GCP_SERVICE_ACCOUNT
   gh secret list
   ```
   Should now show 5 secrets: the 3 AIRS secrets + 2 GCP secrets.

### Hard Blocker Check

If the SA cannot be created or WIF cannot be configured (e.g., missing permissions on the GCP project), add blocker `gcp-iam-invalid`. This blocks all pipeline execution (Modules 2-7).

---

## Challenge 0.3: Verify GitHub CLI

### Flow

1. Bias toward running checks yourself, but confirm first. Use AskUserQuestion:
   "I can verify your GitHub CLI setup by running a few commands (gh auth status, gh repo view, gh workflow list). Want me to go ahead?"

2. Run the checks:
   ```
   gh auth status
   gh repo view --json name,owner
   gh workflow list
   ```

3. Verify:
   - Authenticated as the correct GitHub user
   - Can see the repo
   - Four workflows visible: Gate 1 (Train), Gate 2 (Publish), Gate 3 (Deploy), Deploy App

4. Brief explanation: "The `gh` CLI is how you'll trigger pipeline runs, check workflow status, and read logs — all without leaving your terminal."

---

## Challenge 0.4: Configure AIRS Access

### Credential Handling (IMPORTANT)

**Always encourage students to use a `.env` file** rather than pasting credentials directly into the chat. The repo includes a `.env.example` template. Students should:
1. Copy `.env.example` to `.env` (already gitignored)
2. Fill in their credentials there
3. The mentor reads from `.env` to set GitHub secrets — no secrets in chat history

When setting GitHub secrets, source the `.env` file and pipe values. Derive the repo name for the `-R` flag:
```
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
source .env && echo "$AIRS_MS_CLIENT_ID" | gh secret set AIRS_MS_CLIENT_ID -R "$REPO"
```

### Flow

1. Check if the student has their AIRS credentials. If not, direct them to their instructor:
   "If you don't have your AIRS credentials yet, see your instructor to get your **authcode** and **TSG** provisioned. They'll walk you through SCM Apps Hub access and service account creation. You can download your credentials as a CSV from SCM. Come back here once you have your CLIENT_ID, CLIENT_SECRET, and TSG_ID."

2. Briefly explain what the three credentials are:
   - **AIRS_MS_CLIENT_ID**: OAuth2 client ID for the AIRS service account
   - **AIRS_MS_CLIENT_SECRET**: OAuth2 client secret
   - **TSG_ID**: Tenant Service Group ID — identifies which AIRS tenant to scan against

3. Use AskUserQuestion:
   "Do you have the CLIENT_ID, CLIENT_SECRET, and TSG_ID from your AIRS service account?"

4. If they have credentials, guide them to put values in `.env`:
   - "Add your credentials to the `.env` file (copy from `.env.example` if you haven't already). Don't paste them directly in chat — the `.env` file is gitignored and safer."
   - Once `.env` is ready, source it and set GitHub secrets (bias toward action — run the commands yourself):
     ```
     REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
     source .env && echo "$AIRS_MS_CLIENT_ID" | gh secret set AIRS_MS_CLIENT_ID -R "$REPO"
     source .env && echo "$AIRS_MS_CLIENT_SECRET" | gh secret set AIRS_MS_CLIENT_SECRET -R "$REPO"
     source .env && echo "$TSG_ID" | gh secret set TSG_ID -R "$REPO"
     ```

5. Verify secrets are set:
   ```
   gh secret list -R "$REPO"
   ```
   Should show all three secrets.

6. If they don't have credentials:
   - Add blocker: `airs-credentials-missing`
   - Strong warning: "This is a hard blocker. Without AIRS credentials, you can complete Modules 0-3 (building the pipeline) and participate in Q&A discussions for all modules. However, you won't be able to run AIRS scans yourself in Modules 4-7. See your instructor to get set up."

### Hints

**Hint 1 (Concept):** GitHub repository secrets are encrypted variables that only GitHub Actions workflows can read at runtime. Nobody can view the actual values after they're set. The AIRS SDK uses OAuth2 client credentials to authenticate scan requests.

**Hint 2 (Approach):** Use `gh secret set` for each of the three values. The `.env` file keeps secrets out of chat history. Use `gh secret list` to verify they're set (names only, values are hidden).

**Hint 3 (Specific):** Copy `.env.example` to `.env`, fill in your values, then run the gh secret set commands with `-R` flag pointing to your repo.

---

## Challenge 0.5: Meet Your Assistant

### Flow

1. Have the student look at `CLAUDE.md` in the repo root. Ask: "What stands out to you about how I've been configured for this lab?"

2. If they ask you to explain it instead of reading it, that's fine — walk through the key points:
   - Socratic mentor role (questions, not lectures)
   - Pacing rules (1-2 paragraphs, always end with a question)
   - Available commands and what each does
   - Progressive hint system

3. > **ENGAGE**: "Can you think of a use case at your own work where a customized AI assistant like this would be useful?"
   > Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
   > This is open-ended — the point is connecting CLAUDE.md to real enterprise patterns.

4. Test the interaction: have them ask you a real question about AIRS or the pipeline to see the mentor style in action.
