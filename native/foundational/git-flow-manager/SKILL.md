---
name: git-flow-manager
description: "Implements git-flow branching model: feature, release, hotfix, develop, main — guides branch creation, merging, and deletion per git-flow conventions"
triggers:
  - /git-flow
  - git flow
  - gitflow
  - branch naming convention
  - create feature branch
  - create release branch
  - create hotfix branch
  - finish feature
  - finish release
  - finish hotfix
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - gitflow
  - branching
  - workflow
  - convention
phi_weight: 0.008
---

# Git Flow Manager Skill

> **IntentHash**: `0xGIT_FLOW_MANAGER_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Implements the **git-flow** branching model (Vincent Driessen) for the ECOS ecosystem. Enforces branch naming conventions, guides branch lifecycle (create → work → finish), and ensures consistent merge strategies.

---

## Triggers

- `/git-flow feature <name>` — Create and manage feature branches
- `/git-flow release <version>` — Create and manage release branches
- `/git-flow hotfix <version>` — Create and manage hotfix branches
- `/git-flow finish <branch>` — Finish a feature/release/hotfix
- `git flow` — Interactive mode
- `branch naming convention` — Validate/enforce naming
- `create feature branch` — Create feature branch
- `create release branch` — Create release branch
- `create hotfix branch` — Create hotfix branch

---

## Branch Naming Conventions

| Type | Pattern | Base Branch | Merge Target |
|------|---------|-------------|--------------|
| `feature/` | `feature/<description>` | `develop` | `develop` |
| `release/` | `release/v<semver>` | `develop` | `main` + `develop` |
| `hotfix/` | `hotfix/v<semver>` | `main` | `main` + `develop` |
| `chore/` | `chore/<description>` | `develop` | `develop` |
| `fix/` | `fix/<description>` | `develop` | `develop` |

**Rules**:
- Lowercase only
- Kebab-case for descriptions
- No special characters except `/` and `-`
- Max 50 characters for description

---

## Workflow

### Feature Branch Lifecycle

```powershell
# 1. Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# 2. Work on feature (commit regularly)
git add .
git commit -m "feat(scope): description"

# 3. Keep feature branch up to date
git fetch origin
git rebase origin/develop

# 4. Finish feature (merge to develop)
git checkout develop
git merge --no-ff feature/my-feature
git branch -d feature/my-feature
git push origin develop
```

### Release Branch Lifecycle

```powershell
# 1. Create release branch
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# 2. Bump version, fix bugs only (no features)
git commit -m "chore: bump version to 1.2.0"

# 3. Finish release
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"
git checkout develop
git merge --no-ff release/v1.2.0
git branch -d release/v1.2.0
git push origin main develop --tags
```

### Hotfix Branch Lifecycle

```powershell
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/v1.2.1

# 2. Fix the bug
git commit -m "fix: critical production bug"

# 3. Finish hotfix
git checkout main
git merge --no-ff hotfix/v1.2.1
git tag -a v1.2.1 -m "Hotfix v1.2.1"
git checkout develop
git merge --no-ff hotfix/v1.2.1
git branch -d hotfix/v1.2.1
git push origin main develop --tags
```

---

## Branch Naming Validation

Before creating any branch, validate the name:

```powershell
function Test-BranchName {
    param([string]$name)
    $patterns = @(
        '^feature/[a-z0-9-]+$',
        '^release/v\d+\.\d+\.\d+$',
        '^hotfix/v\d+\.\d+\.\d+$',
        '^chore/[a-z0-9-]+$',
        '^fix/[a-z0-9-]+$'
    )
    foreach ($p in $patterns) {
        if ($name -match $p) { return $true }
    }
    return $false
}
```

If validation fails, reject the branch name and suggest a corrected version.

---

## ECOS Adaptation

For ECOS repositories that use `main` instead of `develop`:

| Git Flow | ECOS Equivalent |
|----------|----------------|
| `develop` | `main` |
| `main` | `main` (same) |
| Feature merges to | `main` |
| Release merges to | `main` + tag |

---

## Examples

### Example 1: Create Feature

```powershell
/git-flow feature mc-rnn-layer
# → git checkout main && git pull && git checkout -b feature/mc-rnn-layer
```

### Example 2: Finish Feature

```powershell
/git-flow finish feature/mc-rnn-layer
# → git checkout main && git merge --no-ff feature/mc-rnn-layer && git branch -d feature/mc-rnn-layer
```

### Example 3: Create Release

```powershell
/git-flow release v2.0.0
# → git checkout main && git pull && git checkout -b release/v2.0.0
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `branch-lifecycle`, `tag-release-manager`, `sync-branches`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xGIT_FLOW_MANAGER_SKILL_20260606` |
