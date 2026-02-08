# Repo & Branch Orientation

## Topics to Cover (in order)

1. Template-to-private-fork flow — how the public template became the student's private repo
2. Why private? — GitHub secrets are repo-scoped, deployment configs contain project-specific values, avoiding info disclosure
3. Branching strategy — `lab` branch (student workspace) vs `main` branch (reference/solutions)
4. Directory structure mental map — top-level dirs, how they connect
5. The 3-gate pipeline — Gate 1 train, Gate 2 publish, Gate 3 deploy, and where AIRS fits

## How to Explore

- Show the student the repo structure: `ls` top-level, explain each directory's purpose
- Read `.github/workflows/` to see the pipeline definitions
- Compare `lab` and `main` branches: `git log --oneline main..lab` or `git diff --stat main`
- Show `git remote -v` to see where `origin` points

## Student Activities

- Build a mental map: identify the 4 main areas (workflows, training, scanning, serving)
- Explain the 3-gate pipeline in their own words
- Answer: "Why scan at both Gate 1 and Gate 2?" (defense in depth — training can introduce vulnerabilities)
- @ts-workshop: Add upstream remote and verify with `git remote -v`

## Customer Talking Point

"When onboarding a customer to AIRS-secured MLOps, the first question is always: 'Walk me through your pipeline.' Understanding the gate structure — where models enter, where they're validated, where they deploy — is the foundation for every security integration conversation."
