---
name: git-lock-rescuer
description: Diagnostic et resolution securisee des fichiers .lock git (.git/index.lock, etc.). Jamais de suppression aveugle. Utilise ce skill quand un git add/commit/push est bloque par un lock, avant toute suppression de .lock.
version: 1.0.0
intent_hash: 0xGIT_LOCK_RESCUER_20260810
---

# Git Lock Rescuer

## Objectif
Debloquer les operations git sans perte ni corruption, en diagnosticant la cause du `.lock` avant toute action.

## Declencheur
- `git add/commit/push` echoue avec `index.lock`
- `fatal: Unable to create '.git/index.lock': File exists.`
- Tout processus git bloque par un fichier `.lock`

## Protocole obligatoire

### Etape 1 - NE PAS supprimer immediatement
```powershell
# [KO] INTERDIT - suppression aveugle
Remove-Item ".git\index.lock" -Force
```

### Etape 2 - Diagnostiquer le processus
```powershell
# Verifier les processus git actifs
Get-Process -Name "git" -ErrorAction SilentlyContinue | Select Id, ProcessName, StartTime, CPU

# Verifier les fichiers .lock
Get-ChildItem -LiteralPath ".git" -Filter "*.lock" -Recurse -ErrorAction SilentlyContinue | Select FullName, Length, LastWriteTime
```

### Etape 3 - Analyser la situation
| Cas | Action |
|-----|--------|
| Processus git vivant < 5 min | Attendre, ne pas toucher |
| Processus git mort > 5 min | Supprimer le .lock |
| Aucun processus git | Supprimer le .lock |
| `.lock` sur `.git/index.lock` avec WIP non commite | `git reset --hard` AVANT suppression |

### Etape 4 - Supprimer UNIQUEMENT si sur
```powershell
# Apres diagnostic confirme
Remove-Item ".git\index.lock" -Force
```

### Etape 5 - Verifier
```powershell
git status
```

## Anti-patterns bloquants
- Supprimer `.lock` sans diagnostic processus
- Tuer un processus git sans verifier s'il est en cours de commit
- Ignorer un `.lock` sur `.git/index.lock` quand il y a du WIP
- Forcer `git reset --hard` sans sauvegarde prealable

## Reference ADR
- **ADR** : ADR-2026-08-10-003-GIT_LOCK_RESCUER
- **IntentHash** : 0xGIT_LOCK_RESCUER_20260810
- **Depot** : gerivdb/GeriCode
- **Statut ADR** : proposed
