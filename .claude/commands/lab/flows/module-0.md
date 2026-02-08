# Module 0 Flow: Environment Setup

## Points Available

| Source | Points | Track |
|--------|--------|-------|
| Challenge 0.1: Repo orientation | 2 | @all |
| Challenge 0.1: Upstream remote | 1 | @ts-workshop |
| Challenge 0.2: GCP project | 3 | @all |
| Challenge 0.2: GCS buckets | 2 | @all |
| Challenge 0.2: Project validation bonus | 2 | @ts-workshop |
| Challenge 0.3: GitHub CLI | 2 | @all |
| Challenge 0.4: AIRS secrets configured | 3 | @all |
| Challenge 0.4: SCM API SA creation | 4 | @ts-workshop |
| Challenge 0.5: Meet assistant | 1 | @all |
| Quiz (2 questions) | 6 | @all |
| **Total** | **16-26** | |

---

## Challenge 0.1: Repo & Branch Orientation

### Flow (@all)

1. Do NOT say "clone the repo" — the student already has it.

2. Start with the big picture. Ask: "You're in a private repository that was created from a public template. Why do you think the lab uses a private repo instead of a public fork?"
   - Expected answer: GitHub secrets would be visible, deployment configs, info disclosure
   - If they struggle: hint that GitHub Actions secrets are repo-scoped

3. Explain the branching strategy:
   - `lab` branch: where the student works. This is their active workspace.
   - `main` branch: reference implementation. Contains documentation, solutions, and the upstream state.
   - The student should stay on `lab` for all their work.

4. Guide the mental map exploration. This worked well — ask them:
   - "What's the overall architecture of this project?"
   - Walk through the directory structure: `.github/workflows/`, `model-tuning/`, `airs/`, `src/`, `scripts/`, `app/`
   - Explain the 3-gate pipeline: Gate 1 (scan + train), Gate 2 (merge + scan + publish), Gate 3 (verify provenance + deploy)

5. Ask comprehension: "Why do you think they scan at both Gate 1 and Gate 2, not just once?"
   - Expected: training could introduce vulnerabilities, insider threat, defense in depth

### Flow (@ts-workshop)

6. Add upstream remote for instructor hotfixes:
   "Your instructor may push fixes during the workshop. Let's add the template repo as an upstream remote so you can pull those in."
   ```
   git remote add upstream https://github.com/PaloAltoNetworks/prisma-airs-mlops-lab.git
   git fetch upstream
   ```
   Verify: `git remote -v` should show both `origin` (their private repo) and `upstream` (the template).

### Hints

**Hint 1 (Concept):** The repo has four main areas: workflows (`.github/workflows/`), model training code (`model-tuning/`), AIRS scanning (`airs/`), and the serving application (`src/`). The `scripts/` directory has utility tools.

**Hint 2 (Approach):** Start by asking me to list the top-level directories and explain each one. Then drill into `.github/workflows/` to see the pipeline definitions. The workflow files are the backbone of the pipeline.

**Hint 3 (Specific):** The three gates are defined in `gate-1-train.yaml`, `gate-2-publish.yaml`, and `gate-3-deploy.yaml`. Each gate has security checkpoints — but in the current state, not all of them are enforcing yet. That's what you'll fix in Modules 5-7.

### Points

- Student can describe the 3-gate pipeline and explain scan-at-both-points: **2 pts**
- @ts-workshop: upstream remote configured: **1 pt**

---

## Challenge 0.2: Verify GCP Environment

### Flow (@ts-workshop)

1. Check if the student's GCP project is correctly set:
   ```
   gcloud config get-value project
   ```
   The project name should be related to the student (e.g., starts with their name or ID). It should be under the TS lab GCP folder. If the project returned is something generic or unrelated (like `ngfw-coe`), this is the wrong project.

2. If wrong project, use AskUserQuestion: "Your active GCP project is `[project]`. Is this the project you set up for the AIRS lab, or do you need to switch?"

3. Check billing account is linked:
   ```
   gcloud billing projects describe $(gcloud config get-value project) --format="value(billingAccountName)"
   ```

4. Check key API scopes are enabled:
   ```
   gcloud services list --enabled --format="value(config.name)" | grep -E "(aiplatform|run.googleapis|cloudbuild|storage)"
   ```
   Need: aiplatform.googleapis.com, run.googleapis.com, cloudbuild.googleapis.com, storage.googleapis.com

5. Proceed to GCS bucket check (shared with @self-paced below).

### Flow (@self-paced)

1. Verify any valid GCP project with working auth:
   ```
   gcloud auth list
   gcloud config get-value project
   ```
   Confirm they have an active account and a project set.

2. Proceed to GCS bucket check (shared below).

### Flow (@all) — GCS Bucket Check

1. Read `.github/pipeline-config.yaml` to find the bucket configuration.
2. If staging_bucket or blessed_bucket still contains `your-model-bucket` → this is a placeholder.
   - Tell the student: "The pipeline config still has placeholder bucket names. These need to be real GCS buckets."
   - Guide them to either:
     a. Create new buckets: `gcloud storage buckets create gs://[student-name]-airs-lab-staging --location=us-central1`
     b. Use existing buckets if they have them
   - Update `.github/pipeline-config.yaml` with the real bucket names.

3. Verify the buckets are accessible:
   ```
   gcloud storage ls gs://[bucket-name]/
   ```

### Hard Blocker Check

- If GCP project is not set or not accessible → add blocker `gcp-project-invalid`
- If GCS buckets don't exist and cannot be created → add blocker `gcs-buckets-missing`
- If pipeline-config.yaml still has placeholders after this challenge → add blocker `gcs-buckets-missing`

Give a strong warning per the Hard Blockers section in CLAUDE.md. Do NOT minimize this.

### Hints

**Hint 1 (Concept):** GCP authentication has two layers: your local CLI auth (for running commands from your terminal) and Application Default Credentials / Workload Identity (for GitHub Actions to authenticate to GCP). This challenge focuses on the local CLI layer.

**Hint 2 (Approach):** Use `gcloud` commands to check your auth status, active project, and verify you can list objects in the staging bucket. The pipeline config file tells you what bucket names to expect.

**Hint 3 (Specific):** Run `gcloud auth list`, `gcloud config get-value project`, then check `.github/pipeline-config.yaml` for bucket names and run `gcloud storage ls` on them.

### Points

- GCP project correctly set and accessible: **3 pts**
- GCS buckets exist and pipeline-config updated: **2 pts**
- @ts-workshop: correct project under TS lab folder: **2 pts bonus**

---

## Challenge 0.3: Verify GitHub CLI

### Flow (@all)

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

### Hints

**Hint 1 (Concept):** The `gh` CLI is how you interact with GitHub Actions without leaving your terminal. You need it to trigger workflows, check run status, and read logs.

**Hint 2 (Approach):** Check your auth status, then verify you can see the repository and its workflows.

**Hint 3 (Specific):** Run `gh auth status`, `gh repo view`, `gh workflow list`. You should see four workflows.

### Points

- GH CLI authenticated, repo visible, workflows listed: **2 pts**

---

## Challenge 0.4: Configure AIRS Access

### Flow (@ts-workshop) — THE WOW MOMENT

This challenge demonstrates Claude's ability to work with APIs in real time. The student will see Claude use Context7 and the SCM API to create a service account — showcasing what's possible with AI-assisted operations.

1. Check prework. Use AskUserQuestion:
   "Your prework included creating a service account in SCM Apps Hub with IAM permissions. Do you have the CLIENT_ID, CLIENT_SECRET, and TSG_ID from that service account?"

2. If they have credentials from prework, proceed to step 5.

3. THE WOW MOMENT — Create a new service account via SCM API:
   a. Explain: "Let's create a new service account that has ONLY model security API permissions. This follows the principle of least privilege — the scanning pipeline should only be able to submit scans and read results."
   b. Use Context7 to look up the SCM IAM API documentation for service account creation.
   c. The goal: Create a service account in the student's AIRS child TSG with a custom role that has ONLY these permissions:
      - Model security scan submission
      - Model security scan result reading
      - No security group management
      - No user management
      - No policy modification
   d. Use the student's parent TSG service account credentials to authenticate to the SCM API.
   e. Walk through what you're doing and why — this is a learning moment, not a magic trick.
   f. Verify the new SA can perform a scan (or at least authenticate).

4. Award bonus points for the SCM API exercise.

5. Set GitHub secrets with the credentials:
   ```
   gh secret set MODEL_SECURITY_CLIENT_ID
   gh secret set MODEL_SECURITY_CLIENT_SECRET
   gh secret set TSG_ID
   ```
   Each command will prompt the student to paste the value.

6. Verify secrets are set:
   ```
   gh secret list
   ```
   Should show all three secrets.

### Flow (@self-paced)

1. Explain what the three credentials are:
   - **MODEL_SECURITY_CLIENT_ID**: OAuth2 client ID for the AIRS service account
   - **MODEL_SECURITY_CLIENT_SECRET**: OAuth2 client secret (the password)
   - **TSG_ID**: Tenant Service Group ID — identifies which AIRS tenant to scan against

2. Where to get them:
   - From your Prisma Cloud / Strata Cloud Manager (SCM) tenant
   - SCM → Settings → Service Accounts
   - Your organization's AIRS administrator can provision these

3. Use AskUserQuestion:
   "Do you already have your AIRS credentials (CLIENT_ID, CLIENT_SECRET, TSG_ID), or do you still need to set them up?"
   Options:
   - "I have them ready"
   - "I don't have them yet"

4. If they have them → proceed to gh secret set (same as step 5 above)

5. If they don't have them:
   - Add blocker: `airs-credentials-missing`
   - Strong warning: "Without AIRS credentials, you can complete Modules 0-3 (building the pipeline) and participate in Q&A discussions for all modules. However, you won't be able to run AIRS scans yourself in Modules 4-7. If you get credentials later, we can come back and configure them."
   - Do NOT just casually note it and move on. This is a hard blocker for the security scanning portions of the lab.

### Hints

**Hint 1 (Concept):** GitHub repository secrets are encrypted variables that only GitHub Actions workflows can read at runtime. Nobody can view the actual values after they're set. The AIRS SDK uses OAuth2 client credentials to authenticate scan requests.

**Hint 2 (Approach):** Use `gh secret set` for each of the three values. The command will prompt you to paste the value interactively. Use `gh secret list` to verify they're set (names only, values are hidden).

**Hint 3 (Specific):** Run these commands one at a time, pasting each value when prompted:
```
gh secret set MODEL_SECURITY_CLIENT_ID
gh secret set MODEL_SECURITY_CLIENT_SECRET
gh secret set TSG_ID
gh secret list
```

### Points

- All three secrets configured: **3 pts**
- @ts-workshop: SCM API SA creation exercise completed: **4 pts bonus**

---

## Challenge 0.5: Meet Your Assistant

### Flow (@all)

1. Have the student look at `CLAUDE.md` in the repo root. Ask: "What stands out to you about how I've been configured for this lab?"

2. If they ask you to explain it instead of reading it, that's fine — walk through the key points:
   - Socratic mentor role (questions, not lectures)
   - Pacing rules (1-2 paragraphs, always end with a question)
   - Available commands and what each does
   - Progressive hint system

3. Ask a comprehension question: "Can you think of a use case at your own work where a customized AI assistant like this would be useful?"
   - This is open-ended, no wrong answer. The point is connecting CLAUDE.md to real enterprise patterns.

4. Test the interaction: have them ask you a real question about AIRS or the pipeline to see the mentor style in action.

### Hints

**Hint 1 (Concept):** CLAUDE.md is a configuration file that shapes how Claude Code behaves in this specific project. It's not code — it's natural language rules.

**Hint 2 (Approach):** Open CLAUDE.md and read the "Your Role", "Pacing Rules", and "Available Commands" sections.

**Hint 3 (Specific):** Ask me: "Read CLAUDE.md and tell me what rules you follow in this lab."

### Points

- Student demonstrates understanding of CLAUDE.md and the mentor model: **1 pt**

---

## End-of-Module Quiz

Present during `/verify-0`. Two questions, one at a time.

### Question 1 (Concept)

"Why does the lab use a private repo created from the template, instead of a public fork?"

**Expected answer:** GitHub secrets would be exposed in a public repo. The repo contains deployment configurations, bucket names, and workflow definitions that could enable info disclosure. Private repos keep secrets scoped and deployment details hidden.

**Scoring:**
- 3 pts: mentions secrets exposure AND deployment config / info disclosure
- 2 pts: mentions one of the above
- 1 pt: vague answer about "security" without specifics
- 0 pts: cannot answer

### Question 2 (Applied)

"If `.github/pipeline-config.yaml` still has `your-model-bucket` as the staging bucket, what will break and when?"

**Expected answer:** Gate 1 training output has nowhere to go (GCS write fails). Gate 2 merge can't find artifacts. The pipeline fails at the first GCS operation — it won't be a subtle error, it will be an immediate failure when any workflow tries to read or write model artifacts.

**Scoring:**
- 3 pts: identifies specific failure point (GCS operations in workflows) and explains the cascade
- 2 pts: knows it will break but vague on where/when
- 1 pt: needed a hint to answer
- 0 pts: cannot answer

**Max quiz score: 6 points**
