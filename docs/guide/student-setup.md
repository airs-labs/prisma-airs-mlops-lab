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

4. Configure your new repo (see screenshot below):
   - **Include all branches:** Toggle **On** -- this is required so you get both the `lab` branch (your workspace) and `main` branch (reference solutions)
   - **Owner:** Select `airs-labs` (the workshop organization)
   - **Repository name:** `<your-name>-prisma-airs-mlops-lab` (e.g., `syoungberg-prisma-airs-mlops-lab`)
   - **Visibility:** Select **Private**

5. Click **"Create repository"**.

![Create repo from template](/create-repo-from-template.png)

> **Why private?** GitHub Secrets are repo-scoped. Your repo will contain GCP project IDs, AIRS credentials, and deployment configs specific to your environment. A public fork would expose these.

---

## Step 2: Clone and Switch to the Lab Branch

1. Clone your new private repo:

   ```bash
   git clone https://github.com/airs-labs/<your-name>-prisma-airs-mlops-lab.git
   cd <your-name>-prisma-airs-mlops-lab
   ```

2. Switch to the `lab` branch:

   ```bash
   git checkout lab
   ```

   The `lab` branch is your working branch. It has the pipeline structure in place but AIRS scanning is not yet integrated -- that is what you will build during the workshop.

   The `main` branch contains the completed reference implementation. You can compare against it anytime with `git diff lab..main`.

3. Install Python dependencies:

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

   Module 0 walks you through verifying your GCP project, GitHub CLI, and AIRS credentials. Claude will also help you connect your repo to the template for receiving instructor updates.

---

## Quick Reference

| Command | What It Does |
|---------|--------------|
| `/lab:module N` | Start or resume module N |
| `/lab:verify-N` | Run verification checks for module N |
| `/lab:hint` | Get a progressive hint for your current challenge |
| `/lab:explore TOPIC` | Deep-dive into a concept |
| `/lab:quiz` | Test your understanding |
| `/lab:progress` | See your completion dashboard |

---

## Resuming Work Between Sessions

When you come back to the lab after closing your terminal or starting a new day, you need two things: your Claude Code context back, and any instructor updates pulled in.

### Step 1: Resume Your Claude Code Session

Open Claude Code in your repo directory and use the resume command:

```bash
cd <your-name>-prisma-airs-mlops-lab
claude
```

Then type:

```
/resume
```

This recovers your previous session context — Claude will remember where you left off, what module you were on, and what you were working on.

### Step 2: Pull Instructor Updates

After resuming, paste this prompt to have Claude set up the upstream remote (if needed) and pull the latest changes:

```
Check if I have an "upstream" remote pointing to airs-labs/prisma-airs-mlops-lab.
If not, add it. Then fetch upstream and merge upstream/lab into my current branch.
If there are merge conflicts on lab/.progress.json or .github/pipeline-config.yaml,
keep my version (--ours) since those have my personal config. For everything else,
take upstream's version (--theirs).
```

Claude will handle the git commands and resolve any conflicts automatically.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Use this template" button not visible | Make sure you are signed into GitHub and have been added to the `airs-labs` org |
| `lab` branch doesn't exist after clone | You missed "Include all branches" during template creation -- delete the repo, recreate with the toggle on |
| `uv: command not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` and restart your terminal |
| `claude: command not found` | Install Claude Code: `npm install -g @anthropic-ai/claude-code` |
| Claude doesn't seem to know about the lab | Make sure you're in the repo directory and on the `lab` branch -- Claude reads `CLAUDE.md` from the repo root |
| Merge conflict on `lab/.progress.json` | Keep your version: `git checkout --ours lab/.progress.json && git add lab/.progress.json && git commit --no-edit` |
| `upstream` remote not found | Add it: `git remote add upstream https://github.com/airs-labs/prisma-airs-mlops-lab.git` |
