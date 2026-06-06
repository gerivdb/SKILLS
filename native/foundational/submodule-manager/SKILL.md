---
name: submodule-manager
description: "Git submodule lifecycle: add, update, sync, remove — validates submodule health and handles broken references"
triggers:
  - /submodule
  - git submodule
  - add submodule
  - update submodule
  - sync submodule
  - remove submodule
  - broken submodule
  - submodule status
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - submodule
  - multi-repo
  - dependency
phi_weight: 0.005
---

# Submodule Manager Skill

> **IntentHash**: `0xSUBMODULE_MANAGER_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Manages git submodule lifecycle: add, update, sync, remove. Validates submodule health and handles broken references.

---

## Triggers

- `/submodule status` — Check all submodules
- `/submodule update` — Update all submodules
- `/submodule add <url> <path>` — Add new submodule
- `/submodule remove <path>` — Remove submodule
- `broken submodule` — Diagnose and fix broken refs
- `sync submodule` — Sync all submodules

---

## Workflow

### Check Submodule Health

```powershell
# Show submodule status
git submodule status --recursive

# Check for broken submodules
git submodule foreach --quiet 'git rev-parse HEAD' 2>$null
```

### Add Submodule

```powershell
git submodule add <repo-url> <path>
git submodule init
git submodule update
git add .gitmodules <path>
git commit -m "chore: add submodule <name>"
```

### Update Submodule

```powershell
# Update to latest remote commit
git submodule update --remote <name>

# Update all submodules
git submodule update --remote --recursive

# Commit the updated pointer
git add <submodule-path>
git commit -m "chore: update submodule <name>"
```

### Sync Submodule

```powershell
# Sync URL from .gitmodules to .git/config
git submodule sync --recursive

# Then update
git submodule update --init --recursive
```

### Remove Submodule

```powershell
# 1. Deinit
git submodule deinit -f <path>

# 2. Remove from index
git rm -f <path>

# 3. Remove from .gitmodules (manual edit if last entry)
Remove-Item -Recurse -Force ".git/modules/<path>"

# 4. Commit
git commit -m "chore: remove submodule <name>"
```

### Fix Broken Submodule

```powershell
# Symptom: empty directory or wrong commit
# 1. Remove broken entry
git rm -f <path>
Remove-Item -Recurse -Force ".git/modules/<path>" -ErrorAction SilentlyContinue

# 2. Re-add
git submodule add <url> <path>
git submodule update --init --recursive
```

---

## Examples

### Example 1: Check Health

```powershell
/submodule status
# → git submodule status --recursive
```

### Example 2: Fix Broken

```powershell
/submodule fix .Jules/ontology
# → Diagnoses and repairs broken submodule
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xSUBMODULE_MANAGER_SKILL_20260606` |
