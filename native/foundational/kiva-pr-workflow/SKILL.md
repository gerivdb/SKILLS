---
name: kiva-pr-workflow
description: "Executes the complete KIVA-CLI PR merge workflow: rollback point, review, merge, WAL update, drift check, citizen promotion"
triggers:
  - /kiva-pr-workflow
  - kiva merge pr
  - merge with kiva
  - pr workflow kiva
  - kiva pr merge
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - kiva
  - pr
  - merge
  - wal
  - citizen
  - workflow
phi_weight: 0.008
---

# KIVA PR Workflow Skill

> **IntentHash**: `0xKIVA_PR_WORKFLOW_SKILL_20260606`  
> **Version**: 1.0.0  
> **Domain**: foundational  
> **Type**: foundational  
> **Status**: active

---

## Synopsis

Executes the complete KIVA-CLI PR merge workflow: rollback point creation → PR review → squash merge → WAL event append → drift check → citizen registration/promotion.

---

## Triggers

- `/kiva-pr-workflow <PR_NUMBER>` — Full workflow for a specific PR
- `kiva merge pr` — Same as above
- `merge with kiva` — Interactive mode (asks for PR number)
- `pr workflow kiva` — Same as above

---

## Prerequisites

- KIVA-CLI installed (`pip install -e <KIVA-CLI_PATH>`)
- GitHub CLI (`gh`) authenticated
- `$env:PYTHONIOENCODING="utf-8"` set (Windows)

---

## Workflow

### Step 1: Create Rollback Point

```powershell
$env:PYTHONIOENCODING="utf-8"
kiva wal rollback --reason "Pre-PR-<N>-merge snapshot"
```

Expected output:
```
Rollback point created!
  Rollback ID: <uuid>
  phi-CPS snapshot: <value>
  Reason: Pre-PR-<N>-merge snapshot
```

### Step 2: Review PR

```powershell
# Get PR details
gh pr view <N> --json title,state,commits,files,additions,deletions

# Optional: diffscope review (if available)
# diffscope pr --number <N>
```

Verify:
- PR state is `OPEN`
- All CI checks passed
- No conflicts with base branch

### Step 3: Merge PR

```powershell
gh pr merge <N> --squash --delete-branch
```

Options:
- `--squash` — Squash merge (recommended for feature branches)
- `--merge` — Merge commit (for release branches)
- `--delete-branch` — Delete branch after merge

### Step 4: Append WAL Event

```powershell
kiva wal append `
  --operation PR_MERGE `
  --repo <REPO_NAME> `
  --phi-delta 0.015 `
  --parent-hash <INTENT_HASH> `
  --commit-sha <MERGE_COMMIT_SHA> `
  --status success
```

### Step 5: Check Drift

```powershell
kiva wal drift
```

Verify drift is within 5% threshold:
```
φ-CPS current: 1.0150
Relative drift: 1.50%
Status: ✅ WITHIN LIMITS
```

If drift > 5%: investigate before proceeding.

### Step 6: Register/Promote Citizen

```powershell
# Check if citizen exists
kiva citizen list --repo <REPO_NAME>

# If not exists: register
kiva citizen register --name <REPO_NAME> --type TOOL --repo <REPO_NAME> --level L2_OPERATIONAL

# If exists: promote
kiva citizen promote <CITIZEN_ID> --level L3_PRODUCTION
```

---

## Examples

### Example 1: Full Workflow

```powershell
/kiva-pr-workflow 236
```

Output:
```
KIVA PR WORKFLOW — PR #236
==========================

[1/6] Creating rollback point... ✅ Rollback ID: c87925aadcaeed0d
[2/6] Reviewing PR... ✅ 3 commits, 1047 additions, 0 deletions
[3/6] Merging PR... ✅ Squash merged, branch deleted
[4/6] Appending WAL event... ✅ Event ID: 02705e840e6cf256
[5/6] Checking drift... ✅ 1.50% (within 5% threshold)
[6/6] Registering citizen... ✅ ctz_d9339a9b2fb6ee6c (L2_OPERATIONAL)

WORKFLOW COMPLETE ✅
```

### Example 2: Interactive Mode

```powershell
/kiva-pr-workflow
# Prompts for PR number, repo name, merge strategy
```

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Rollback point creation fails | Abort workflow, check KIVA-CLI |
| PR has conflicts | Abort, ask user to resolve |
| Merge fails | Abort, check gh auth |
| WAL append fails | Report error, WAL may be out of sync |
| Drift > 5% | Warn user, ask to continue or abort |
| Citizen not found | Register new citizen |

---

## Dependencies

- **Depends on**: `branch-lifecycle`, `cherry-pick-batch`, `diffscope-review`
- **Provides to**: None (terminal skill)

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xKIVA_PR_WORKFLOW_SKILL_20260606` |
