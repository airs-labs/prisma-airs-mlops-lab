# Module 0 Flow: Environment Setup

> INTERNAL PLAYBOOK — never shown to students.
> Engagement points tracked during module. All other scoring happens during /lab:verify-0.

## Points Available

| Source | Points | When |
|--------|--------|------|
| Engage: Pipeline gate pattern (0.1) | 1 | During flow |
| Engage: SA vs default (0.2b) | 1 | During flow |
| Engage: WIF attribute-condition (0.2b) | 1 | During flow |
| Engage: Credit consumption (0.4) | 1 | During flow |
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
| **Total** | **26** | |

---

## Challenge 0.1: Repo & Branch Orientation

### Flow

This challenge has 3 interactive beats. Do NOT rush through them — pause for the student at each beat and wait for a response before continuing. The goal is exploration and basic understanding, not a lecture.

**Beat 1: The Big Picture (README + Pipeline Diagram)**

1. Do NOT say "clone the repo" — the student already has it.

2. Start with branches — keep it brief:
   - This is a private repo created from a public template (not a fork). Briefly note why: secrets and deployment configs stay private.
   - `lab` branch: where the student works. This is their active workspace.
   - `main` branch: reference implementation and upstream state.
   - The student should stay on `lab` for all their work.

3. Brief CI/CD primer. Many students may not be familiar with GitHub Actions or CI/CD pipelines. Keep it short and concrete — no abstract theory.

   Cover in 1-2 paragraphs:
   - **CI/CD pipeline**: Automated steps that run when you push code or merge a PR. Instead of manually building, testing, and deploying, the pipeline does it for you — consistently, every time.
   - **GitHub Actions**: GitHub's built-in CI/CD system. Workflows are defined as YAML files in `.github/workflows/`. Each workflow has triggers (e.g., "run when code is pushed to `lab`") and steps (e.g., "run tests", "build container", "deploy to Cloud Run").
   - **Gates**: This lab's pipeline has 3 gates — think of them as checkpoints. Code must pass each gate before moving to the next stage. Security scans happen at each gate.

4. Show the pipeline diagram from the README (the ASCII art from the "What You'll Build" section). Display it directly — don't make the student go find it.

5. **PAUSE and ask:** "Looking at this diagram — what do you think happens to a model as it moves from Gate 1 to Gate 3? What's the pattern you see?"

   Wait for the student to respond. This is a low-stakes observation question — any reasonable reading of the diagram is fine. If they're off-base, gently redirect. The key insight: each gate adds a security checkpoint, and the model transforms at each stage (base → trained → merged → deployed).

**Beat 2: Explore GitHub Actions UI**

6. Send the student to explore the GitHub Actions UI in their browser. Give them the direct URL:
   `https://github.com/{their-repo}/actions`

   Tell them: "Go to your repo's Actions tab in the browser. Look at the **left sidebar** — that's where the individual workflows are listed by name. The main panel shows run history, which will have some failed runs from the initial repo setup — that's expected and you can ignore those for now. Focus on the workflow names in the sidebar. What workflows do you see, and which ones match the gates from the diagram?"

7. **WAIT for the student to come back.** Do NOT proceed until they report what they saw. This is the interactive beat — they need to make the connection themselves between the YAML files and the pipeline diagram.

   Expected: They should see Gate 1 (Train), Gate 2 (Publish), Gate 3 (Deploy), and Deploy App. If they also notice deploy-docs.yaml, that's just the docs site — not part of the ML pipeline.

   If they can't find it or are confused, help with navigation: repo page → "Actions" tab at the top. Direct them to the left sidebar for the clean workflow list — the main panel's failed runs from initial setup are noise.

   > ENGAGE: "You've seen the diagram and the real workflows. In a security pipeline like this, why do you think there are multiple gates instead of just one big 'scan everything at the end' step?"
   > Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
   > (Answer: defense in depth — catch issues early, different stages have different risks, a problem in training is cheaper to fix than one found at deployment. Also: different scan types apply at different stages — you can't scan a deployed model the same way you scan a raw checkpoint.)

8. Once they engage, briefly confirm and connect: "Those workflow files in `.github/workflows/` are what GitHub reads to know what to do when you push code or merge a PR. Each gate runs automatically."

**Beat 3: Directory Tour**

9. Quick directory overview — list top-level dirs and give a one-liner for each. Frame it as "now let's see where the code lives that those workflows actually run":
   - `.github/workflows/` — the 3-gate pipeline (Gate 1 train, Gate 2 publish, Gate 3 deploy)
   - `model-tuning/` — ML training code and data
   - `airs/` — AIRS scanning scripts
   - `src/` — the serving application
   - `scripts/` — utilities
   - `lab/` — lab guides and progress tracking

10. Quick check: "Can you map the directories back to the gates? For example, which directory do you think Gate 1 uses when it trains the model?"

    This is light — don't make it a quiz. If they say `model-tuning/` → great, confirm. If they're unsure, just tell them. The point is connecting structure to function, not testing recall.

**Close-out: Upstream Remote Sync**

11. Add upstream remote and sync history for instructor hotfixes. Briefly explain what you're about to do, then execute it directly (bias toward action).

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

**Hint 2 (Approach):** Start by looking at the README for the pipeline diagram. Then go to the Actions tab in your GitHub repo to see the real workflows. Try to map the workflows to the gates in the diagram.

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
   Verify GCP_WORKLOAD_IDENTITY_PROVIDER and GCP_SERVICE_ACCOUNT are now listed. Combined with AIRS secrets from Challenge 0.4, all expected secrets should be present.

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

## Challenge 0.4: Configure AIRS Model Security

> CONTEXT: Read `.claude/reference/workshop-context.md` for prereq background.
> CONTEXT: Read `.claude/reference/airs-provisioning.md` for provisioning steps.

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

**This challenge provisions AIRS Model Security early so SCM can activate while students work through Modules 1-3.** The deep exploration of Model Security features happens in Module 4.

1. **Check existing TSG from prereq lab.**
   Ask: "In the n8n Runtime Security lab, you created a TSG and deployment profile. Do you have that TSG name handy?"
   - If they have it → proceed to step 2
   - If they used their own CSP/TSG → same flow, just different CSP account
   - If they have no TSG at all → they will create a new one in step 3 (flag provisioning delay)

2. **Create Model Security deployment profile in CSP.** (SCM UI — student does this themselves, guide with navigation paths)
   Walk through:
   - Log in to CSP → Products → Software/Cloud NGFW Credits → Create Deployment Profile
   - Select: Prisma AIRS → Model Security
   - Click **Calculate Estimated Cost** to see credit impact
   - Create the profile

   > **ENGAGE**: "The cost estimate shows Model Security consumes 1500 credits flat — it just went GA last week. Why would credit consumption matter when you're talking to a customer about deploying AIRS?"
   > Award 1 pt for meaningful engagement. No wrong answers — teach if needed.
   > (Answer: budget planning, multi-product stacking, credit pool sizing, comparing to alternatives)

   Surface this context naturally: Model Security and Red Team both went GA late February 2026. Credit consumption is significantly higher than during preview/beta. Students should know this for customer conversations.

3. **Associate deployment profile to existing TSG.** (SCM UI — student does this themselves)
   This is the critical step — guide them to associate to their EXISTING tenant, NOT create a new one.
   - In CSP → find the new profile → click **Finish Setup** → redirects to Hub
   - Select CSP account → select their **existing tenant** from the n8n lab
   - Region: United States - Americas
   - Select the Model Security deployment profile → Agree → Activate

   **If they already have SCM on their TSG** (from n8n lab): activation is near-instant. Celebrate — "Since your TSG already has SCM provisioned, Model Security should activate quickly."

   **If they need a new TSG:** Flag clearly: "New TSG means SCM provisioning, which takes 15-30 minutes. That's fine — you can keep working through Modules 1-3 while it provisions. We'll verify it's ready before Module 4."

   **Important context for students:** "This TSG is your AIRS home base. You'll use it across all the AIRS labs — model security, red team, runtime. Think of it as your tenant for the entire learning path."

4. **Create service account for Model Security scanning.** (SCM UI — student does this themselves)
   IAM for AIRS is managed through Strata Cloud Manager → Common Services → Identity & Access. Mention that AIRS has granular IAM options through custom roles — but there's a known bug (see below).

   Once Model Security is activated (may need to wait if new TSG):

   - Strata Cloud Manager → Common Services → Identity & Access → Access Management
   - Select their tenant → Service Accounts → Create new
   - Name: e.g., `mlops-lab-scanner`
   - **Assign Role: Superuser** (see Known Issue below)
   - **Download the credentials immediately** — contains CLIENT_ID and CLIENT_SECRET. You cannot retrieve the secret later.
   - Note the TSG_ID from tenant details (Common Services → Tenant Management → select tenant)

   The SA is automatically scoped to the TSG they're managing.

   **Known Issue (as of March 2026):** Custom roles with Model Security permissions (`ai_ms_pypi_auth`, `ai_ms.scans`, `ai_ms.security_groups`) return HTTP 403 on all AIRS API endpoints, even when permissions are correctly enabled. Only the **Superuser** role works. This is a post-GA RBAC bug. Use this as a teaching moment:
   - The granular IAM *design* is there (good architecture)
   - The *enforcement* has a bug (real-world reality)
   - Use Superuser for POCs/labs, plan for custom roles once the fix ships
   - If a customer hits this, flag it with your SE

   If Model Security is still provisioning, skip to step 6 and come back for this step later.

5. **Set credentials via .env and GitHub secrets.**
   Guide the student to add values to `.env` (copy from `.env.example` if needed). Then set GitHub secrets:
   ```
   REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
   source .env && echo "$AIRS_MS_CLIENT_ID" | gh secret set AIRS_MS_CLIENT_ID -R "$REPO"
   source .env && echo "$AIRS_MS_CLIENT_SECRET" | gh secret set AIRS_MS_CLIENT_SECRET -R "$REPO"
   source .env && echo "$TSG_ID" | gh secret set TSG_ID -R "$REPO"
   ```

   Verify:
   ```
   gh secret list -R "$REPO"
   ```

6. **If credentials cannot be configured yet** (SCM still provisioning, no TSG, instructor not available):
   - Add blocker: `airs-credentials-missing`
   - Strong warning: "This is a hard blocker for Modules 4-7. Without AIRS credentials, you can complete Modules 0-3 (building the pipeline) and participate in Q&A discussions. However, you won't be able to run AIRS scans yourself. We'll check back before Module 4."
   - Do NOT minimize this. Do NOT just note it and move on.

7. **Provisioning note.** Tell the student: "Model Security is activating in the background. You can continue with Modules 1-3 — ML fundamentals, training, and deployment. We'll verify Model Security is ready when we hit Module 4."

### Hints

**Hint 1 (Concept):** AI Model Security is a separate capability from the AIRS Runtime API you used in the n8n lab. It requires its own deployment profile — think of it like enabling a new feature module on your existing platform tenant. The deployment profile is how licensing and feature activation work across all Prisma AIRS products.

**Hint 2 (Approach):** The key decision is associating to your EXISTING tenant, not creating a new one. If you create a new tenant, you'll have orphaned SCM instances and wasted credits. Find your TSG name from the n8n lab first.

**Hint 3 (Specific):** In CSP: Products → Software/Cloud NGFW Credits → Create Deployment Profile → Prisma AIRS → Model Security. Then Finish Setup → Hub → select your existing tenant. For credentials: Hub → Common Services → Identity & Access → Access Management → select tenant → create Service Account with **Superuser** role (custom roles have a known RBAC bug as of March 2026) → download credentials immediately.

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
