---
name: batch-cherry-pick-executor
description: "Executes cherry-pick of unique commits from multiple orphan branches with conflict detection, deduplication, and reporting"
triggers:
  - /batch-cherry-pick
  - cherry-pick orphans
  - cherry-pick multiple branches
  - execute cherry-pick plan
  - bulk cherry-pick
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
  - orphan
  - execution
phi_weight: 0.007
---

# Batch Cherry-Pick Executor Skill

> **IntentHash**: `0xBATCH_CHERRY_PICK_EXECUTOR_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Executes cherry-pick of unique commits from multiple orphan branches. Handles deduplication (same commit in multiple branches), conflict detection, and produces a detailed report.

---

## Triggers

- `/batch-cherry-pick` — Execute cherry-pick plan from orphan-dispatcher
- `cherry-pick orphans` — Same as above
- `cherry-pick multiple branches` — Interactive mode
- `bulk cherry-pick` — Same as above

---

## Workflow

### Step 1: Build Unique Commit List

```powershell
# Get unique commits from all target branches (not in main)
$allCommits = @{}
$branches = @("branch1", "branch2", "branch3")

foreach ($b in $branches) {
    $commits = git log --oneline --no-merges main..origin/$b --format='%H %s'
    foreach ($c in $commits) {
        $sha = ($c -split ' ')[0]
        $msg = ($c -split ' ', 2)[1]
        if (-not $allCommits.ContainsKey($sha)) {
            $allCommits[$sha] = @{ Message = $msg; Branch = $b }
        }
    }
}

# Sort by commit date (chronological)
$ordered = $allCommits.GetEnumerator() | Sort-Object { git log -1 --format='%at' $_.Key }
```

### Step 2: Cherry-Pick Each Commit

```powershell
$ok = 0
$conflict = 0
$skip = 0
$failed = @()

foreach ($entry in $ordered) {
    $sha = $entry.Key
    $msg = $entry.Value.Message

    # Try cherry-pick
    git cherry-pick $sha 2>&1 | Out-Null

    if ($LASTEXITCODE -eq 0) {
        $ok++
        Write-Output "✅ $sha — $msg"
    } else {
        # Check if it's a duplicate (already applied)
        $isDuplicate = git diff --cached --quiet 2>$null
        if ($isDuplicate) {
            $skip++
            Write-Output "⏭️  $sha — duplicate, skipping"
            git cherry-pick --skip 2>$null
        } else {
            $conflict++
            Write-Output "❌ $sha — CONFLICT: $msg"
            # Resolve or skip
            git cherry-pick --skip 2>$null
            $failed += $sha
        }
    }
}
```

### Step 3: Handle Conflicts

For each conflicted commit:

```powershell
# Option A: Skip (keep for later)
git cherry-pick --skip

# Option B: Resolve manually
# User edits files, then:
git add <resolved-files>
git cherry-pick --continue

# Option C: Use theirs/theirs for binary
git checkout --theirs <binary-file>
git add <binary-file>
git cherry-pick --continue
```

### Step 4: Generate Report

```
BATCH CHERRY-PICK REPORT
========================

Branches processed: 10
Total unique commits: 397

OK:        312 ✅
SKIPPED:    45 ⏭️  (duplicates)
CONFLICTS:  40 ❌

CONFLICTED COMMITS:
  abc1234 — feat(cli): Pattern Detector Phase 1B
  def5678 — feat(epistemic): IntentValidator Citizen
  ...

RECOMMENDATION: Review conflicted commits manually
```

---

## Deduplication Strategy

Many ECOS-AUTO branches share the same base commits. To avoid duplicates:

```powershell
# Before cherry-picking, check if commit is already in main
$alreadyInMain = git log --oneline main --format='%H' | Where-Object { $_ -eq $sha }
if ($alreadyInMain) {
    Write-Output "SKIP: $sha already in main"
    continue
}
```

---

## Examples

### Example 1: Execute Plan

```powershell
/batch-cherry-pick --plan orphan-dispatch-plan.json
# → Reads plan, cherry-picks all unique commits
```

### Example 2: Interactive

```powershell
/batch-cherry-pick
# → Prompts for branches, shows plan, confirms, executes
```

---

## Dependencies

- **Depends on**: `orphan-branch-dispatcher`, `cherry-pick-batch`, `cherry-pick-conflict-resolver`
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xBATCH_CHERRY_PICK_EXECUTOR_SKILL_20260606` |
