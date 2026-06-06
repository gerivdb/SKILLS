---
name: cherry-pick-conflict-resolver
description: "Extends cherry-pick-batch with conflict resolution during cherry-pick operations (binary files, rerere, manual resolve)"
triggers:
  - /cherry-pick-resolve
  - cherry-pick conflict
  - resolve cherry-pick conflict
  - cherry-pick binary conflict
  - git rerere
  - reuse recorded resolution
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - cherry-pick
  - conflict
  - resolution
  - rerere
phi_weight: 0.006
---

# Cherry-Pick Conflict Resolver Skill

> **IntentHash**: `0xCHERRY_PICK_CONFLICT_RESOLVER_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Extends `cherry-pick-batch` with conflict resolution during cherry-pick operations. Handles binary files, enables `git rerere` for recurring conflicts, and guides manual resolution.

---

## Triggers

- `/cherry-pick-resolve` — Resolve current cherry-pick conflict
- `cherry-pick conflict` — Same as above
- `resolve cherry-pick conflict` — Same as above
- `cherry-pick binary conflict` — Handle binary file conflicts
- `git rerere` — Enable reuse recorded resolution

---

## Workflow

### Step 1: Detect Conflict Type

```powershell
# List conflicted files
git diff --name-only --diff-filter=U

# Classify each
foreach ($f in $conflicted) {
    $ext = [System.IO.Path]::GetExtension($f)
    if ($ext -match '\.(png|jpg|exe|dll|zip|pdf|woff|ttf)$') {
        Write-Output "BINARY: $f"
    } else {
        Write-Output "TEXT: $f"
    }
}
```

### Step 2: Resolve by Type

#### Text Files

```powershell
# Option A: Ours (keep current branch)
git checkout --ours <file>
git add <file>

# Option B: Theirs (keep incoming commit)
git checkout --theirs <file>
git add <file>

# Option C: Manual resolution
# Edit file, remove conflict markers, then:
git add <file>
```

#### Binary Files

```powershell
# MUST choose one — no line-by-line merge
git checkout --ours <file>    # or --theirs
git add <file>
```

### Step 3: Enable Rerere (Optional but Recommended)

```powershell
# Enable reuse recorded resolution
git config --global rerere.enabled true

# After resolving once, git remembers the resolution
# Next time same conflict appears, auto-resolves
git rerere status    # show recorded resolutions
git rerere diff      # show current resolution
```

### Step 4: Continue Cherry-Pick

```powershell
# Verify no conflicts remain
git diff --name-only --diff-filter=U

# Continue
git cherry-pick --continue
```

---

## Recovery

```powershell
# Abort cherry-pick
git cherry-pick --abort

# If you continued but want to undo
git reset --hard HEAD~1
git cherry-pick <original-sha>
```

---

## Examples

### Example 1: Resolve Cherry-Pick Conflict

```powershell
/cherry-pick-resolve
# → Detects conflicted files, presents options per file
```

### Example 2: Enable Rerere

```powershell
/rerere enable
# → git config --global rerere.enabled true
```

---

## Dependencies

- **Depends on**: `cherry-pick-batch`, `merge-conflict-resolver`
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xCHERRY_PICK_CONFLICT_RESOLVER_SKILL_20260606` |
