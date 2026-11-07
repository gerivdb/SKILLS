---
type: SKILL
version: "1.0.0"
intent_hash: 0xBRANCH_AUDITOR_20260808
---

# Branch Auditor

## Objectif

Auditer les branches : orphelines, drift, métriques.

## Déclencheur

À la fin de chaque session KiloCode, et en audit mensuel NEXUS/ARGUS.

## Règles

### 1. Scanner les branches orphelines

```powershell
# Lister les branches sans PR ouverte
$branches = git branch -r
foreach ($branch in $branches) {
    $pr = gh pr list --head $branch --state open
    if (-not $pr) {
        Write-Output "[ORPHAN] $branch"
    }
}
```

### 2. Détecter le drift

```powershell
# Calculer le diff avec main
git diff main...feat/rlm243-laplace-optimization --stat
```

→ Si diff > 1000 lignes → **ALERTE** ARGUS

### 3. Détecter les branches âgées

```powershell
# Vérifier la date du dernier commit
git log -1 --format=%ci feat/rlm243-laplace-optimization
```

→ Si > 30 jours → **ALERTE** ARGUS

### 4. Générer les métriques

```powershell
# Nombre de branches actives
git branch -r | Measure-Object | Select-Object -ExpandProperty Count

# Taux de merge
$merged = git branch -r --merged main | Measure-Object | Select-Object -ExpandProperty Count
$total = git branch -r | Measure-Object | Select-Object -ExpandProperty Count
$mergeRate = $merged / $total
```

### 5. Journaliser dans WAL

```
[BRANCH_AUDIT] date=<iso>, active=<n>, merged=<k>, orphaned=<m>, drift=<d>, alert=<boolean>
```

## Référence ADR

- **ADR** : ADR-2026-08-08-AGENTIC-GIT-WORKFLOW
- **IntentHash** : 0xAGENTIC_GIT_WORKFLOW_20260808
- **Statut ADR** : proposed
