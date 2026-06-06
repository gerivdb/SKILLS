---
name: orphan-branch-dispatcher
description: "Analyzes orphan/closed-PR branches and dispatches: cherry-pick valuable commits, delete stale ones, escalate ambiguous cases"
triggers:
  - /orphan-dispatch
  - orphan branches
  - closed pr branches
  - dispatch orphans
  - review closed branches
  - triage orphan branches
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - orphan
  - branch
  - dispatch
  - cherry-pick
  - triage
phi_weight: 0.007
---

# Orphan Branch Dispatcher Skill

> **IntentHash**: `0xORPHAN_BRANCH_DISPATCHER_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Analyzes orphan branches (closed PR, no PR, stale) and dispatches each to the optimal action: **CHERRY-PICK** (valuable code), **DELETE** (stale/docs-only), or **ESCALATE** (ambiguous). Produces an execution plan with commit SHAs to cherry-pick.

---

## Triggers

- `/orphan-dispatch` — Analyze and dispatch all orphan branches
- `orphan branches` — Same as above
- `closed pr branches` — Analyze closed-PR branches specifically
- `dispatch orphans` — Same as above
- `triage orphan branches` — Same as above

---

## Decision Tree

For each orphan branch, evaluate:

```
1. Is it a docs-only branch (only .md files changed)?
   └── YES → DELETE (docs are likely outdated)

2. Is it >180 days old with no recent activity?
   └── YES → DELETE (stale)

3. Does it contain ECOS-AUTO commits?
   └── YES → CHERRY-PICK (automated code is usually valuable)

4. Does it have <5 commits and unique content not in main?
   └── YES → CHERRY-PICK (low risk, high value)

5. Does it have >50 commits with overlapping content?
   └── YES → ANALYZE (check for duplicates, cherry-pick unique only)

6. Is the PR title "vision" or "strategy" (not implementation)?
   └── YES → DELETE (strategic docs, not code)

7. Does it modify critical paths (src/brain/, src/core/)?
   └── YES → CHERRY-PICK (core code is valuable)

8. Ambiguous?
   └── ESCALATE to user with recommendation
```

---

## Workflow

### Step 1: Gather Orphan Branches

```powershell
# Closed PR branches
$closedPR = gh pr list --state closed --json number,headRefName,title,closedAt,labels

# Stale branches (no PR, old)
$stale = git branch -r --no-merged main | Where-Object {
    $lastCommit = git log -1 --format='%ai' $_
    ((Get-Date) - [DateTime]$lastCommit).Days -gt 90
}
```

### Step 2: Analyze Each Branch

For each branch, compute:
- **Commit count** ahead of main
- **File types changed** (code vs docs vs config)
- **Last commit age** in days
- **PR labels** (auto, strategy, etc.)
- **Commit message patterns** (feat/fix/chore/docs ratio)

### Step 3: Classify

| Classification | Criteria | Action |
|---------------|----------|--------|
| `CHERRY_PICK` | Code commits, <180d, ECOS-AUTO, core paths | Cherry-pick unique commits |
| `DELETE` | Docs-only, >180d, vision/strategy, already merged content | Delete remote branch |
| `ESCALATE` | Ambiguous, mixed content, >100 commits | Ask user |

### Step 4: Generate Execution Plan

```
ORPHAN DISPATCH REPORT
======================

CHERRY-PICK (10):
  ✅ feat/cli-phase1b-pattern-detector (85 commits) — ECOS-AUTO, CLI code
  ✅ feat/epistemic-routing-citizens (112 commits) — IntentValidator, ContextRouter
  ✅ feat/multi-tier-pipelines (112 commits) — MultiTier, DefensiveBreak
  ✅ feat/phi-cps-validator-rollback-auditor (112 commits) — PhiCPSValidator
  ✅ feature/brain-cli-extraction-task4 (86 commits) — BRAIN CLI
  ✅ feature/fractal-nervous-phase6-final-polish (1 commit) — final polish
  ✅ feature/fractal-phase3-sync-bidirectional (1 commit) — Notion sync
  ✅ feature/p2a-wal-core-batch-impl (2 commits) — WAL core
  ✅ feature/p2a-wal-manager-core-implementation (6 commits) — WAL manager
  ✅ feature/perplexity-bridge-brain (1 commit) — Perplexity bridge

DELETE (2):
  🗑️ feature/intelligence-processor-phase2b (29 commits, 218d old) — PR#1 vision, obsolete
  🗑️ ops/git-audit-consolidation-2026-03 (1 commit) — docs only, audit done

ESCALATE (0):
  (none)

Execute? [y/N]
```

### Step 5: Execute (with confirmation)

For CHERRY-PICK: delegate to `batch-cherry-pick-executor`
For DELETE: `git push origin --delete <branch>`

---

## Examples

### Example 1: Full Dispatch

```powershell
/orphan-dispatch
# → Analyzes all orphans, produces report, executes on confirmation
```

### Example 2: Dry Run

```powershell
/orphan-dispatch --dry-run
# → Shows plan without executing
```

---

## Dependencies

- **Depends on**: `branch-lifecycle`
- **Provides to**: `batch-cherry-pick-executor`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xORPHAN_BRANCH_DISPATCHER_SKILL_20260606` |
