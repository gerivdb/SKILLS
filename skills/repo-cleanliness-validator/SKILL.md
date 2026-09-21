---
type: skill
version: "1.0.0"
date: "2026-09-15"
status: draft
intent_hash: 0xREPO_CLEANLINESS_VALIDATOR_20260915
---

# Skill: repo-cleanliness-validator

## Purpose
Vérifie la propreté des working trees sur N repos et signale les drifts non commités.
Évite les oublis de commit en fin de session.

## Context
Utilisé en fin de session KiloCode ou avant une opération critique (deploy, sync).
Scan les repos actifs listés dans `known_repositories.yaml`.

## Prerequisites
- Accès aux repos locaux
- `git` en PATH
- `known_repositories.yaml` à jour

## Workflow

### 1. Charger la liste des repos
```powershell
# Lire known_repositories.yaml
# Extraire les local_path des repos actifs
```

### 2. Vérifier chaque repo
```powershell
foreach ($repo in $repos) {
    git -C $repo status --short
    git -C $repo diff --stat
}
```

### 3. Classifier les drifts
| Type | Action |
|------|--------|
| Clean | ✅ OK |
| Modified (tracked) | ⚠️ Signaler |
| Untracked | ⚠️ Signaler |
| Ahead/Behind | ❌ Bloquer |

### 4. Rapport
```
[CLEANLINESS] repo=<name> status=<clean|dirty> files=<n> action=<commit|stash|revert>
```

## Anti-patterns
- ❌ Signaler sans classifier
- ❌ Ignorer les repos avec 0 modification
- ❌ Commit automatique sans validation humaine

## References
- **Rule** : git-atomic-commit.md
- **Skill** : git-atomic-push
- **Pattern** : Pattern A (read atomique)
