---
name: sync-branches
description: Synchronizes local and remote branches, detects already-merged branches, and cleans up stale references
triggers:
  - /sync-branches
  - sync branches local remote
  - cleanup merged branches
  - delete merged branches
  - branch sync
  - prune branches
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
  - sync
  - cleanup
  - prune
phi_weight: 0.005
---

# Sync Branches Skill

> **IntentHash**: `0xSYNC_BRANCHES_SKILL_20260606`  
> **Version**: 1.0.0  
> **Domain**: foundational  
> **Type**: foundational  
> **Status**: active

---

## Synopsis

Synchronizes local and remote branches, detects already-merged branches via `gh pr list`, and cleans up stale references.

---

## Triggers

- `/sync-branches` — Full sync (fetch prune + detect merged + cleanup)
- `sync branches local remote` — Same as above
- `cleanup merged branches` — Only cleanup merged branches
- `delete merged branches` — Same as above
- `branch sync` — Same as above

---

## Workflow

### Step 1: Fetch and Prune

```powershell
git fetch --prune
```

This removes remote-tracking branches that no longer exist on remote.

### Step 2: Detect Merged Branches

```powershell
# Get all local branches merged into main
git branch --merged main --format="%(refname:short)"

# For each merged branch, check PR status
gh pr list --head <branch> --state merged --json number,title,mergedAt
```

### Step 3: Classify Branches

| Condition | Classification | Action |
|-----------|---------------|--------|
| Merged into main + PR exists | `SAFE_DELETE` | Delete local + remote |
| Merged into main, no pr | `REVIEW_DELETE` | Ask user before delete |
| Not merged, no remote | `LOCAL_ONLY` | Keep (local work) |
| Not merged, has remote | `ACTIVE` | Keep (active development) |
| Stale (no commits ahead) | `STALE` | Suggest delete |

### Step 4: Execute Deletions (with confirmation)

For each `SAFE_DELETE` branch:

```powershell
# Delete local branch
git branch -D <branch>

# Delete remote branch
git push origin --delete <branch>
```

### Step 5: Report

```
BRANCH SYNC REPORT
==================

Fetched + pruned: ✅

SAFE_DELETE (1):
  ✅ feature/extract-tql — PR #235 merged, local + remote deleted

REVIEW_DELETE (0):
  (none)

LOCAL_ONLY (2):
  ℹ️ feature/old-experiment — local only, not merged
  ℹ️ dev/test-branch — local only, not merged

ACTIVE (3):
  ✅ feature/mc-rnn-layer — PR #236 open
  ✅ feature/perplexity-bridge — PR open
  ✅ main — default branch

STALE (0):
  (none)

RESULT: 1 branch deleted, 2 local-only kept, 3 active kept
```

---

## Examples

### Example 1: Full Sync

```powershell
/sync-branches
```

### Example 2: Dry Run

```powershell
/sync-branches --dry-run
# Shows what would be deleted without actually deleting
```

### Example 3: Force Delete All Merged

```powershell
/sync-branches --force
# Deletes all merged branches without confirmation
```

---

## Dependencies

- **Depends on**: `branch-lifecycle` (for branch classification)
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xSYNC_BRANCHES_SKILL_20260606` |
