---
name: merge-conflict-resolver
description: "Interactive merge conflict resolution: detects conflicts, presents options (ours/theirs/manual), guides resolution, validates result"
triggers:
  - /resolve-conflicts
  - merge conflict
  - resolve merge conflict
  - conflict resolution
  - fix merge conflict
  - git conflict
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - merge
  - conflict
  - resolution
phi_weight: 0.008
---

# Merge Conflict Resolver Skill

> **IntentHash**: `0xMERGE_CONFLICT_RESOLVER_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Guides through interactive merge conflict resolution. Detects conflicted files, presents resolution options per file (ours/theirs/manual/binary), validates the result, and completes the merge.

---

## Triggers

- `/resolve-conflicts` — Detect and resolve all current conflicts
- `merge conflict` — Same as above
- `resolve merge conflict` — Same as above
- `conflict resolution` — Same as above
- `fix merge conflict` — Same as above

---

## Workflow

### Step 1: Detect Conflicts

```powershell
# List conflicted files
git diff --name-only --diff-filter=U

# Show conflict details per file
git diff --check
```

### Step 2: Classify Each Conflicted File

For each conflicted file, determine the type:

| Type | Extension | Strategy |
|------|-----------|----------|
| Text source | `.py`, `.js`, `.ts`, `.ps1`, `.sh` | Manual or ours/theirs |
| Binary | `.png`, `.jpg`, `.exe`, `.dll`, `.zip` | Ours or theirs only |
| Config | `.json`, `.yaml`, `.yml`, `.toml` | Manual preferred |
| Generated | `.min.js`, `.map` | Regenerate after merge |
| Lock | `package-lock.json`, `poetry.lock` | Regenerate after merge |

### Step 3: Resolve Per File

For each conflicted file, present options:

```
CONFLICTED: src/brain/mc_rnn/mc_rnn_layer.py
  1) OURS   — Keep current branch version
  2) THEIRS — Keep incoming branch version
  3) MANUAL — Open diff for manual resolution
  4) SKIP   — Defer to later

Choice [1/2/3/4]:
```

**For text files (ours/theirs)**:
```powershell
# Ours
git checkout --ours <file>
git add <file>

# Theirs
git checkout --theirs <file>
git add <file>
```

**For binary files**:
```powershell
# Must choose one — no line-by-line merge possible
git checkout --ours <file>   # or --theirs
git add <file>
```

**For manual resolution**:
```powershell
# Show conflict markers
git diff <file>
# User edits file manually, then:
git add <file>
```

### Step 4: Validate Resolution

```powershell
# Check no conflict markers remain
git diff --check

# Verify all conflicted files are staged
git diff --name-only --diff-filter=U
# Should return empty

# Run tests if available
pytest --co -q 2>$null
```

### Step 5: Complete Merge

```powershell
# For merge
git commit -m "merge: resolve conflicts from <branch>"

# For rebase
git rebase --continue

# For cherry-pick
git cherry-pick --continue
```

---

## Special Cases

### `.gitmodules` Conflicts

`.gitmodules` is INI-format — standard conflict markers break parsing:

```powershell
# Resolve section-by-section, not line-by-line
git config -f .gitmodules --list  # validate after resolution
```

### Lock File Conflicts

```powershell
# Don't manually resolve — regenerate
npm install        # for package-lock.json
poetry lock        # for poetry.lock
```

### Multiple Conflicts in Same File

```powershell
# Count conflict markers
Select-String -Path <file> -Pattern "^<<<<<<< " | Measure-Object
# Resolve each block sequentially
```

---

## Examples

### Example 1: Resolve Merge Conflict

```powershell
/resolve-conflicts
# → Detects 3 conflicted files
# → Presents options per file
# → Validates and commits
```

### Example 2: Resolve Rebase Conflict

```powershell
/resolve-conflicts --context rebase
# → Same workflow but uses git rebase --continue at end
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `cherry-pick-batch`, `cherry-pick-conflict-resolver`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xMERGE_CONFLICT_RESOLVER_SKILL_20260606` |
