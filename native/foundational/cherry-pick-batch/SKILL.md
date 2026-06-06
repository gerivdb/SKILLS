---
name: cherry-pick-batch
description: Cherry-picks multiple commits with automatic conflict detection, skip/abort decisions, and reporting
triggers:
  - /cherry-pick-batch
  - cherry-pick multiple commits
  - batch cherry-pick
  - cherry-pick from branch
  - cherry-pick range
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
  - batch
  - workflow
phi_weight: 0.005
---

# Cherry-Pick Batch Skill

> **IntentHash**: `0xCHERRY_PICK_BATCH_SKILL_20260606`  
> **Version**: 1.0.0  
> **Domain**: foundational  
> **Type**: foundational  
> **Status**: active

---

## Synopsis

Cherry-picks multiple commits from a source branch with automatic conflict detection, skip/abort decisions, and a summary report.

---

## Triggers

- `/cherry-pick-batch <branch>` — Cherry-pick all unique commits from branch
- `/cherry-pick-batch <sha1> <sha2> ...` — Cherry-pick specific commits
- `cherry-pick multiple commits` — Interactive mode
- `batch cherry-pick` — Same as above

---

## Workflow

### Step 1: Resolve Commit List

If branch name provided:
```powershell
# Get unique commits (not in main)
git log --oneline main..<branch> | Select-Object -ExpandProperty Line
```

If commit SHAs provided: use directly.

### Step 2: Cherry-Pick Each Commit

For each commit (in chronological order):

```powershell
git cherry-pick <sha>
```

**On success**: Mark as `OK`, continue to next.

**On conflict**:
1. Report conflicted files: `git diff --name-only --diff-filter=U`
2. Mark as `CONFLICT`
3. Ask user: [s]kip / [a]bort / [m]anual resolve
4. If skip: `git cherry-pick --skip`, continue
5. If abort: `git cherry-pick --abort`, stop
6. If manual: wait for user, then `git cherry-pick --continue`

### Step 3: Generate Report

```
CHERRY-PICK BATCH REPORT
========================

Source: feat/orphan-cherry-pick
Total commits: 10

OK (8):
  ✅ ca8c114  feat(perplexity): extract perplexity bridge
  ✅ 216ba51  feat(tool_quality_standard): closes #176
  ✅ d6e5522  feat: EPIC Pilier Ouverture
  ✅ d8cce46  feat: ajout graphscope et rtp_llm modules
  ✅ ace538a  chore(wal): alignement schema ECOYSTEM
  ✅ 1460c0e  feat(brain): Migration CITIZEN_NATIVE complète
  ✅ 5e842fd  feat(citizens): Jules agents + citizens modules
  ✅ b149c8e  feat(brgs): deploy v3.0 hooks

SKIPPED (2):
  ⏭️ 453957a  feat(brgs): deploy v3.0 hooks (variante) — duplicate
  ⏭️ 9e262e3  feat(brgs): deploy v3.0 hooks (variante) — duplicate

CONFLICT (0):
  (none)

RESULT: 8/10 commits cherry-picked successfully
```

---

## Examples

### Example 1: Cherry-Pick from Branch

```powershell
/cherry-pick-batch feat/orphan-cherry-pick
```

### Example 2: Cherry-Pick Specific Commits

```powershell
/cherry-pick-batch ca8c114a21 216ba51567 d6e552267b
```

### Example 3: Interactive Mode

```powershell
/cherry-pick-batch
# Prompts for branch name or commit SHAs
```

---

## Conflict Resolution Strategy

1. **Prefer skip** for duplicate/overlapping commits
2. **Prefer abort** for fundamental incompatibilities
3. **Manual resolve** only when the commit is critical

---

## Dependencies

- **Depends on**: `branch-lifecycle` (for identifying which commits to cherry-pick)
- **Provides to**: `kiva-pr-workflow`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xCHERRY_PICK_BATCH_SKILL_20260606` |
