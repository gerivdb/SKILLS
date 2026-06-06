---
name: rebase-workflow
description: "Covers interactive rebase, rebase vs. merge decision tree, squashing, reordering, and safe rebase practices"
triggers:
  - /rebase
  - interactive rebase
  - rebase workflow
  - squash commits
  - reorder commits
  - rebase vs merge
  - git rebase
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - rebase
  - squash
  - history
  - workflow
phi_weight: 0.007
---

# Rebase Workflow Skill

> **IntentHash**: `0xREBASE_WORKFLOW_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Covers interactive rebase, rebase vs. merge decisions, squashing, reordering, and safe rebase practices. Enforces "never rebase public history" rule.

---

## Triggers

- `/rebase interactive` — Interactive rebase
- `/rebase squash` — Squash commits
- `/rebase onto <base>` — Rebase onto different base
- `rebase vs merge` — Decision guidance
- `squash commits` — Squash before merge
- `interactive rebase` — Same as /rebase interactive

---

## Rebase vs. Merge Decision Tree

```
Is the branch local-only (not pushed)?
├── YES → REBASE is safe
│   ├── Need clean history? → Interactive rebase (squash/fixup)
│   └── Just sync with main? → git rebase main
├── NO (already pushed)
│   ├── Is it your personal feature branch?
│   │   ├── YES → REBASE + force-with-lease (safe)
│   │   └── NO (shared branch) → MERGE only (never rebase)
└── Is it a PR branch?
    ├── PR review in progress? → REBASE to clean history (notify reviewers)
    └── PR ready to merge? → SQUASH MERGE via gh pr merge --squash
```

---

## Workflow

### Interactive Rebase

```powershell
# Rebase last N commits
git rebase -i HEAD~N

# Rebase onto different base
git rebase -i --onto <newbase> <oldbase> <branch>
```

**Interactive rebase actions**:

| Action | Description |
|--------|-------------|
| `pick` | Keep commit as-is |
| `reword` | Edit commit message |
| `edit` | Pause to amend commit |
| `squash` | Combine with previous (keep message) |
| `fixup` | Combine with previous (discard message) |
| `drop` | Remove commit entirely |
| `exec` | Run shell command |

### Safe Rebase (Personal Branch)

```powershell
# 1. Create backup branch
git branch backup/<branch>

# 2. Rebase
git rebase -i main

# 3. If something goes wrong, recover
git rebase --abort
git checkout backup/<branch>

# 4. Force-push with lease (safe)
git push origin <branch> --force-with-lease
```

### Squash Before Merge

```powershell
# Squash all feature branch commits into one
git checkout feature/my-feature
git rebase -i main
# Mark all but first as squash/fixup

# Or use squash merge
git checkout main
git merge --squash feature/my-feature
git commit -m "feat(scope): complete feature description"
```

### Pull with Rebase

```powershell
# Instead of git pull (which creates merge commits)
git pull --rebase origin main

# Set as default
git config --global pull.rebase true
```

---

## Safety Rules

1. **NEVER rebase `main` or `develop`** — these are public branches
2. **NEVER rebase shared branches** — only your personal feature branches
3. **Always create backup** before rebase: `git branch backup/<name>`
4. **Use `--force-with-lease`** instead of `--force` when pushing rebased branches
5. **Notify teammates** if you force-push a branch they might have pulled

---

## Recovery

```powershell
# Abort rebase in progress
git rebase --abort

# Recover from reflog if rebase went wrong
git reflog
git reset --hard HEAD@{N}

# Recover from backup branch
git checkout backup/<branch>
git branch -f <branch> backup/<branch>
git checkout <branch>
```

---

## Examples

### Example 1: Squash Last 5 Commits

```powershell
/rebase squash 5
# → git rebase -i HEAD~5, mark 4 as squash
```

### Example 2: Rebase Feature onto Latest Main

```powershell
/rebase onto main
# → git fetch origin && git rebase origin/main
```

### Example 3: Pull with Rebase

```powershell
/rebase pull
# → git pull --rebase origin main
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `create-pull-request`, `kiva-pr-workflow`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xREBASE_WORKFLOW_SKILL_20260606` |
