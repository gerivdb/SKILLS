# Skill: repo-ref-validator

## Contexte
PRDs et EPICs référencent des chemins de fichiers et des noms de repos. Ces références deviennent des liens cassés quand les chemins changent ou que les repos sont renommés.

## Règle
Pour tout PRD/EPIC/INTENT modifié :
1. Parser le fichier pour extraire :
   - Chemins relatifs : `kiva_cli/...`, `packages/backend/...`, `specs/...`
   - Références de repo : `gerivdb/xxx`, `evalops/xxx`
   - Fichiers markdown : `[nom](chemin)` ou chemins inline
2. Pour chaque chemin : résoudre via `repo-path-resolver`, vérifier `Test-Path`
3. Pour chaque repo ref : vérifier dans `known_repositories.yaml` et `repos.json`
4. Générer `.kilo/ref-validation/BROKEN_REFS.txt` si applicable
5. Si liens cassés > 0 : refuser la validation pre-commit

## Types de références à valider
- Chemins de fichiers dans les sections “Fichier clé”, “Livrable”, “Deliverables”
- Repos dans les champs `repo:`, `owner:`, `full_name:`
- Liens markdown : `[text](relative/path)`
- Imports Python/JS : `from x.y import z` si `x.y` correspond à un chemin

## Anti-pattern interdit
- Référencer un fichier sans vérifier son existence
- Utiliser un nom de repo sans valider dans `known_repositories.yaml`
- Ignorer les liens cassés et pousser quand même

## Exemple d'application
```
EPIC KIVA-CLI référence :
  - `kiva_cli/commands/github_commands.py`
  - repo: gerivdb/KIVA-CLI
→ repo-path-resolver : D:\DO\WEB\TOOLS\L1-INFRA\KIVA-CLI
→ Test-Path kiva_cli/commands/github_commands.py : OK
→ known_repositories.yaml : gerivdb/KIVA-CLI trouvé
→ Validation : PASS
---
PRD référence :
  - `specs/pr_review_pipeline.yaml` dans NEXUS
→ NEXUS local_path : D:\DO\WEB\TOOLS\L0-CANON\NEXUS
→ Test-Path specs/pr_review_pipeline.yaml : OK
→ Validation : PASS
```
