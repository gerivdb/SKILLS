---
name: worktree-manager
description: "Git worktree management: create, list, remove worktrees for parallel branch work"
triggers:
  - /worktree
  - git worktree
  - create worktree
  - list worktrees
  - remove worktree
  - parallel branches
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - worktree
  - parallel
  - branch
phi_weight: 0.003
---

# Worktree Manager Skill

> **IntentHash**: `0xWORKTREE_MANAGER_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Manages git worktrees for working on multiple branches simultaneously without switching.

---

## Triggers

- `/worktree add <path> <branch>` — Create worktree
- `/worktree list` — List worktrees
- `/worktree remove <path>` — Remove worktree
- `git worktree` — Interactive mode
- `parallel branches` — Same as /worktree add

---

## Workflow

### Create Worktree

```powershell
# Create worktree with new branch
git worktree add ../<repo>-<feature> -b feature/<feature>

# Create worktree from existing branch
git worktree add ../<repo>-hotfix hotfix/v1.2.1
```

### List Worktrees

```powershell
git worktree list
```

### Remove Worktree

```powershell
# Remove worktree
git worktree remove ../<repo>-<feature>

# Prune stale worktrees
git worktree prune
```

---

## Examples

### Example 1: Create Worktree

```powershell
/worktree add ../brain-feature feature/mc-rnn
# → git worktree add ../brain-feature -b feature/mc-rnn
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xWORKTREE_MANAGER_SKILL_20260606` |
