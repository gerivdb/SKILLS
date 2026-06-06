---
name: fork-sync-workflow
description: "Fork-based contribution workflow: sync upstream, manage remotes, PR from fork"
triggers:
  - /fork-sync
  - sync fork
  - fork workflow
  - upstream sync
  - pull from upstream
  - pr from fork
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - fork
  - upstream
  - contribution
  - pr
phi_weight: 0.004
---

# Fork Sync Workflow Skill

> **IntentHash**: `0xFORK_SYNC_WORKFLOW_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Manages fork-based contribution workflows: sync fork with upstream, manage remotes, create PRs from fork.

---

## Triggers

- `/fork-sync` — Sync fork with upstream
- `sync fork` — Same as above
- `upstream sync` — Same as above
- `pr from fork` — Create PR from fork to upstream

---

## Workflow

### Setup Fork

```powershell
# 1. Add upstream remote
git remote add upstream <upstream-url>

# 2. Verify remotes
git remote -v
```

### Sync Fork

```powershell
# 1. Fetch upstream
git fetch upstream

# 2. Checkout main
git checkout main

# 3. Merge upstream changes
git merge upstream/main

# 4. Push to fork
git push origin main
```

### Create PR from Fork

```powershell
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Work and commit
git add .
git commit -m "feat: description"

# 3. Push to fork
git push origin feature/my-feature

# 4. Create PR to upstream
gh pr create --repo <upstream-owner>/<repo> --head <fork-owner>:feature/my-feature --title "..." --body "..."
```

---

## Examples

### Example 1: Sync Fork

```powershell
/fork-sync
# → Fetches upstream, merges, pushes to fork
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `create-pull-request`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xFORK_SYNC_WORKFLOW_SKILL_20260606` |
