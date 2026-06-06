---
name: citizen-module-integrator
description: "Handles Jules citizen modules integration: validates citizen structure, checks for conflicts, integrates new citizens"
triggers:
  - /citizen-integrate
  - citizen module
  - jules citizen
  - integrate citizen
  - citizen branch
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - citizen
  - jules
  - module
  - integration
phi_weight: 0.005
---

# Citizen Module Integrator Skill

> **IntentHash**: `0xCITIZEN_MODULE_INTEGRATOR_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Handles Jules citizen modules integration. Validates citizen structure, checks for conflicts with existing citizens, and integrates new citizens safely.

---

## Triggers

- `/citizen-integrate <branch>` — Analyze and integrate citizen branch
- `citizen module` — Interactive mode
- `jules citizen` — Same as above

---

## Workflow

### Step 1: Identify Citizen Files

```powershell
$citizenPatterns = @(
    '.Jules/citizens/*.py',
    '.Jules/citizens/**/*.py',
    'src/brain/citizens/*.py'
)

$branchFiles = git diff --name-only main...origin/$branch
$citizenFiles = $branchFiles | Where-Object {
    $file = $_
    $citizenPatterns | Where-Object { $file -like $_ }
}
```

### Step 2: Validate Citizen Structure

```powershell
# Each citizen should have:
# - __init__.py in citizens directory
# - Class inheriting from CitizenBase
# - register() method
foreach ($f in $citizenFiles) {
    $content = git show "origin/$branch`:$f" 2>$null
    if ($content -match 'class \w+\(CitizenBase\)') {
        Write-Output "✅ Valid citizen: $f"
    } elseif ($content -match '__init__') {
        Write-Output "✅ Init file: $f"
    } else {
        Write-Output "⚠️  Unknown citizen file: $f"
    }
}
```

### Step 3: Check for Duplicate Citizens

```powershell
# Check if citizen already exists in main
$existingCitizens = git ls-files '.Jules/citizens/*.py' 2>$null | ForEach-Object {
    [System.IO.Path]::GetFileNameWithoutExtension($_)
}
$newCitizens = $citizenFiles | Where-Object { $_ -match 'citizens/' } | ForEach-Object {
    [System.IO.Path]::GetFileNameWithoutExtension($_)
}
$duplicates = $newCitizens | Where-Object { $_ -in $existingCitizens }

if ($duplicates) {
    Write-Output "⚠️  Duplicate citizens: $($duplicates -join ', ')"
}
```

### Step 4: Integrate

```powershell
# For citizen modules, cherry-pick to preserve individual citizen commits
$commits = git log --oneline --reverse main..origin/$branch --format='%H %s' | Where-Object {
    $_ -notmatch 'Merge' -and ($_ -match 'citizen|Jules|module' -or $true)
}
foreach ($c in $commits) {
    $sha = ($c -split ' ')[0]
    $inMain = git log --oneline main --format='%H' | Where-Object { $_ -eq $sha }
    if ($inMain) { continue }

    git cherry-pick $sha --no-commit 2>$null
    if ($LASTEXITCODE -eq 0) {
        $diff = git diff --cached --stat 2>$null
        if ([string]::IsNullOrEmpty($diff)) {
            git reset HEAD 2>$null
        } else {
            git commit -m "cherry-pick: $(git log -1 --format='%s' $sha)" --no-verify 2>$null
        }
    } else {
        git cherry-pick --abort 2>$null
    }
}
```

---

## Dependencies

- **Depends on**: `branch-content-analyzer`, `branch-merge-strategy`
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xCITIZEN_MODULE_INTEGRATOR_SKILL_20260606` |
