---
type: skill
version: 1.0.0
intent_hash: 0xDOC_GATE_20260608
replaces: [doc-status-validator, git-hook-enforcer]
adr_ref: adr-2026-06-07-001-governance-gate
---

# doc-gate (fusion doc-status-validator + git-hook-enforcer)

## Objectif
Extraire les regles des hooks pre-commit ET valider les statuts
PRD/EPIC/INTENT en une seule passe chainee.

## Protocole

### Phase 1 - Extraction regles (ex git-hook-enforcer)
```powershell
$hookPath = ".githooks/pre-commit"
if (Test-Path $hookPath) {
    $rules = Get-Content $hookPath | Where-Object { $_ -match "status|frontmatter|ADR" }
    Write-Output "[DOC_GATE] Hook rules: $($rules.Count) regles detectees"
} else {
    Write-Output "[DOC_GATE] WARN: pas de hook pre-commit"
}
```

### Phase 2 - Validation statuts (ex doc-status-validator)
```powershell
# Verifier que les statuts dans PRD/EPIC sont dans la liste valide
$validStatuses = @("draft","proposed","accepted","deprecated","superseded",
                   "planned","active","completed")
$docs = Get-ChildItem -Recurse -Include "*.md" | 
        Select-String "^status:" | 
        Where-Object { $_.Line -notmatch ($validStatuses -join "|") }

if ($docs) {
    Write-Output "[DOC_GATE] INVALID STATUS: $($docs.Count) docs"
    $docs | ForEach-Object { Write-Output "  -> $($_.Filename): $($_.Line)" }
    exit 1
}
Write-Output "[DOC_GATE] All statuses valid"
```

## Log unifie
```
[DOC_GATE] Hook rules: 3 regles detectees
[DOC_GATE] All statuses valid
[DOC_GATE] INVALID STATUS: 1 docs -> PRD_MC_RNN: status: wip
```
