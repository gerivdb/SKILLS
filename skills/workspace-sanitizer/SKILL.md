# Skill: workspace-sanitizer

## Contexte
Un working tree sale (modifications non liées, suppressions massives) contamine les commits et expose au risque de `git add .` destructeur.

## Règle
Avant tout commit/push :
1. Exécuter `git status --short`
2. Si `working tree clean` : procéder
3. Si changements non liés au livrable : émettre alerte `WORKSPACE_DIRTY`
4. Refuser `git add .` — n’autoriser que `git add <fichier>` explicite
5. Si plus de 10 fichiers modifiés non liés, demander confirmation humaine
6. Ne jamais committer sur un repo avec des deletions massives non vérifiées

## Anti-pattern interdit
- `git add .` dans un repo avec 90+ fichiers modifiés
- Committer sans lister les fichiers avec `git status --short`
- Ignorer les warnings LF/CRLF sans vérifier l’impact

## Exemple d'application
```
NEXUS : 98 fichiers modifiés (deletions managers/, ajouts audit/)
→ git status --short révèle la pollution
→ Refus de git add .
→ Seul specs/pr_review_pipeline.yaml est ajouté
→ Commit propre, pas de contamination
```
