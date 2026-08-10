---
name: git-lock-rescuer
description: Diagnostic et résolution sécurisée des fichiers .lock git (.git/index.lock, etc.). Jamais de suppression aveugle. Utilise ce skill quand un git add/commit/push est bloqué par un lock, avant toute suppression de .lock.
version: 1.0.0
intent_hash: 0xGIT_LOCK_RESCUER_20260810
---

# Git Lock Rescuer

## Objectif
Débloquer les opérations git sans perte ni corruption, en diagnosticant la cause du `.lock` avant toute action.

## Déclencheur
- `git add/commit/push` échoue avec `index.lock`
- `fatal: Unable to create '.git/index.lock': File exists.`
- Tout processus git bloqué par un fichier `.lock`

## Protocole obligatoire

### Étape 1 — NE PAS supprimer immédiatement
```powershell
# ❌ INTERDIT — suppression aveugle
Remove-Item ".git\index.lock" -Force
```

### Étape 2 — Diagnostiquer le processus
```powershell
# Vérifier les processus git actifs
Get-Process -Name "git" -ErrorAction SilentlyContinue | Select Id, ProcessName, StartTime, CPU

# Vérifier les fichiers .lock
Get-ChildItem -LiteralPath ".git" -Filter "*.lock" -Recurse -ErrorAction SilentlyContinue | Select FullName, Length, LastWriteTime
```

### Étape 3 — Analyser la situation
| Cas | Action |
|-----|--------|
| Processus git vivant < 5 min | Attendre, ne pas toucher |
| Processus git mort > 5 min | Supprimer le .lock |
| Aucun processus git | Supprimer le .lock |
| `.lock` sur `.git/index.lock` avec WIP non commité | `git reset --hard` AVANT suppression |

### Étape 4 — Supprimer UNIQUEMENT si sûr
```powershell
# Après diagnostic confirmé
Remove-Item ".git\index.lock" -Force
```

### Étape 5 — Vérifier
```powershell
git status
```

## Anti-patterns bloquants
- Supprimer `.lock` sans diagnostic processus
- Tuer un processus git sans vérifier s'il est en cours de commit
- Ignorer un `.lock` sur `.git/index.lock` quand il y a du WIP
- Forcer `git reset --hard` sans sauvegarde préalable

## Référence ADR
- **ADR** : ADR-2026-08-10-003-GIT_LOCK_RESCUER
- **IntentHash** : 0xGIT_LOCK_RESCUER_20260810
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
