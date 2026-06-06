# PRD — 6 New Skills for Git Workflow Automation

> **IntentHash**: `0xPRD_GIT_WORKFLOW_SKILLS_20260606`  
> **Version**: 1.0.0  
> **Date**: 2026-06-06  
> **Status**: draft  
> **Author**: gerivdb  
> **PRD_ref**: adr-git-workflow-skills-20260606.md

---

## 1. Executive Summary

This PRD defines **6 new skills** to automate git workflow operations identified as gaps during the BRAIN repository PR #236 merge cycle. These skills cover branch lifecycle management, cherry-pick orchestration, KIVA-CLI integration, PR review, pycache cleanup, and branch synchronization.

### Problem Statement

During the BRAIN PR #236 workflow (2026-06-06), the following tasks were performed manually without dedicated skills:

1. **Branch analysis**: Analyzing 3 branches + 1 stash to determine PR merge / cherry-pick / delete strategy
2. **Cherry-pick orchestration**: Cherry-picking 8 commits individually with conflict management
3. **KIVA-CLI workflow**: Executing wal rollback → review → merge → wal append → drift check → citizen register
4. **PR review**: Using `gh pr view` as fallback (diffscope unavailable on Windows)
5. **Pycache cleanup**: Removing 96 `.pyc` files from git index + working tree
6. **Branch sync**: Deleting local/remote branches + verifying PR merge status

### Solution

Create 6 foundational skills that automate these workflows, integrated into the SKILLS registry.

---

## 2. Skill Specifications

### 2.1 `branch-lifecycle`

| Field | Value |
|-------|-------|
| **Name** | `branch-lifecycle` |
| **Type** | foundational |
| **Domain** | git-workflow |
| **Version** | 1.0.0 |
| **IntentHash** | `0xBRANCH_LIFECYCLE_SKILL_20260606` |

**Description**: Analyzes all branches in a git repository and recommends PR merge / cherry-pick / delete strategy for each.

**Triggers**:
- `/branch-lifecycle`
- `analyze branches`
- `branch strategy`
- `which branches to merge`
- `branch cleanup`

**Workflow**:
1. Run `git branch -a` + `git stash list`
2. For each branch, compute: commits ahead/behind main, files changed, ancestry
3. Classify each branch as: `PR_MERGE` | `CHERRY_PICK` | `DELETE` | `KEEP`
4. Output structured report with recommendations
5. Execute approved actions (with confirmation)

**Dependencies**: None (pure git)

---

### 2.2 `cherry-pick-batch`

| Field | Value |
|-------|-------|
| **Name** | `cherry-pick-batch` |
| **Type** | foundational |
| **Domain** | git-workflow |
| **Version** | 1.0.0 |
| **IntentHash** | `0xCHERRY_PICK_BATCH_SKILL_20260606` |

**Description**: Cherry-picks multiple commits with automatic conflict detection, skip/abort decisions, and reporting.

**Triggers**:
- `/cherry-pick-batch`
- `cherry-pick multiple commits`
- `batch cherry-pick`
- `cherry-pick from branch`

**Workflow**:
1. Accept list of commit SHAs or branch name
2. For each commit: `git cherry-pick <sha>`
3. On conflict: report conflicted files, mark as `CONFLICT`, continue to next
4. On success: mark as `OK`
5. Generate summary report: OK / CONFLICT / SKIP counts
6. Abort option on unresolvable conflicts

**Dependencies**: None (pure git)

---

### 2.3 `kiva-pr-workflow`

| Field | Value |
|-------|-------|
| **Name** | `kiva-pr-workflow` |
| **Type** | foundational |
| **Domain** | git-workflow |
| **Version** | 1.0.0 |
| **IntentHash** | `0xKIVA_PR_WORKFLOW_SKILL_20260606` |

**Description**: Executes the complete KIVA-CLI PR merge workflow: rollback point → review → merge → WAL update → drift check → citizen promotion.

**Triggers**:
- `/kiva-pr-workflow`
- `kiva merge pr`
- `merge with kiva`
- `pr workflow kiva`

**Workflow**:
1. `kiva wal rollback --reason "Pre-PR-<N>-merge snapshot"`
2. Review PR (via `gh pr view` or `diffscope pr`)
3. `gh pr merge <N> --squash --delete-branch`
4. `kiva wal append --operation PR_MERGE --repo <repo> --phi-delta 0.015 --status success`
5. `kiva wal drift` (verify < 5% threshold)
6. `kiva citizen register` or `kiva citizen promote` (if citizen exists)

**Dependencies**: KIVA-CLI (`kiva`), GitHub CLI (`gh`)

---

### 2.4 `diffscope-review`

| Field | Value |
|-------|-------|
| **Name** | `diffscope-review` |
| **Type** | foundational |
| **Domain** | git-workflow |
| **Version** | 1.0.0 |
| **IntentHash** | `0xDIFFSCOPE_REVIEW_SKILL_20260606` |

**Description**: Reviews a pull request using diffscope (or `gh` fallback on Windows) and posts review comments.

**Triggers**:
- `/diffscope-review`
- `review pr with diffscope`
- `diffscope pr`
- `automated pr review`

**Workflow**:
1. Detect platform: if Windows → use `gh pr view` as fallback
2. If diffscope available: `diffscope pr --number <N> --post-comments`
3. If fallback: `gh pr view <N>` + manual review summary
4. Output review report with findings

**Dependencies**: diffscope (Linux/macOS) or gh (Windows fallback)

---

### 2.5 `clean-pycache`

| Field | Value |
|-------|-------|
| **Name** | `clean-pycache` |
| **Type** | foundational |
| **Domain** | git-workflow |
| **Version** | 1.0.0 |
| **IntentHash** | `0xCLEAN_PYCACHE_SKILL_20260606` |

**Description**: Removes `__pycache__` directories and `.pyc` files from both working tree and git index, ensures `.gitignore` coverage.

**Triggers**:
- `/clean-pycache`
- `clean pycache`
- `remove pyc files`
- `pycache cleanup`

**Workflow**:
1. Find all `__pycache__/` directories and `.pyc` files
2. `git rm --cached -r <pycache_paths>` (remove from index)
3. `Remove-Item -Recurse -Force <pycache_paths>` (remove from working tree)
4. Verify `.gitignore` contains `__pycache__/` and `*.py[cod]`
5. If not, append to `.gitignore`
6. Report: files removed, index cleaned, .gitignore updated

**Dependencies**: None (pure git + filesystem)

---

### 2.6 `sync-branches`

| Field | Value |
|-------|-------|
| **Name** | `sync-branches` |
| **Type** | foundational |
| **Domain** | git-workflow |
| **Version** | 1.0.0 |
| **IntentHash** | `0xSYNC_BRANCHES_SKILL_20260606` |

**Description**: Synchronizes local and remote branches, detects already-merged branches, and cleans up stale references.

**Triggers**:
- `/sync-branches`
- `sync branches local remote`
- `cleanup merged branches`
- `delete merged branches`
- `branch sync`

**Workflow**:
1. `git fetch --prune`
2. For each local branch: check if remote tracking branch exists
3. For each branch: check if fully merged into main (`git branch --merged main`)
4. For merged branches: verify PR status via `gh pr list --state merged`
5. Delete local + remote branches that are fully merged
6. Report: deleted / kept / stale counts

**Dependencies**: GitHub CLI (`gh`)

---

## 3. Taxonomy Placement

All 6 skills are **foundational** type (cross-cutting, reusable across ≥3 domains).

**Proposed directory structure**:
```
native/foundational/
├── branch-lifecycle/
│   └── SKILL.md
├── cherry-pick-batch/
│   └── SKILL.md
├── kiva-pr-workflow/
│   └── SKILL.md
├── diffscope-review/
│   └── SKILL.md
├── clean-pycache/
│   └── SKILL.md
└── sync-branches/
    └── SKILL.md
```

---

## 4. Dependencies Matrix

| Skill | Depends On | Provides To |
|-------|-----------|-------------|
| `branch-lifecycle` | — | `cherry-pick-batch`, `kiva-pr-workflow`, `sync-branches` |
| `cherry-pick-batch` | `branch-lifecycle` | `kiva-pr-workflow` |
| `kiva-pr-workflow` | `branch-lifecycle`, `cherry-pick-batch`, `diffscope-review` | — |
| `diffscope-review` | — | `kiva-pr-workflow` |
| `clean-pycache` | — | — |
| `sync-branches` | `branch-lifecycle` | — |

---

## 5. Acceptance Criteria

- [ ] All 6 SKILL.md files created with valid frontmatter
- [ ] All skills registered in REGISTRY.yaml
- [ ] CI validation passes (`tools/validate-skills.sh`)
- [ ] Each skill has ≥3 triggers
- [ ] Each skill has working examples
- [ ] No naming conflicts with existing skills
- [ ] PR submitted with completed template

---

## 6. Out of Scope

- Integration with CI/CD pipelines (future PRD)
- GUI/TUI for branch visualization
- Automated conflict resolution (manual only)
- Support for non-GitHub remotes (GitHub only)

---

## 7. Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial PRD — 6 new git workflow skills | `0xPRD_GIT_WORKFLOW_SKILLS_20260606` |

---

*Part of ecosystem-1 SKILLS registry · gerivdb*
