---
type: skill
version: "1.0.0"
date: "2026-06-08"
intent_hash: 0xREPO_COVERAGE_BATCH_20260608
status: active
trit_primitive: TritObserve
tags: [argus, coverage, batch, repo, stratum]
---

# repo-coverage-batch

## Purpose
Run the generic `repo_coverage_health` scanner on multiple repos in batch — verify STRATUM_RELAY.md, ECOS_ROOT.json, README.md presence across the ecosystem.

## Trigger
Use when: running coverage checks across multiple repos, user mentions "repo coverage", "batch scanner", "STRATUM_RELAY batch", or "ecosystem coverage".

## Steps

### Step 1 — Build repo list from strata

Use the 3-level search protocol (INDEX → STRATA → RECURSIVE):

```powershell
$repos = @()
foreach ($s in @("L0-CANON","L1-INFRA","L2-PLATFORM","L3-CITIZENS","L4-TOOLS","L5-ARCHIVE")) {
    $dirs = Get-ChildItem "D:\DO\WEB\TOOLS\$s" -Directory -ErrorAction SilentlyContinue
    foreach ($d in $dirs) {
        $repos += @{name=$d.Name; root=$d.FullName}
    }
}
```

### Step 2 — Run scanner per repo

```powershell
$scanner = "D:\DO\WEB\TOOLS\L3-CITIZENS\ARGUS\scanners\declared\repo_coverage_health.yaml"
$gov = "D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB"

foreach ($r in $repos) {
    $out = python -m engine.declarative_runner $scanner `
        "repo_name=$($r.name)" "repo_root=$($r.root)" "gov_root=$gov" 2>&1
    if ($LASTEXITCODE -eq 0) { Write-Host "OK  $($r.name)" }
    else { Write-Host "FAIL $($r.name)" }
}
```

### Step 3 — Fix failing repos

For each FAIL, create missing files:
- `STRATUM_RELAY.md` — from `known_repositories.yaml` metadata (layer, role)
- `ECOS_ROOT.json` — from `known_repositories.yaml` metadata
- `README.md` — minimal with layer and role

### Step 4 — Re-run until all PASS

Target: score 1.0 for all repos.

## Files created per repo

```
{repo_root}/
  STRATUM_RELAY.md   ← layer, role, status, section
  ECOS_ROOT.json     ← {name, layer, status, citizen, strate, role}
  README.md          ← # {name}, **Layer:** {layer}, **Role:** {role}
```

## Rules
- Always search strata L0-L5 first — never hardcode repo paths
- Always check `known_repositories.yaml` for metadata before creating files
- Re-run after fixing — validation is mandatory

## Anti-patterns
- Don't hardcode repo paths
- Don't create files without checking `known_repositories.yaml`
- Don't skip the re-run after fixing
