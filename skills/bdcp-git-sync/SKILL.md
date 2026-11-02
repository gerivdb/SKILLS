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

## Contexte important - proxy CDP

Le clapet BDCP ferme bloque les connexions directes sortantes. Pour qu'un `git fetch` fonctionne avec le clapet ferme, le trafic doit transiter par un proxy local. Sur ENV2, ce proxy est le **CDP sur `localhost:18000`**.

**Condition prealable obligatoire :** le proxy CDP doit etre demarre et ecouter sur `localhost:18000`. Si le proxy n'ecoute pas, `git fetch` ECHOUERA avec le clapet ferme (erreur de connexion, pas un echec de BDCP).

## Prerequisites
- Clapet BDCP ferme (bdcp-clapet-guard valide)
- Remote `origin` configure
- Working tree propre (ou commits en attente)
- Proxy CDP ecoutant sur `localhost:18000` (verifier avec Test-NetConnection)

## Workflow

### 1. Verifier que le clapet est ferme (pre-requis)
```powershell
Test-Path "$env:TEMP\ecos_clapet_state"
# Si le fichier existe -> clapet ouvert -> BDCP viole, STOP
```

### 2. Verifier que le proxy CDP ecoute sur 18000 (pre-requis)
```powershell
$proxyTest = Test-NetConnection -ComputerName localhost -Port 18000
if (-not $proxyTest.TcpTestSucceeded) {
    Write-Error "PROXY CDP NON DISPONIBLE sur localhost:18000"
    Write-Host "Le fetch git echouera avec le clapet ferme."
    Write-Host "Actions possibles : demarrer le proxy CDP sur 18000, ou ouvrir le clapet (instruction explicite requise)"
    exit 1
}
```

### 3. Fetch explicite depuis le remote
```powershell
# Recuperer les metadonnees du remote sans merger
git -C "<repo_path>" fetch origin
# Le trafic transite par le proxy CDP localhost:18000 (si configure dans git)
```

### 4. Verifier la divergence avec le remote
```powershell
# Verifier si le remote a des commits que le local n'a pas
git -C "<repo_path>" log --oneline origin/main..main
# Commits locaux non pushes

git -C "<repo_path>" log --oneline main..origin/main
# Commits distaux non presents localement
```

### 5. Decision selon la divergence
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

### 6. Rebase si necessaire (post-merge fetch explicite)
```powershell
# Protocole : fetch explicite avant rebase (ADR-2026-06-29-001)
git -C "<repo_path>" fetch origin
git -C "<repo_path>" rebase origin/main
# Resoudre les conflits si necessaire
```

### 7. Verifier l'etat final
```powershell
git -C "<repo_path>" status --short
git -C "<repo_path>" log --oneline -3
# Le working tree doit etre coherent avec le remote
```

## Regles BDCP specifiques
- **Fetch explicite avant rebase** (ADR-2026-06-29-001)
- **Clapet BDCP ferme** - le fetch passe par le proxy CDP sur 18000
- **Jamais `git pull` sans verification prealable** (pull = fetch + merge implicite)
- **Jamais `git push --force`** apres rebase sans avoir verifie les etapes 1-3 de bdcp-safe-push
- **Sans proxy CDP sur 18000, git fetch echouera avec le clapet ferme**

## Anti-patterns interdits
- [KO] `git pull` sans avoir verifie le remote d'abord
- [KO] Rebase sans avoir fait fetch explicite
- [KO] Push apres rebase sans verification du remote
- [KO] Ignorer les conflits de rebase
- [KO] Fetch sans verifier que le proxy CDP ecoute sur 18000

## Bloquants
| Condition | Action |
|---|---|
| Divergence (commits uniques des deux cotes) | STOP - resoudre manuellement |
| Conflits de rebase non resolus | STOP - ne pas push |
| Clapet BDCP ouvert | STOP - invoquer bdcp-clapet-guard |
| Proxy CDP non ecoutant sur 18000 | STOP - demarrer le proxy CDP ou ouvrir le clapet (instruction explicite) |

## Configuration git pour utiliser le proxy CDP (si necessaire)
```powershell
git config --global http.proxy http://localhost:18000
git config --global https.proxy http://localhost:18000
# Pour revenir a la connexion directe (quand le clapet est ouvert):
git config --global --unset http.proxy
git config --global --unset https.proxy
```

## References
- **Rule** : git-remote-safety.md (protocole avant push)
- **Rule** : bash-cwd-persistence.md (chemins absolus)
- **ADR** : ADR-2026-06-29-001 (protocole fetch explicite avant rebase)
- **ADR** : ADR-094-git-remote-safety-protocol
- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
