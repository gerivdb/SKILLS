---
name: branch-content-analyzer
description: "Detects if branch content is already in main (0 unique files = safe to delete), analyzes file overlap and commit ancestry"
triggers:
  - /analyze-branch-content
  - branch content analysis
  - is branch merged
  - branch overlap
  - check branch files
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - branch
  - analysis
  - content
  - dedup
phi_weight: 0.006
---

# Branch Content Analyzer Skill

> **IntentHash**: `0xBRANCH_CONTENT_ANALYZER_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Detects whether a branch's content is already present in main. A branch with 0 unique files (all content already merged) is safe to delete. Also analyzes file overlap percentage and commit ancestry.

---

## Triggers

- `/analyze-branch-content <branch>` — Analyze single branch
- `/analyze-branch-content --all` — Analyze all remote branches
- `is branch merged` — Quick check if branch content is in main
- `branch overlap` — Show file overlap between branch and main

---

## Workflow

### Step 1: Check Unique Files

```powershell
# Files changed in branch vs main (3-dot diff = unique to branch)
$uniqueFiles = git diff --name-only main...origin/$branch 2>$null | Where-Object {
    $_ -notmatch '__pycache__|\.pyc$|logs/|\.log$'
}
$uniqueCount = ($uniqueFiles | Measure-Object).Count
```

### Step 2: Check Commit Ancestry

```powershell
# Commits in branch not in main
$ahead = (git log --oneline main..origin/$branch 2>$null | Measure-Object).Count
# Commits in main not in branch
$behind = (git log --oneline origin/$branch..main 2>$null | Measure-Object).Count
```

### Step 3: Classify

| Condition | Classification | Action |
|-----------|---------------|--------|
| `$uniqueCount -eq 0` | `EMPTY` — all content in main | Safe to delete |
| `$uniqueCount -lt 5 -and $ahead -lt 10` | `TRIVIAL` — few unique files | Cherry-pick |
| `$uniqueCount -ge 5 -and $ahead -lt 50` | `MODERATE` — some unique content | Cherry-pick or squash |
| `$uniqueCount -ge 20 -and $ahead -ge 50` | `LARGE` — significant unique content | Squash merge |
| `$behind -gt 90` | `DIVERGED` — far behind main | Squash or manual |
| `$daysOld -gt 180` | `STALE` — old branch | Delete |

### Step 4: Output Report

```
BRANCH CONTENT ANALYSIS
=======================

env2/canonical-registry-sync
  Unique files: 0 (all content in main)
  Commits ahead: 1152 | behind: 93
  Classification: EMPTY
  → SAFE TO DELETE

feat/brain-citizen-native
  Unique files: 28
  Commits ahead: 5 | behind: 44
  Classification: MODERATE
  → CHERRY-PICK recommended
  Key files:
    .Jules/citizens/__init__.py
    .Jules/citizens/citizen_bolt.py
    .Jules/citizens/citizen_palette.py
    ...

feature/asa-v2-autopoietic-architecture
  Unique files: 0 (all content in main)
  Commits ahead: 67 | behind: 93
  Classification: EMPTY
  → SAFE TO DELETE
```

---

## Examples

### Example 1: Single Branch

```powershell
/analyze-branch-content feat/brain-citizen-native
```

### Example 2: All Branches

```powershell
/analyze-branch-content --all
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `orphan-branch-dispatcher`, `branch-merge-strategy`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xBRANCH_CONTENT_ANALYZER_SKILL_20260606` |
