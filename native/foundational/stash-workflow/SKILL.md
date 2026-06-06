---
name: stash-workflow
description: "Covers stash save, pop, apply, drop, branch-from-stash, partial stashes, and stash conflict handling"
triggers:
  - /stash
  - git stash
  - stash save
  - stash pop
  - stash apply
  - stash list
  - stash branch
  - partial stash
  - stash untracked
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - stash
  - workflow
  - wip
phi_weight: 0.005
---

# Stash Workflow Skill

> **IntentHash**: `0xSTASH_WORKFLOW_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Manages git stash operations: save, pop, apply, drop, branch-from-stash, partial stashes, and stash conflict handling. Inspects stash contents before operations.

---

## Triggers

- `/stash save [message]` — Save current changes to stash
- `/stash pop [N]` — Pop stash (apply + drop)
- `/stash apply [N]` — Apply stash (keep in stash)
- `/stash drop [N]` — Drop stash entry
- `/stash list` — List all stashes
- `/stash branch <name> [N]` — Create branch from stash
- `/stash show [N]` — Show stash contents
- `partial stash` — Stash specific files
- `stash untracked` — Include untracked files

---

## Workflow

### Inspect Before Pop

```powershell
# List stashes
git stash list

# Show stash contents BEFORE popping
git stash show -p stash@{N}

# Show including untracked files
git stash show --include-untracked -p stash@{N}
```

### Save Stash

```powershell
# Basic stash (tracked files only)
git stash push -m "WIP: feature description"

# Include untracked files
git stash push --include-untracked -m "WIP: with new files"

# Stash specific files only
git stash push -- <file1> <file2> -m "WIP: partial"

# Stash only unstaged changes (keep staged)
git stash push --keep-index -m "WIP: unstaged only"
```

### Apply Stash

```powershell
# Apply most recent stash (keeps in stash)
git stash apply

# Apply specific stash
git stash apply stash@{2}

# Apply and drop
git stash pop

# Apply with conflict handling
git stash pop
# If conflict: resolve manually, then git add <files>
# Note: git stash pop --abort does NOT exist
# To recover: git reset --hard && git stash pop
```

### Create Branch from Stash

```powershell
# Create new branch and apply stash
git stash branch new-branch-name stash@{0}
# This: creates branch at stash's parent commit, applies stash, drops it
```

### Drop Stash

```powershell
# Drop specific stash
git stash drop stash@{1}

# Clear all stashes
git stash clear
```

---

## Stash Conflict Handling

When `git stash pop` produces conflicts:

```powershell
# 1. Resolve conflicts manually
git diff --name-only --diff-filter=U

# 2. Stage resolved files
git add <resolved-files>

# 3. The stash is NOT automatically dropped on conflict
# Drop it manually after resolution
git stash drop stash@{0}

# 4. If you want to abort: restore working tree
git checkout -- .
git clean -fd
# Then re-apply: git stash apply
```

---

## Stash Decision Tree

```
Need to switch branches with uncommitted changes?
├── Changes are WIP (not ready to commit)
│   ├── Need to include untracked files?
│   │   ├── YES → git stash push --include-untracked -m "..."
│   │   └── NO  → git stash push -m "..."
│   └── Only specific files?
│       └── git stash push -- <files> -m "..."
├── Changes are ready to commit
│   └── git commit -m "..." (preferred over stash)
└── Need to save for later on SAME branch
    └── git stash push -m "WIP: ..."
```

---

## Examples

### Example 1: Save and Pop

```powershell
/stash save "WIP: MC-RNN tests"
# → git stash push -m "WIP: MC-RNN tests"

/stash pop 0
# → git stash pop stash@{0}
```

### Example 2: Partial Stash

```powershell
/stash save --files "src/brain/mc_rnn/" "WIP: MC-RNN only"
# → git stash push -- src/brain/mc_rnn/ -m "WIP: MC-RNN only"
```

### Example 3: Stash Branch

```powershell
/stash branch experiment stash@{1}
# → git stash branch experiment stash@{1}
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xSTASH_WORKFLOW_SKILL_20260606` |
