---
name: branch-hygiene-auditor
description: Detecte et nettoie les branches orphelines dans un repo git. Utilise ce skill quand tu dois auditer les branches, supprimer les branches mergees, ou pruner les refs remote obsoletes.
version: 1.0.0
intent_hash: 0xBRANCH_HYGIENE_AUDITOR_20260809
---

# Branch Hygiene Auditor

## Objectif
Maintenir la proprete du graphe git en detectant et supprimant les branches orphelines, mergees ou non suivies.

## Declencheur
- Fin de session KiloCode
- Audit quotidien
- Avant toute creation de branche feature
- Apres chaque merge dans main

## Prerequis
- Repo git valide
- Acces en ecriture au repo
- Remote `origin` configure

## Protocole

### Etape 1 - Pruner les refs remote obsoletes
```powershell
git remote prune origin
```

### Etape 2 - Lister les branches remote non mergees
```powershell
$defaultBranch = git symbolic-ref refs/remotes/origin/HEAD | ForEach-Object { $_.Split('/') | Select-Object -Last 1 }
git branch -r --no-merged origin/$defaultBranch
```
-> Si liste vide -> OK, passer a l'etape 4
-> Si liste non vide -> examiner chaque branche

### Etape 3 - Decider pour chaque branche orpheline

| Cas | Action |
|-----|--------|
| Branche mergee dans main (PR fermee) | `git branch -d <branch>` |
| Branche non mergee, commits uniques | Sauvegarder les commits, puis `git branch -D <branch>` |
| Branche remote supprimee mais ref locale reste | `git remote prune origin` |
| Branche inconnue | STOP - demander confirmation HITL |

### Etape 4 - Lister les branches locales
```powershell
git branch -vv
```

### Etape 5 - Supprimer les branches locales mergees
```powershell
$defaultBranch = git symbolic-ref refs/remotes/origin/HEAD | ForEach-Object { $_.Split('/') | Select-Object -Last 1 }
git branch --merged $defaultBranch | Where-Object { $_ -notmatch "^\* $defaultBranch`$" } | ForEach-Object { git branch -d $_.Trim() }
```

### Etape 6 - Verification finale
```powershell
$defaultBranch = git symbolic-ref refs/remotes/origin/HEAD | ForEach-Object { $_.Split('/') | Select-Object -Last 1 }
git branch -r --no-merged origin/$defaultBranch
git branch -vv
```

## Sortie standard

```yaml
branches_orphaned: []
branches_merged_removed: []
branches_force_removed: []
remote_pruned: []
recommendations: []
```

## Anti-patterns bloquants
- Supprimer une branche non mergee sans sauvegarde
- Supprimer `main` ou `master`
- Supprimer une branche dont le remote est encore actif
- Utiliser `--force` sans verification prealable

## Reference ADR
- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **IntentHash** : 0xBRANCH_HYGIENE_AUDITOR_20260809
- **Depot** : gerivdb/GeriCode
- **Statut ADR** : proposed

## References
- **IntentHash parent** : `0xPRD_MOC_GIT_HYGIENE_MECHANISMS_20260809`
- **IntentHash review fixes** : `0xPRD_MOC_GIT_HYGIENE_REVIEW_FIXES_20260809`
- **IntentHash incoherences** : `0xPRD_MOC_GIT_HYGIENE_INCOHERENCE_FIXES_20260809`
