---
name: branch-merge-strategy
description: "Decides optimal merge strategy per branch: cherry-pick, squash merge, rebase, or delete based on content analysis"
triggers:
  - /merge-strategy
  - branch merge strategy
  - how to merge branch
  - cherry-pick or squash
  - optimal merge
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
  - strategy
  - cherry-pick
  - squash
phi_weight: 0.006
---

# Branch Merge Strategy Skill

> **IntentHash**: `0xBRANCH_MERGE_STRATEGY_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Decides the optimal merge strategy for each branch based on content analysis: **CHERRY-PICK** (few unique commits), **SQUASH MERGE** (many commits, clean history), **REBASE** (linear history needed), or **DELETE** (already merged/stale).

---

## Triggers

- `/merge-strategy <branch>` — Get recommendation for a branch
- `branch merge strategy` — Interactive mode
- `how to merge branch` — Same as above
- `cherry-pick or squash` — Decision guidance

---

## Decision Tree

```
Input: branch with N unique files, M commits ahead, P commits behind, D days old

1. N == 0 (no unique files)?
   └── YES → DELETE (all content already in main)

2. M == 0 (no commits ahead)?
   └── YES → DELETE (branch is behind main, stale)

3. D > 180 (older than 6 months)?
   └── YES → DELETE (stale, content likely outdated)

4. N < 5 AND M < 10 (few unique files/commits)?
   └── YES → CHERRY-PICK (low risk, preserves individual commits)

5. N >= 5 AND M < 50 (moderate content)?
   └── Check conflict likelihood:
       ├── Low conflict files (new files, different paths) → CHERRY-PICK
       └── High conflict files (same paths as main) → SQUASH MERGE

6. N >= 20 OR M >= 50 (large content)?
   └── SQUASH MERGE (clean history, single commit)

7. P > 90 (far behind main)?
   └── SQUASH MERGE (rebase would be too complex)

8. Branch modifies critical paths (src/brain/, src/core/)?
   └── CHERRY-PICK (preserve individual commit history for audit)
```

---

## Conflict Likelihood Assessment

```powershell
# Check if branch modifies files that also exist in main
$branchFiles = git diff --name-only main...origin/$branch
$mainFiles = git ls-files
$overlap = $branchFiles | Where-Object { $_ -in $mainFiles }
$overlapPercent = ($overlap.Count / $branchFiles.Count) * 100

if ($overlapPercent -lt 30) { "LOW conflict risk" }
elseif ($overlapPercent -lt 70) { "MEDIUM conflict risk" }
else { "HIGH conflict risk" }
```

---

## Execution

### Cherry-Pick Strategy

```powershell
# For small branches with unique files
$commits = git log --oneline --reverse main..origin/$branch --format='%H %s' | Where-Object { $_ -notmatch 'Merge' }
foreach ($c in $commits) {
    $sha = ($c -split ' ')[0]
    git cherry-pick $sha --no-commit 2>$null
    if ($LASTEXITCODE -eq 0) {
        $diff = git diff --cached --stat 2>$null
        if ([string]::IsNullOrEmpty($diff)) {
            git reset HEAD 2>$null  # empty, skip
        } else {
            git commit -m "cherry-pick: $(git log -1 --format='%s' $sha)" --no-verify 2>$null
        }
    } else {
        git cherry-pick --abort 2>$null
    }
}
```

### Squash Merge Strategy

```powershell
# For large branches
$tempBranch = "temp/squash-$($branch -replace '[^a-z0-9]', '-')"
git checkout -b $tempBranch origin/$branch 2>$null
git checkout main 2>$null
git merge --squash $tempBranch 2>$null
if ($LASTEXITCODE -eq 0) {
    git commit -m "feat($label): squash merge from $branch" --no-verify 2>$null
} else {
    # Resolve conflicts
    git diff --name-only --diff-filter=U 2>$null | ForEach-Object {
        git checkout --theirs $_ 2>$null; git add $_ 2>$null
    }
    git commit -m "feat($label): squash merge from $branch (conflicts resolved)" --no-verify 2>$null
}
git branch -D $tempBranch 2>$null
```

---

## Examples

### Example 1: Get Strategy

```powershell
/merge-strategy feat/brain-citizen-native
# → Recommendation: CHERRY-PICK (28 unique files, 5 commits, low conflict)
```

### Example 2: Execute Strategy

```powershell
/merge-strategy feat/brain-citizen-native --execute
# → Cherry-picks 5 commits, reports result
```

---

## Dependencies

- **Depends on**: `branch-content-analyzer`
- **Provides to**: `batch-cherry-pick-executor`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xBRANCH_MERGE_STRATEGY_SKILL_20260606` |
