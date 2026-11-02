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
Effectuer un `git push` securise depuis n'importe quel repo de l'ecosysteme gerivdb sur ENV2, en respectant le mode BDCP (clapet ferme, trafic proxyfie via CDP). Aucun `gh`, aucune interface web GitHub, aucun `--force` sans verification.

## Context
Le push git est l'operation la plus sensible car elle sort du workspace local. Sur ENV2 (HP Z600, 2 Xeon E5620, 24 Go DDR3), le push doit transiter par le proxy CDP et non par une connexion directe. Ce skill applique le protocole de securite avant chaque push.

## Prerequisites
- Clapet BDCP ferme (bdcp-clapet-guard valide)
- Commit(s) effectue(s) localement (bdcp-atomic-commit valide)
- Remote `origin` configure (https://github.com/gerivdb/<repo>.git)

## Workflow

### 1. Verifier le remote (Etape 1)
```powershell
# Verifier que le remote correspond au repo attendu
git -C "<repo_path>" remote -v
# Resultat attendu : origin  https://github.com/gerivdb/<REPO>.git (fetch)
#                    origin  https://github.com/gerivdb/<REPO>.git (push)
# Si mismatch -> git -C "<repo_path>" remote set-url origin <url_correcte>
```

### 2. Verifier la branche (Etape 2)
```powershell
# Verifier qu'on est sur la bonne branche (pas de HEAD detache)
git -C "<repo_path>" branch
# Si HEAD detache -> git -C "<repo_path>" checkout -B main HEAD
```

### 3. Verifier l'historique distant (Etape 3)
```powershell
# Verifier que le distant n'a pas ete ecrase
git -C "<repo_path>" log origin/main --oneline -5
# Comparer avec l'historique local
```

### 4. Push sans force (Etape 4)
```powershell
# Push SANS --force
git -C "<repo_path>" push origin <branch>
# Le trafic est automatiquement proxyfie par le CDP (localhost:18000)
# Aucun appel POST /clapet/open n'est necessaire
```

### 5. Verifier le resultat (Etape 5)
```powershell
# Confirmer que le push a ete accepte
git -C "<repo_path>" log --oneline -1
git -C "<repo_path>" log origin/main --oneline -1
# Les deux doivent afficher le meme commit HEAD
```

## Regles BDCP specifiques
- **Jamais `gh repo create`, `gh pr`, `gh issue`** (interdit par BDCP)
- **Jamais GitHub Actions / `.github/workflows/`**
- **Jamais interface web GitHub** pour creer/fusionner des PRs
- **Jamais `git push --force`** sans avoir verifie les etapes 1-3
- **Clapet BDCP reste ferme** - le trafic passe par le proxy CDP

## Anti-patterns interdits
- [KO] `git push --force` sans verifier remote, branche, historique
- [KO] Push sans verifier `git remote -v`
- [KO] Changer de repo sans utiliser `git -C` ou chemins absolus
- [KO] Utiliser `gh CLI` pour toute operation git

## Bloquants
| Condition | Action |
|---|---|
| Remote mismatch | Corriger l'URL avant de continuer |
| HEAD detache | `git checkout -B main HEAD` avant push |
| Distant ecrase | STOP - ne pas push, investiguer d'abord |
| Clapet BDCP ouvert | STOP - invoquer bdcp-clapet-guard |

## References
- **Rule** : git-remote-safety.md (protocole avant push)
- **Rule** : bash-cwd-persistence.md (chemins absolus)
- **Rule** : bdcp-kiva-workflow.md (interdiction gh, GitHub Actions)
- **ADR** : ADR-094-git-remote-safety-protocol
- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
