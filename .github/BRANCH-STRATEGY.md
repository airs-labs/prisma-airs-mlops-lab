# Branch Strategy: main vs lab

> **Status: NEEDS REFACTORING** — This was a first-pass solution. Plans to revisit.

## The Problem

This repo has two branches with intentionally different content:

- **main**: Complete reference implementation. Clone, configure, run.
- **lab**: Workshop experience. Exercise files are intentionally stripped so students rebuild them with Claude Code as mentor.

Bug fixes and improvements land on main but need to flow to lab — **without overwriting the intentionally broken exercise files**.

## What's on Lab Only (no conflict risk)

These files only exist on lab. Merging from main never touches them:

- `lab/` — guides, topics, progress tracking
- `.claude/commands/lab/` — slash commands for the mentor
- `.claude/reference/` — AIRS tech docs, research materials
- `CLAUDE.md` — mentor persona configuration
- `docs/` — VitePress documentation site
- `leaderboard/` — instructor dashboard app

## Exercise Files (conflict risk)

These exist on both branches but are **intentionally different** on lab:

| File | What's stripped on lab | Why |
|---|---|---|
| `gate-2-publish.yaml` | No AIRS scanning, no security_group input | Students add AIRS in Module 5 |
| `gate-3-deploy.yaml` | No manifest verification, no AIRS env | Students add verification in Module 5 |
| `airs/scan_model.py` | No labels, no s3/azure, fewer groups | Students extend in Module 4-5 |
| `scanning/security.py` | No NAMED_SECURITY_GROUPS | Students discover in Module 4 |
| `scanning/__init__.py` | No NAMED_SECURITY_GROUPS export | Matches security.py |
| `README.md` | Student landing page | Different audience |

## Current Solution: .gitattributes merge=ours

On the lab branch, `.gitattributes` marks exercise files to keep lab's version during merges:

```gitattributes
.github/workflows/gate-2-publish.yaml merge=ours
.github/workflows/gate-3-deploy.yaml merge=ours
airs/scan_model.py merge=ours
# ... etc
```

### Setup (required per machine)

```bash
git config merge.ours.driver true
```

### Merge workflow

```bash
git checkout lab
git merge main
# Exercise files protected → lab's versions kept
# Shared code (Dockerfile, utilities) merges normally
# ALWAYS verify exercise files after merge
```

### Known Limitations

1. **merge=ours only fires on conflicts** — if only main changed a file and lab hasn't touched it since the last merge, git takes main's version. Always verify after merge.
2. **Per-machine config** — `git config merge.ours.driver true` needed on every fresh clone.
3. **No automation** — relies on discipline and post-merge verification.

## Alternatives Considered

**Additive exercises**: Exercise files don't exist on lab at all. Students create them from scratch. Zero conflict risk. Would require rewriting lab guides.

**Single branch**: One branch with a `solutions/` directory. Exercise mode controlled by config. Zero drift by definition.
