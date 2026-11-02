---
type: skill
version: "1.0.0"
date: "2026-11-02"
intent_hash: 0xBDCP_SAFE_PUSH_20261102
status: active
extends: bdcp-clapet-guard
---

# Skill: bdcp-safe-push

## Purpose
Effectuer un `git push` securise depuis n'importe quel repo de l'ecosysteme gerivdb sur ENV2, en respectant le mode BDCP (clapet ferme). Aucun `gh`, aucune interface web GitHub, aucun `--force` sans verification.

## Contexte important - proxy CDP

Le clapet BDCP ferme bloque les connexions directes sortantes. Pour qu'un `git push` fonctionne avec le clapet ferme, le trafic doit transiter par un proxy local. Sur ENV2, ce proxy est le **CDP sur `localhost:18000`**.

**Condition prealable obligatoire :** le proxy CDP doit etre demarre et ecouter sur `localhost:18000`. Si le proxy n'ecoute pas, `git push` ECHOUERA avec le clapet ferme (erreur de connexion, pas un echec de BDCP).

## Prerequisites
- Clapet BDCP ferme (bdcp-clapet-guard valide)
- Commit(s) effectue(s) localement (bdcp-atomic-commit valide)
- Remote `origin` configure (https://github.com/gerivdb/<repo>.git)
- Proxy CDP ecoutant sur `localhost:18000` (verifier avec Test-NetConnection)

## Workflow

### 1. Verifier que le clapet est ferme (pre-requis)
```powershell
# Le fichier $env:TEMP\ecos_clapet_state doit etre ABSENT (clapet ferme = BDCP mode)
Test-Path "$env:TEMP\ecos_clapet_state"
# Si le fichier existe -> clapet ouvert -> BDCP viole, STOP
```

### 2. Verifier que le proxy CDP ecoute sur 18000 (pre-requis)
```powershell
$proxyTest = Test-NetConnection -ComputerName localhost -Port 18000
if (-not $proxyTest.TcpTestSucceeded) {
    Write-Error "PROXY CDP NON DISPONIBLE sur localhost:18000"
    Write-Host "Le push git echouera avec le clapet ferme car aucune connexion directe nest autorisee."
    Write-Host "Actions possibles :"
    Write-Host "  a) Demarrer le proxy CDP sur 18000, puis reessayer"
    Write-Host "  b) Ouvrir le clapet (instruction explicite de l utilisateur requise)"
    exit 1
}
```

### 3. Verifier le remote (Etape 1)
```powershell
git -C "<repo_path>" remote -v
# Resultat attendu : origin  https://github.com/gerivdb/<REPO>.git (fetch)
#                    origin  https://github.com/gerivdb/<REPO>.git (push)
# Si mismatch -> git -C "<repo_path>" remote set-url origin <url_correcte>
```

### 4. Verifier la branche (Etape 2)
```powershell
git -C "<repo_path>" branch
# Si HEAD detache -> git -C "<repo_path>" checkout -B main HEAD
```

### 5. Verifier l'historique distant (Etape 3)
```powershell
git -C "<repo_path>" log origin/main --oneline -5
# Comparer avec l'historique local
```

### 6. Push sans force (Etape 4)
```powershell
# Push SANS --force
git -C "<repo_path>" push origin <branch>
# Le trafic transite par le proxy CDP localhost:18000 (si configure dans git)
# Aucun appel POST /clapet/open n'est necessaire
```

### 7. Verifier le resultat (Etape 5)
```powershell
git -C "<repo_path>" log --oneline -1
git -C "<repo_path>" log origin/main --oneline -1
# Les deux doivent afficher le meme commit HEAD
```

## Regles BDCP specifiques
- **Jamais `gh repo create`, `gh pr`, `gh issue`** (interdit par BDCP)
- **Jamais GitHub Actions / `.github/workflows/`**
- **Jamais interface web GitHub** pour creer/fusionner des PRs
- **Jamais `git push --force`** sans avoir verifie les etapes 1-3
- **Clapet BDCP reste ferme** - le trafic doit passer par le proxy CDP sur 18000
- **Sans proxy CDP sur 18000, git push echouera avec le clapet ferme**

## Anti-patterns interdits
- [KO] `git push --force` sans verifier remote, branche, historique
- [KO] Push sans verifier `git remote -v`
- [KO] Push sans verifier que le proxy CDP ecoute sur 18000
- [KO] Changer de repo sans utiliser `git -C` ou chemins absolus
- [KO] Utiliser `gh CLI` pour toute operation git

## Bloquants
| Condition | Action |
|---|---|
| Remote mismatch | Corriger l'URL avant de continuer |
| HEAD detache | `git checkout -B main HEAD` avant push |
| Distant ecrase | STOP - ne pas push, investiguer d'abord |
| Clapet BDCP ouvert | STOP - invoquer bdcp-clapet-guard |
| Proxy CDP non ecoutant sur 18000 | STOP - demarrer le proxy CDP ou ouvrir le clapet (instruction explicite) |

## Configuration git pour utiliser le proxy CDP (si necessaire)
```powershell
# Configurer git pour utiliser le proxy local sur toutes les operations
git config --global http.proxy http://localhost:18000
git config --global https.proxy http://localhost:18000
# Pour revenir a la connexion directe (quand le clapet est ouvert):
git config --global --unset http.proxy
git config --global --unset https.proxy
```

## References
- **Rule** : git-remote-safety.md (protocole avant push)
- **Rule** : bash-cwd-persistence.md (chemins absolus)
- **Rule** : bdcp-kiva-workflow.md (interdiction gh, GitHub Actions)
- **ADR** : ADR-094-git-remote-safety-protocol
- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
