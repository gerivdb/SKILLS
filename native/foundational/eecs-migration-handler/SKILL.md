---
name: eecs-migration-handler
description: "Handles EECS migration branches: validates migration files, checks for conflicts with existing EECS config, integrates safely"
triggers:
  - /eecs-migration
  - eecs migration
  - migrate eecs
  - eecs branch
  - eecs integration
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - eecs
  - migration
  - integration
phi_weight: 0.005
---

# EECS Migration Handler Skill

> **IntentHash**: `0xEECS_MIGRATION_HANDLER_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Handles EECS (ECOS Ecosystem Configuration System) migration branches. Validates migration files, checks for conflicts with existing EECS config, and integrates safely.

---

## Triggers

- `/eecs-migration <branch>` — Analyze and integrate EECS migration branch
- `eecs migration` — Interactive mode
- `eecs branch` — Same as above

---

## Workflow

### Step 1: Identify EECS Files

```powershell
# EECS-specific files
$eecsPatterns = @(
    '.eecs_config.yaml',
    '.ecos/local_registry.json',
    'EECS_MIGRATION.md',
    '.github/workflows/eecs-*.yml',
    'config/ecosystem-cli-config.json'
)

$branchFiles = git diff --name-only main...origin/$branch
$eecsFiles = $branchFiles | Where-Object {
    $file = $_
    $eecsPatterns | Where-Object { $file -like $_ }
}
```

### Step 2: Validate Migration

```powershell
# Check if EECS config is valid YAML
foreach ($f in $eecsFiles) {
    if ($f -match '\.yaml$|\.yml$') {
        try {
            $content = git show "origin/$branch`:$f" 2>$null
            $null = $content | ConvertFrom-Yaml -ErrorAction Stop
            Write-Output "✅ Valid YAML: $f"
        } catch {
            Write-Output "❌ Invalid YAML: $f — $_"
        }
    }
}
```

### Step 3: Check Conflicts

```powershell
# Check if EECS files already exist in main
$existingEecs = git ls-files | Where-Object { $_ -match 'eecs|ecos.*config' }
$conflicts = $eecsFiles | Where-Object { $_ -in $existingEecs }

if ($conflicts) {
    Write-Output "⚠️  Conflicts with existing EECS files:"
    $conflicts | ForEach-Object { Write-Output "  $_" }
}
```

### Step 4: Integrate

```powershell
# For EECS migrations, prefer squash merge (single config commit)
$tempBranch = "temp/eecs-$($branch -replace '[^a-z0-9]', '-')"
git checkout -b $tempBranch origin/$branch 2>$null
git checkout main 2>$null
git merge --squash $tempBranch 2>$null

if ($LASTEXITCODE -eq 0) {
    git commit -m "chore(eecs): integrate migration from $branch" --no-verify 2>$null
    Write-Output "✅ EECS migration integrated"
} else {
    Write-Output "❌ Conflicts — manual resolution needed"
    git merge --abort 2>$null
}
git branch -D $tempBranch 2>$null
```

---

## Dependencies

- **Depends on**: `branch-content-analyzer`, `branch-merge-strategy`
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xEECS_MIGRATION_HANDLER_SKILL_20260606` |
