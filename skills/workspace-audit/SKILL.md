---
type: skill
version: 1.0.0
intent_hash: 0xWORKSPACE_AUDIT_20260608
replaces: [workspace-sanitizer, untracked-auditor]
adr_ref: adr-preflight-pipeline-20260608
---

# workspace-audit (fusion workspace-sanitizer + untracked-auditor)

## Objectif
Remplace 2 appels `git status --short` par 1 seul.
Verifie working tree propre ET fichiers untracked en une passe.

## Protocole

```powershell
# 1 seul appel git
$status = git status --short 2>&1

# Separer modified/staged vs untracked
$modified  = $status | Where-Object { $_ -match "^[MAD ]" }
$untracked = $status | Where-Object { $_ -match "^\?\?" }

# Rapport
if ($modified)  { Write-Output "[WORKSPACE_AUDIT] DIRTY: $($modified.Count) modified" }
if ($untracked) { Write-Output "[WORKSPACE_AUDIT] UNTRACKED: $($untracked.Count) files" }
if (-not $status) { Write-Output "[WORKSPACE_AUDIT] CLEAN" }

# Gate
if ($modified -or $untracked) { exit 1 }   # bloquant
```

## Migration
- Remplacer tout appel a `workspace-sanitizer` par `workspace-audit`
- Remplacer tout appel a `untracked-auditor` par `workspace-audit`
- Mettre a jour `pre-flight-orchestrator` steps 3+4 -> step 3 unique

## Log unifie
```
[WORKSPACE_AUDIT] CLEAN
[WORKSPACE_AUDIT] DIRTY: 2 modified
[WORKSPACE_AUDIT] UNTRACKED: 3 files
```
