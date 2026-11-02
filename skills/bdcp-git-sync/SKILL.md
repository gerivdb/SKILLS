---
type: skill
version: "1.0.0"
date: "2026-11-02"
intent_hash: 0xBDCP_GIT_SYNC_20261102
status: active
extends: bdcp-safe-push
---

# Skill: bdcp-git-sync

## Purpose
Synchroniser un repo local avec son remote GitHub (fetch, verification de divergence, rebase si necessaire) en respectant le mode BDCP. Ce skill s'applique avant tout push ou apres tout pull pour s'assurer que le working tree est coherent avec le remote.

## Context
Sur ENV2, plusieurs sessions KiloCode peuvent travailler sur le meme repo. Avant de push, il faut verifier que le remote n'a pas evolue de maniere incompatible. Ce skill applique un fetch explicite suivi d'une verification de divergence.

## Prerequisites
- Clapet BDCP ferme (bdcp-clapet-guard valide)
- Remote `origin` configure
- Working tree propre (ou commits en attente)

## Workflow

### 1. Fetch explicite depuis le remote
```powershell
# Recuperer les metadonnees du remote sans merger
git -C "<repo_path>" fetch origin
# Le trafic passe par le proxy CDP (localhost:18000)
```

### 2. Verifier la divergence avec le remote
```powershell
# Verifier si le remote a des commits que le local n'a pas
git -C "<repo_path>" log --oneline origin/main..main
# Commits locaux non pushes

git -C "<repo_path>" log --oneline main..origin/main
# Commits distaux non presents localement
```

### 3. Decision selon la divergence
```powershell
# Cas A : Remote a des commits que le local n'a pas
# -> Rebase ou merge avant push
git -C "<repo_path>" rebase origin/main
# Ou : git -C "<repo_path>" merge origin/main

# Cas B : Local a des commits que le remote n'a pas
# -> Proceder au push (bdcp-safe-push)

# Cas C : Les deux ont des commits uniques (divergence)
# -> STOP - resoudre manuellement avant de continuer
```

### 4. Rebase si necessaire (post-merge fetch explicite)
```powershell
# Protocole : fetch explicite avant rebase (ADR-2026-06-29-001)
git -C "<repo_path>" fetch origin
git -C "<repo_path>" rebase origin/main
# Resoudre les conflits si necessaire
```

### 5. Verifier l'etat final
```powershell
git -C "<repo_path>" status --short
git -C "<repo_path>" log --oneline -3
# Le working tree doit etre coherent avec le remote
```

## Regles BDCP specifiques
- **Fetch explicite avant rebase** (ADR-2026-06-29-001)
- **Clapet BDCP ferme** - le fetch passe par le proxy CDP
- **Jamais `git pull` sans verification prealable** (pull = fetch + merge implicite)
- **Jamais `git push --force`** apres rebase sans avoir verifie les etapes 1-3 de bdcp-safe-push

## Anti-patterns interdits
- [KO] `git pull` sans avoir verifie le remote d'abord
- [KO] Rebase sans avoir fait fetch explicite
- [KO] Push apres rebase sans verification du remote
- [KO] Ignorer les conflits de rebase

## Bloquants
| Condition | Action |
|---|---|
| Divergence (commits uniques des deux cotes) | STOP - resoudre manuellement |
| Conflits de rebase non resolus | STOP - ne pas push |
| Clapet BDCP ouvert | STOP - invoquer bdcp-clapet-guard |
| Remote non accessible | Verifier le proxy CDP (localhost:18000) |

## References
- **Rule** : git-remote-safety.md (protocole avant push)
- **Rule** : bash-cwd-persistence.md (chemins absolus)
- **ADR** : ADR-2026-06-29-001 (protocole fetch explicite avant rebase)
- **ADR** : ADR-094-git-remote-safety-protocol
- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
