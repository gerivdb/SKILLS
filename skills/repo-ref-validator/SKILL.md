# Skill: repo-ref-validator

## Contexte
PRDs et EPICs referencent des chemins de fichiers et des noms de repos. Ces references deviennent des liens casses quand les chemins changent ou que les repos sont renommes.

## Regle
Pour tout PRD/EPIC/INTENT modifie :
1. Parser le fichier pour extraire :
   - Chemins relatifs : `kiva_cli/...`, `packages/backend/...`, `specs/...`
   - References de repo : `gerivdb/xxx`, `evalops/xxx`
   - Fichiers markdown : `[nom](chemin)` ou chemins inline
2. Pour chaque chemin : resoudre via `repo-path-resolver`, verifier `Test-Path`
3. Pour chaque repo ref : verifier dans `known_repositories.yaml` et `repos.json`
4. Generer `.kilo/ref-validation/BROKEN_REFS.txt` si applicable
5. Si liens casses > 0 : refuser la validation pre-commit

## Types de references a valider
- Chemins de fichiers dans les sections "Fichier cle", "Livrable", "Deliverables"
- Repos dans les champs `repo:`, `owner:`, `full_name:`
- Liens markdown : `[text](relative/path)`
- Imports Python/JS : `from x.y import z` si `x.y` correspond a un chemin

## Anti-pattern interdit
- Referencer un fichier sans verifier son existence
- Utiliser un nom de repo sans valider dans `known_repositories.yaml`
- Ignorer les liens casses et pousser quand meme

## Exemple d'application
```
EPIC KIVA-CLI reference :
  - `kiva_cli/commands/github_commands.py`
  - repo: gerivdb/KIVA-CLI
-> repo-path-resolver : D:\DO\WEB\TOOLS\L1-INFRA\KIVA-CLI
-> Test-Path kiva_cli/commands/github_commands.py : OK
-> known_repositories.yaml : gerivdb/KIVA-CLI trouve
-> Validation : PASS
---
PRD reference :
  - `specs/pr_review_pipeline.yaml` dans NEXUS
-> NEXUS local_path : D:\DO\WEB\TOOLS\L0-CANON\NEXUS
-> Test-Path specs/pr_review_pipeline.yaml : OK
-> Validation : PASS
```
