---
type: skill
version: "1.0.0"
date: "2026-11-02"
intent_hash: 0xBDCP_FULL_WORKFLOW_20261102
status: active
extends:
  - bdcp-clapet-guard
  - bdcp-atomic-commit
  - bdcp-safe-push
  - bdcp-git-sync
---

# Skill: bdcp-full-workflow

## Purpose
Meta-skill orchestrant le workflow complet BDCP : verification clapet -> verification proxy CDP -> commit atomique -> sync avec remote -> push securise. Applicable depuis n'importe quel repo de l'ecosysteme gerivdb sur ENV2.

## Context
Ce skill remplace l'enchainement manuel de commandes git. Il garantit que chaque etape respecte les regles BDCP (clapet ferme, pas de gh, pas de force push, trafic proxyfie via CDP). Utilisable pour toute session de remediation, de feature, ou de hotfix sur un repo gerivdb.

## Contexte important - proxy CDP

Le clapet BDCP ferme bloque les connexions directes sortantes. Pour qu'un `git fetch` ou `git push` fonctionne avec le clapet ferme, le trafic doit transiter par un proxy local. Sur ENV2, ce proxy est le **CDP sur `localhost:18000`**.

**Condition prealable obligatoire :** le proxy CDP doit etre demarre et ecouter sur `localhost:18000`. Si le proxy n'ecoute pas, `git fetch` et `git push` ECHOUERONT avec le clapet ferme (erreur de connexion, pas un echec de BDCP).

## Prerequisites
- Repo git avec remote `origin` vers `https://github.com/gerivdb/<repo>.git`
- Clapet BDCP ferme (fichier `$env:TEMP\ecos_clapet_state` absent)
- Proxy CDP ecoutant sur `localhost:18000` (verifier avec Test-NetConnection)
- Aucun secret dans les fichiers a committer

## Workflow - Sequence obligatoire (6 etapes)

### ETAPE 1 - bdcp-clapet-guard (verification clapet ferme)
```powershell
# Le fichier $env:TEMP\ecos_clapet_state doit etre ABSENT
Test-Path "$env:TEMP\ecos_clapet_state"
# Si le fichier existe -> clapet ouvert -> BDCP viole, STOP
```

### ETAPE 2 - Verification proxy CDP (pre-requis pour fetch et push)
```powershell
$proxyTest = Test-NetConnection -ComputerName localhost -Port 18000
if (-not $proxyTest.TcpTestSucceeded) {
    Write-Error "PROXY CDP NON DISPONIBLE sur localhost:18000"
    Write-Host "Aucune operation reseau git ne peut reussir avec le clapet ferme sans proxy."
    Write-Host "Actions possibles :"
    Write-Host "  a) Demarrer le proxy CDP sur 18000, puis reessayer"
    Write-Host "  b) Ouvrir le clapet (instruction explicite de l utilisateur requise)"
    exit 1
}
```

### ETAPE 3 - bdcp-atomic-commit (commit local)
```powershell
# 1. Verifier l'etat du working tree
git -C "<repo_path>" status --short
git -C "<repo_path>" diff --stat

# 2. Selectionner max 3 fichiers
git -C "<repo_path>" add <fichier1> [<fichier2>] [<fichier3>]

# 3. Commit conventionnel
git -C "<repo_path>" commit -m "type(scope): description atomique"
# Exemple : feat(gateway-manager): add ONTOLOGY_DECLARATION.yaml

# 4. Verifier le commit
git -C "<repo_path>" log --oneline -1
```

### ETAPE 4 - bdcp-git-sync (synchronisation avec remote)
```powershell
# 1. Fetch explicite depuis le remote
git -C "<repo_path>" fetch origin

# 2. Verifier la divergence
git -C "<repo_path>" log --oneline main..origin/main   # commits distaux
git -C "<repo_path>" log --oneline origin/main..main   # commits locaux

# 3. Rebase si le remote a evolue
git -C "<repo_path>" rebase origin/main   # si necessaire

# 4. Resoudre les conflits s'il y en a
```

### ETAPE 5 - bdcp-safe-push (push vers remote)
```powershell
# 1. Verifier le remote (remote -v)
# 2. Verifier la branche (branch)
# 3. Verifier l'historique distant (log origin/main)
# 4. Push sans force
git -C "<repo_path>" push origin <branch>
# Le trafic est proxyfie par le CDP localhost:18000 - aucun POST /clapet/open

# 5. Verifier le resultat
git -C "<repo_path>" log --oneline -1
git -C "<repo_path>" log origin/main --oneline -1
```

### ETAPE 6 - Nettoyage post-push
```powershell
# Supprimer les branches locales deja mergees
git -C "<repo_path>" branch --merged main | grep -v "main" | xargs git -C "<repo_path>" branch -d
# Verifier l'etat final
git -C "<repo_path>" status --short
```

## Regles BDCP globales
| Regle | Application |
|---|---|
| Clapet ferme | Verifie a l'ETAPE 1, maintenu ferme toute la session |
| Proxy CDP sur 18000 | Verifie a l'ETAPE 2, requis pour fetch et push |
| Pas de `gh` CLI | Jamais utilise - `git` natif uniquement |
| Pas de GitHub Actions | Jamais cree ou invoque |
| Pas de web GitHub | Jamais utilise pour PR/merge |
| Pas de `--force` | Jamais sans verification etapes 1-3 de bdcp-safe-push |
| Chemins absolus | Toujours `git -C "<chemin_absolu>"` |
| Max 3 fichiers par commit | Applique a l'ETAPE 3 |
| Max 30 min entre commits | Commit WIP si necessaire |

## Anti-patterns interdits
- [KO] Ouvrir le clapet pour "debloquer" un push
- [KO] Utiliser `gh repo create` ou `gh pr`
- [KO] `git push --force` sans verification
- [KO] `git add -A` avec plus de 3 fichiers
- [KO] Session de plus de 30 min sans commit
- [KO] Fetch/push sans verifier que le proxy CDP ecoute sur 18000

## Exemple d'application (GATEWAY-MANAGER)
```powershell
# Session de remediation RSS-v2.3 sur GATEWAY-MANAGER
$repo = "D:\DO\WEB\TOOLS\L1-INFRA\GATEWAY-MANAGER"

# ETAPE 1 - Clapet ferme (verifie)
# ETAPE 2 - Proxy CDP sur 18000 (verifie)
# ETAPE 3 - Commit atomique
git -C $repo add REPO.yaml ONTOLOGY_DECLARATION.yaml CROSSLINKS/crosslinks.yaml
git -C $repo commit -m "feat: create ONTOLOGY_DECLARATION + CROSSLINKS bridges"
# ETAPE 4 - Sync (fetch + rebase si necessaire)
git -C $repo fetch origin
git -C $repo rebase origin/main
# ETAPE 5 - Push securise (via proxy CDP 18000)
git -C $repo push origin main
# ETAPE 6 - Nettoyage
git -C $repo branch --merged main | grep -v main | xargs git -C $repo branch -d
```

## Bloquants
| Condition | Action |
|---|---|
| Clapet BDCP ouvert | STOP - invoquer bdcp-clapet-guard |
| Proxy CDP non ecoutant sur 18000 | STOP - demarrer le proxy CDP ou ouvrir le clapet (instruction explicite) |
| Plus de 3 fichiers a committer | Diviser en plusieurs commits |
| Divergence non resolue | STOP - resoudre avant push |
| Conflits de rebase | STOP - resoudre avant push |
| Secret detecte dans les fichiers | STOP - retirer avant commit |

## References
- **Rule** : bdcp-kiva-workflow.md (interdiction gh, GitHub Actions, web)
- **Rule** : git-atomic-commit.md (max 3 fichiers, max 30 min)
- **Rule** : git-remote-safety.md (protocole avant push)
- **Rule** : bash-cwd-persistence.md (chemins absolus)
- **Rule** : pr-lifecycle-gate.md (nettoyage branches apres merge)
- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
- **ADR** : ADR-094-git-remote-safety-protocol
- **ADR** : ADR-099-git-atomic-commit
- **ADR** : ADR-2026-06-29-001 (fetch explicite avant rebase)
