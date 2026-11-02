---
type: skill
version: "1.0.0"
date: "2026-11-02"
intent_hash: 0xBDCP_ATOMIC_COMMIT_20261102
status: active
extends: bdcp-clapet-guard
---

# Skill: bdcp-atomic-commit

## Purpose
Effectuer des commits atomiques conformes aux regles KiloCode et BDCP : maximum 3 fichiers modifies par commit, maximum 30 minutes entre deux commits, message de commit conventionnel, verification du clapet BDCP ferme avant toute operation.

## Context
Ce skill remplace les commandes `git add -A` avec plus de 10 fichiers et les sessions de plus d'1 heure sans commit. Chaque commit doit etre atomique (un seul livrable) et tracable.

## Prerequisites
- Clapet BDCP ferme (verifie via bdcp-clapet-guard)
- Repo git avec remote configure (gerivdb/<repo>)
- Fichiers modifies identifies et cibles (pas de `git add -A` aveugle)

## Workflow

### 1. Verifier le clapet BDCP (pre-requis)
```powershell
# Invoquer bdcp-clapet-guard avant tout commit
# Le clapet doit etre ferme
```

### 2. Verifier l'etat du working tree
```powershell
git -C "<repo_path>" status --short
git -C "<repo_path>" diff --stat
git -C "<repo_path>" log --oneline -3
```

### 3. Selectionner max 3 fichiers par commit
```powershell
# [KO] INTERDIT : git add -A avec plus de 3 fichiers
# [OK] OBLIGATOIRE : selection ciblee
git -C "<repo_path>" add <fichier1> <fichier2> <fichier3>
```

### 4. Commit atomique avec message conventionnel
```powershell
git -C "<repo_path>" commit -m "type(scope): description atomique"
# Exemples de types : feat, fix, refactor, chore, docs, style, test
# Exemple : feat(gateway-manager): add ONTOLOGY_DECLARATION.yaml
```

### 5. Verifier le commit
```powershell
git -C "<repo_path>" log --oneline -1
git -C "<repo_path>" status --short
```

## Regles BDCP specifiques
- **Max 3 fichiers modifies entre deux commits**
- **Max 30 minutes entre deux commits** - si une tache prend plus de 30 min, committer en WIP
- **Message de commit conventionnel** : `type(scope): description`
- **Pas de secrets** dans les fichiers commites
- **Pas de `git add -A`** avec plus de 3 fichiers

## Anti-patterns interdits
- [KO] Session de plus de 30 min sans commit
- [KO] Commit avec message vague ("WIP", "updates", "everything")
- [KO] `git add -A` avec plus de 3 fichiers modifies
- [KO] Commit sans avoir verifie le clapet BDCP ferme

## Bloquants
| Condition | Action |
|---|---|
| Plus de 3 fichiers a committer | Diviser en plusieurs commits atomiques |
| Plus de 30 min ecoulees sans commit | Commit WIP intermediaire |
| Clapet BDCP ouvert | STOP - invoquer bdcp-clapet-guard |
| Secret detecte dans les fichiers | STOP - retirer le secret avant commit |

## References
- **Rule** : git-atomic-commit.md (max 3 fichiers, max 30 min)
- **Rule** : bash-cwd-persistence.md (chemins absolus)
- **Rule** : bdcp-kiva-workflow.md (BDCP mode permanent)
- **ADR** : ADR-099-git-atomic-commit
- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
