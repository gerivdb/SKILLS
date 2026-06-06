---
name: clean-pycache
description: Removes __pycache__ directories and .pyc files from working tree and git index, ensures .gitignore coverage
triggers:
  - /clean-pycache
  - clean pycache
  - remove pyc files
  - pycache cleanup
  - clean python cache
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - python
  - pycache
  - cleanup
  - .gitignore
phi_weight: 0.003
---

# Clean Pycache Skill

> **IntentHash**: `0xCLEAN_PYCACHE_SKILL_20260606`  
> **Version**: 1.0.0  
> **Domain**: foundational  
> **Type**: foundational  
> **Status**: active

---

## Synopsis

Removes `__pycache__/` directories and `.pyc` files from both the working tree and git index, and ensures `.gitignore` has proper coverage.

---

## Triggers

- `/clean-pycache` — Full cleanup (index + working tree + .gitignore)
- `clean pycache` — Same as above
- `remove pyc files` — Same as above
- `pycache cleanup` — Same as above

---

## Workflow

### Step 1: Find Pycache Files

```powershell
# Find all __pycache__ directories
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue

# Find all .pyc files
Get-ChildItem -Path . -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue

# Check git index for tracked pyc files
git ls-files | Select-String "\.pyc$"
git ls-files | Select-String "__pycache__"
```

### Step 2: Remove from Git Index

```powershell
# Remove all tracked __pycache__ from index
git rm --cached -r src/__pycache__/
git rm --cached -r tests/__pycache__/
# (repeat for each directory found)

# Or remove all at once
git ls-files | Select-String "__pycache__" | ForEach-Object { git rm --cached -r $_.Line }
```

### Step 3: Remove from Working Tree

```powershell
# Remove __pycache__ directories
Remove-Item -Recurse -Force "src\__pycache__"
Remove-Item -Recurse -Force "tests\__pycache__"
# (repeat for each directory found)
```

### Step 4: Verify .gitignore

Check that `.gitignore` contains:
```
__pycache__/
*.py[cod]
*$py.class
```

If not present, append:
```powershell
Add-Content -Path .gitignore -Value "`n# Python cache`n__pycache__/`n*.py[cod]`n*$py.class"
```

### Step 5: Report

```
PYCACHE CLEANUP REPORT
=======================

Files removed from index: 96
  - src/__pycache__/: 11 files
  - tests/__pycache__/: 85 files

Files removed from working tree: 96
  - src/__pycache__/: 1 directory
  - tests/__pycache__/: 1 directory

.gitignore: ✅ Already contains __pycache__/ and *.py[cod]

Working tree status: ✅ Clean (no pyc files remaining)
```

---

## Examples

### Example 1: Full Cleanup

```powershell
/clean-pycache
```

### Example 2: Dry Run

```powershell
/clean-pycache --dry-run
# Shows what would be removed without actually removing
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xCLEAN_PYCACHE_SKILL_20260606` |
