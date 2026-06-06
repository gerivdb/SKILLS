---
name: git-assainissement
description: "Complete git repository sanitization: branch lifecycle, orphan dispatch, cherry-pick, cleanup, tags, submodules, reporting"
triggers:
  - /assainir
  - git cleanup
  - sanitize git
  - repository cleanup
  - full git audit
  - assainissement git
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - cleanup
  - sanitization
  - branches
  - maintenance
phi_weight: 0.010
---

# Git Assainissement Skill

> **IntentHash**: `0xGIT_ASSAINISSEMENT_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Orchestrates complete git repository sanitization. Runs all git management skills in sequence and produces a comprehensive report.

---

## Triggers

- `/assainir` — Full repository sanitization
- `git cleanup` — Same as above
- `sanitize git` — Same as above
- `repository cleanup` — Same as above
- `full git audit` — Audit only (no changes)

---

## Workflow

### Phase 1: Branch Lifecycle Analysis
**Skill**: `branch-lifecycle`
1. `git fetch --prune`
2. Classify all remote branches: SAFE_DELETE / REVIEW_DELETE / ACTIVE / STALE
3. Output report

### Phase 2: Stash Inspection
**Skill**: `stash-workflow`
1. `git stash list`
2. Inspect each stash contents
3. Drop stale stashes (pycache, auto-stash)
4. Keep stashes with meaningful changes

### Phase 3: Submodule Health Check
**Skill**: `submodule-manager`
1. `git submodule status --recursive`
2. Check for orphaned entries (`git ls-files --stage | grep 160000`)
3. Fix broken references

### Phase 4: Execute SAFE_DELETE
**Skill**: `sync-branches`
1. Delete all branches with merged PRs
2. `git push origin --delete <branch>`

### Phase 5: Orphan Dispatch
**Skill**: `orphan-branch-dispatcher`
1. Analyze REVIEW_DELETE branches
2. Classify: CHERRY_PICK / DELETE / ESCALATE
3. Generate execution plan

### Phase 6: Execute Cherry-Picks
**Skills**: `cherry-pick-batch`, `cherry-pick-conflict-resolver`, `batch-cherry-pick-executor`
1. Cherry-pick unique commits from orphan branches
2. Handle conflicts (skip duplicates, resolve with --theirs for binary)
3. For large divergent branches: use squash merge

### Phase 7: Tag Audit
**Skill**: `tag-release-manager`
1. List existing tags
2. Create tags for milestones if missing
3. Push tags

### Phase 8: Commit Message Audit
**Skill**: `conventional-commit-validator`
1. Check last N commits for conventional format
2. Report compliance percentage

### Phase 9: Final Report

```
GIT ASSAINISSEMENT REPORT
=========================

Branches:
  Before: 47 remote branches
  After:  11 remote branches
  Deleted: 36 (21 safe-delete, 8 cherry-picked, 7 stale)

Stashes:
  Before: 3
  After:  1
  Dropped: 2 (pycache, auto-stash)

Submodules:
  Fixed: echo-mcp orphaned entry removed

Tags:
  Before: 1 (v1.0.0-gitnote)
  After:  2 (v1.0.0-gitnote, v1.1.0-mc-rnn)

Commits cherry-picked: 10
Commits squash-merged: 0 (all content already in main)

Conventional commits: 56% compliance

Working tree: clean
```

---

## Dependencies

- **Depends on**: All git workflow skills
- **Provides to**: None (orchestrator)

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version — orchestrates all git management skills | `0xGIT_ASSAINISSEMENT_SKILL_20260606` |
