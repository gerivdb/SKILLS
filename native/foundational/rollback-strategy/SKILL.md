---
name: rollback-strategy
description: "Guides git revert vs. git reset decisions, safe rollback procedures, and post-rollback validation"
triggers:
  - /rollback
  - git revert
  - git reset
  - undo commit
  - rollback commit
  - undo merge
  - revert merge
  - safe rollback
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - rollback
  - revert
  - reset
  - recovery
phi_weight: 0.007
---

# Rollback Strategy Skill

> **IntentHash**: `0xROLLBACK_STRATEGY_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Guides `git revert` vs. `git reset` decisions with a clear decision tree. Ensures safe rollback with backup creation and post-rollback validation.

---

## Triggers

- `/rollback <commit>` — Rollback specific commit
- `/rollback merge <commit>` — Revert a merge commit
- `git revert` — Revert guidance
- `git reset` — Reset guidance
- `undo commit` — Same as /rollback
- `undo merge` — Revert merge guidance

---

## Revert vs. Reset Decision Tree

```
Is the commit already pushed to remote?
├── YES → Use REVERT (safe, creates new commit)
│   └── git revert <commit>
└── NO (local only) → Can use RESET (rewrites history)
    ├── Want to keep changes in working tree?
    │   ├── YES → git reset --soft <commit>
    │   └── NO  → git reset --hard <commit>
    └── Want to unstage but keep files?
        └── git reset --mixed <commit> (default)
```

**RULE: Never reset pushed/shared commits. Always revert.**

---

## Workflow

### Safe Revert (Pushed Commits)

```powershell
# 1. Identify commit to revert
git log --oneline -10

# 2. Revert (creates new inverse commit)
git revert <commit-sha>

# 3. For merge commits, specify parent
git revert -m 1 <merge-commit-sha>

# 4. Push
git push origin <branch>
```

### Safe Reset (Local Only)

```powershell
# 1. Create backup branch FIRST
git branch backup/before-rollback

# 2. Reset
git reset --soft HEAD~1    # Keep changes staged
git reset --mixed HEAD~1   # Keep changes unstaged (default)
git reset --hard HEAD~1    # Discard changes entirely

# 3. If you need to recover
git checkout backup/before-rollback
```

### Revert Range

```powershell
# Revert multiple commits (oldest first)
git revert --no-commit <oldest>..<newest>
git commit -m "revert: undo feature X (commits <oldest>..<newest>)"
```

### Revert Merge Commit

```powershell
# Find merge commit
git log --oneline --merges

# Revert with parent specification
# -m 1 = keep main branch side (usually what you want)
# -m 2 = keep merged branch side
git revert -m 1 <merge-commit-sha>
```

---

## Post-Rollback Validation

```powershell
# 1. Verify history
git log --oneline -10

# 2. Run tests
pytest 2>$null

# 3. Check no unintended changes
git diff origin/<branch>

# 4. Push if clean
git push origin <branch>
```

---

## Recovery from Bad Rollback

```powershell
# If you reset too far
git reflog
git reset --hard HEAD@{N}

# If you reverted wrong commit
git revert --abort          # if in progress
git revert <revert-commit>  # revert the revert
```

---

## Examples

### Example 1: Revert Last Commit

```powershell
/rollback HEAD
# → git revert HEAD (if pushed) or git reset --soft HEAD~1 (if local)
```

### Example 2: Revert Merge

```powershell
/rollback merge abc1234
# → git revert -m 1 abc1234
```

### Example 3: Undo Last 3 Local Commits

```powershell
/rollback HEAD~3 --local --keep-changes
# → git reset --soft HEAD~3
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `kiva-pr-workflow`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xROLLBACK_STRATEGY_SKILL_20260606` |
