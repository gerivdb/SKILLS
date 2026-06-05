# Skill: repo-path-resolver

## Contexte
Tout agent Kilo opérant cross-repo doit résoudre le chemin canonique d'un repo avant toute opération. La knowledge base des chemins est `known_repositories.yaml`.

## Règle
Avant toute opération sur un repo nommé :
1. Lire `D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB/known_repositories.yaml`
2. Extraire `local_path` depuis l'entrée correspondant à `name` ou `full_name`
3. Vérifier existence par `Test-Path <local_path>`
4. Si absent : lever erreur `REPO_PATH_NOT_FOUND`, ne pas deviner
5. Si présent : utiliser ce chemin pour toutes les opérations (read/write/edit/bash)

## Anti-pattern interdit
- Déduire le chemin depuis le nom du repo
- Utiliser `C:\DevTools\<repo>` sans vérification
- Créer un répertoire si le chemin n'existe pas sans ordre explicite

## Checklist pré-opération
- [ ] `known_repositories.yaml` lu
- [ ] `local_path` extrait
- [ ] `Test-Path` confirmé
- [ ] Chemin utilisé pour la commande courante

## Exemple d'application
```
Repo demandé : GOVERNANCE-HUB
→ known_repositories.yaml : local_path: D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB
→ Test-Path : OK
→ Opérations sur D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB
```
