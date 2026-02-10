# Student Setup Guide

Complete these steps before the lab begins. By the end, you will have your own private copy of the lab repository, dependencies installed, and Claude Code ready to go.

---

## Step 1: Create Your Private Repo from the Template

1. Open the template repository in your browser:

   ```
   https://github.com/airs-labs/prisma-airs-mlops-lab
   ```

2. Click the green **"Use this template"** button (top right, next to "Code").

3. Select **"Create a new repository"**.

4. Configure your new repo:
   - **Owner:** Select `airs-labs` (the workshop organization)
   - **Repository name:** `prisma-airs-mlops-lab-<your-name>` (e.g., `prisma-airs-mlops-lab-jsmith`)
   - **Visibility:** Select **Private**
   - **Include all branches:** Check this box -- this is required so you get both the `lab` branch (your workspace) and `main` branch (reference solutions)

5. Click **"Create repository"**.

> **Why private?** GitHub Secrets are repo-scoped. Your repo will contain GCP project IDs, AIRS credentials, and deployment configs specific to your environment. A public fork would expose these.

---

## Step 2: Clone and Switch to the Lab Branch

1. Clone your new private repo:

   ```bash
   git clone https://github.com/airs-labs/prisma-airs-mlops-lab-<your-name>.git
   cd prisma-airs-mlops-lab-<your-name>
   ```

2. Switch to the `lab` branch:

   ```bash
   git checkout lab
   ```

   The `lab` branch is your working branch. It has the pipeline structure in place but AIRS scanning is not yet integrated -- that is what you will build during the workshop.

   The `main` branch contains the completed reference implementation. You can compare against it anytime with `git diff lab..main`.

3. Connect to the template repo and sync history:

   GitHub templates create a fresh git history, which prevents you from pulling updates or submitting PRs. This step fixes that:

   ```bash
   git remote add upstream https://github.com/airs-labs/prisma-airs-mlops-lab.git
   git fetch upstream

   git checkout lab
   git reset --hard upstream/lab
   git push --force origin lab

   git checkout main
   git reset --hard upstream/main
   git push --force origin main

   git checkout lab
   ```

   > The force-push is safe because this is a fresh repo with no work yet. After this, `git pull upstream lab` will work for instructor updates, and you can submit PRs back to the template.

4. Install Python dependencies:

   ```bash
   uv sync
   ```

   > If you don't have `uv` installed: `curl -LsSf https://astral.sh/uv/install.sh | sh` then restart your terminal.

---

## Step 3: Launch Claude Code

1. Open Claude Code in the repo directory:

   ```bash
   claude
   ```

   Claude has been pre-configured as your lab mentor through the `CLAUDE.md` file in the repo root. It knows the codebase, paces its explanations, and uses Socratic questioning to guide you.

2. Start the lab by typing:

   ```
   /lab:module 0
   ```

   Module 0 walks you through verifying your GCP project, GitHub CLI, and AIRS credentials. Claude will guide you through each step.

---

## Quick Reference

| Command | What It Does |
|---------|--------------|
| `/lab:module N` | Start or resume module N |
| `/lab:verify-N` | Run verification checks for module N |
| `/hint` | Get a progressive hint for your current challenge |
| `/explore TOPIC` | Deep-dive into a concept |
| `/quiz` | Test your understanding |
| `/progress` | See your completion dashboard |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Use this template" button not visible | Make sure you are signed into GitHub and have been added to the `airs-labs` org |
| `lab` branch doesn't exist after clone | You missed "Include all branches" during template creation -- delete the repo, recreate with the checkbox checked |
| `uv: command not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` and restart your terminal |
| `claude: command not found` | Install Claude Code: `npm install -g @anthropic-ai/claude-code` |
| Claude doesn't seem to know about the lab | Make sure you're in the repo directory and on the `lab` branch -- Claude reads `CLAUDE.md` from the repo root |
