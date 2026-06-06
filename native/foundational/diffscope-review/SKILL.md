---
name: diffscope-review
description: Reviews a pull request using diffscope (or gh fallback on Windows) and posts review comments
triggers:
  - /diffscope-review
  - review pr with diffscope
  - diffscope pr
  - automated pr review
  - pr review auto
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - diffscope
  - pr
  - review
  - automated
  - code-review
phi_weight: 0.005
---

# DiffScope Review Skill

> **IntentHash**: `0xDIFFSCOPE_REVIEW_SKILL_20260606`  
> **Version**: 1.0.0  
> **Domain**: foundational  
> **Type**: foundational  
> **Status**: active

---

## Synopsis

Reviews a pull request using diffscope (Linux/macOS) or `gh` fallback (Windows) and posts review comments to GitHub.

---

## Triggers

- `/diffscope-review <PR_NUMBER>` — Review specific PR
- `review pr with diffscope` — Interactive mode
- `diffscope pr` — Same as above
- `automated pr review` — Same as above

---

## Platform Detection

```powershell
# Detect platform
if ($IsWindows -or $env:OS -eq "Windows_NT") {
    $useDiffscope = $false  # diffscope not available on Windows
} else {
    $useDiffscope = $null -ne (Get-Command diffscope -ErrorAction SilentlyContinue)
}
```

---

## Workflow

### Step 1: Get PR Details

```powershell
gh pr view <N> --json title,body,state,commits,files,additions,deletions,author
```

### Step 2: Review (Platform-Specific)

#### Option A: diffscope (Linux/macOS)

```powershell
# Review current PR
diffscope pr --number <N>

# Post comments to GitHub
diffscope pr --number <N> --post-comments
```

#### Option B: gh Fallback (Windows)

```powershell
# Get PR diff
gh pr diff <N>

# Get PR files
gh pr view <N> --json files

# Post review comment
gh pr review <N> --body "<review_comment>" --event COMMENT
```

### Step 3: Generate Review Report

```
DIFFSCOPE REVIEW REPORT — PR #236
==================================

Title: feat(mc-rnn): Phase 1 — MC-RNN layer, ArgusPass bridge, KEEL v0.6 parser
Author: gerivdb
State: OPEN
Commits: 3
Files changed: 119
Additions: 1047
Deletions: 0

REVIEW FINDINGS:
  ✅ Code structure: Clean module layout
  ✅ Tests: 35 tests, all passing
  ✅ Documentation: IntentHash + ADR references present
  ⚠️ .gitignore: logs/ added (verify no secrets in logs)
  ✅ No forbidden paths modified

VERDICT: APPROVE
```

---

## Examples

### Example 1: Review with diffscope

```powershell
/diffscope-review 236
# → diffscope pr --number 236 --post-comments
```

### Example 2: Review with gh fallback

```powershell
/diffscope-review 236
# → Windows detected, using gh fallback
# → gh pr view 236 + gh pr diff 236
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `kiva-pr-workflow`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xDIFFSCOPE_REVIEW_SKILL_20260606` |
