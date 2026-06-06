---
name: cross-repo-hooks
description: "Cross-repo hook analysis and orchestration: identify missing hooks, deploy hooks across repos, validate integration"
triggers:
  - /cross-repo-hooks
  - cross-repo hooks
  - analyze hooks
  - deploy hooks
  - hook orchestration
  - hook analysis
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - hooks
  - cross-repo
  - orchestration
  - analysis
phi_weight: 0.005
---

# Cross-Repo Hooks Skill

> **IntentHash**: `0xCROSS_REPO_HOOKS_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Combined skill for cross-repo hook analysis and orchestration. Two modes: `analyze` (identify missing hooks) and `orchestrate` (deploy hooks across repos).

---

## Triggers

- `/cross-repo-hooks analyze` — Analyze cross-repo hook integration
- `/cross-repo-hooks deploy` — Deploy hooks across repos
- `cross-repo hooks` — Interactive mode
- `analyze hooks` — Same as analyze mode
- `deploy hooks` — Same as deploy mode

---

## Workflow

### Analyze Mode

```powershell
# 1. Find all hook integration points
Get-ChildItem -Path . -Recurse -Filter "*.ps1" | Select-String -Pattern "Invoke-Hook|call.*hook" -List

# 2. Identify missing hooks
# Compare expected hooks (from registry) vs actual hooks (in scripts)

# 3. Report gaps
Write-Output "Missing hooks:"
Write-Output "  - pre-commit: not found in src/scripts/"
Write-Output "  - post-merge: not found in deploy/"
```

### Orchestrate Mode

```powershell
# 1. Define hook source
$hookSource = "C:\DevTools\SCRIPTS\hooks\"

# 2. Deploy to target repos
$targets = @(
    "D:\DO\WEB\BRAIN",
    "D:\DO\WEB\FLUENCE",
    "D:\DO\WEB\ECOYSTEM"
)

foreach ($repo in $targets) {
    Copy-Item "$hookSource\*" "$repo\.githooks\" -Force
    Write-Output "Deployed hooks to $repo"
}

# 3. Validate deployment
foreach ($repo in $targets) {
    $hooks = Get-ChildItem "$repo\.githooks" -File
    Write-Output "$repo : $($hooks.Count) hooks installed"
}
```

---

## Examples

### Example 1: Analyze

```powershell
/cross-repo-hooks analyze
# → Scans scripts, reports missing hooks
```

### Example 2: Deploy

```powershell
/cross-repo-hooks deploy
# → Deploys hooks to all target repos
```

---

## Dependencies

- **Depends on**: `git-hooks-manager`
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version (merged from cross-repo-hook-analyzer + multi-repo-hook-orchestration) | `0xCROSS_REPO_HOOKS_SKILL_20260606` |
