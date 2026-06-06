---
name: branch-lifecycle
description: Analyzes all branches in a git repository and recommends PR merge / cherry-pick / delete strategy for each
triggers:
  - /branch-lifecycle
  - analyze branches
  - branch strategy
  - which branches to merge
  - branch cleanup
  - branch analysis
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
  - workflow
  - pr
  - cherry-pick
phi_weight: 0.005
---

# Branch Lifecycle Skill

> **IntentHash**: `0xBRANCH_LIFECYCLE_SKILL_20260606`  
> **Version**: 1.0.0  
> **Domain**: foundational  
> **Type**: foundational  
> **Status**: active

---

## Synopsis

Analyzes all branches (local + remote + stash) in a git repository and recommends a strategy for each: **PR_MERGE** | **CHERRY_PICK** | **DELETE** | **KEEP**.

---

## Triggers

- `/branch-lifecycle` — Full analysis of all branches
- `analyze branches` — Same as above
- `branch strategy` — Same as above
- `which branches to merge` — Filter to PR_MERGE recommendations
- `branch cleanup` — Filter to DELETE recommendations

---

## Workflow

### Step 1: Gather Data

```powershell
# List all local branches
git branch -v

# List all remote branches
git branch -r

# List stashes
git stash list

# Get default branch
git symbolic-ref refs/remotes/origin/HEAD
```

### Step 2: Analyze Each Branch

For each branch, compute:

```powershell
# Commits ahead of main
git log --oneline main..<branch> | Measure-Object -Line

# Commits behind main
git log --oneline <branch>..main | Measure-Object -Line

# Files changed vs main
git diff --stat main...<branch>

# Check if branch has associated PR
gh pr list --head <branch> --state all
```

### Step 3: Classify

| Condition | Classification | Action |
|-----------|---------------|--------|
| Has open PR, clean history | `PR_MERGE` | Create/merge PR |
| Already merged into main | `DELETE` | Delete local + remote |
| Diverged, partial overlap with main | `CHERRY_PICK` | Cherry-pick unique commits |
| No commits ahead of main | `DELETE` | Delete (stale) |
| Active development, not ready | `KEEP` | Do nothing |

### Step 4: Output Report

```
BRANCH LIFECYCLE REPORT
=======================

PR_MERGE (1):
  feature/mc-rnn-layer    3 commits ahead, 0 behind, 119 files changed

CHERRY_PICK (1):
  feat/orphan-cherry-pick 10 commits ahead, 0 behind, mixed content

DELETE (1):
  feature/extract-tql     Already merged (PR #235)

STALE (1):
  stash@{0}               WIP on feature/extract-tql (pycache only)
```

### Step 5: Execute (with confirmation)

For each classified branch, ask user confirmation before executing the recommended action.

---

## Examples

### Example 1: Full Analysis

```powershell
/branch-lifecycle
```

Output:
```
Analyzing 4 branches + 1 stash...

  feature/mc-rnn-layer       → PR_MERGE (3 commits, clean)
  feat/orphan-cherry-pick    → CHERRY_PICK (10 commits, mixed)
  feature/extract-tql        → DELETE (already merged)
  stash@{0}                  → DELETE (pycache only)

Execute recommendations? [y/N]
```

### Example 2: Filter to Mergeable

```powershell
/branch-lifecycle --filter PR_MERGE
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `cherry-pick-batch`, `kiva-pr-workflow`, `sync-branches`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xBRANCH_LIFECYCLE_SKILL_20260606` |
