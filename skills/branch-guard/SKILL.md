# Skill: branch-guard

## Contexte
Un commit créé sur la mauvaise branche (ex: `feature/tql-deprecation` au lieu de `main`) nécessite des opérations de récupération (cherry-pick, rebase) et expose à des conflits.

## Règle
Avant tout commit :
1. Lire l'EPIC/PRD pour déterminer la branche cible (champ `repo:` ou convention `main`)
2. Exécuter `git branch --show-current`
3. Si mismatch, proposer checkout cible ou demander confirmation
4. Interdire commit sur branche feature sans ordre explicite
5. Logger la branche utilisée dans le commit message

## Convention
- `main` = branche par défaut pour livraisons
- `feature/*` = branche de travail, ne se commit pas directement sans ordre
- Si pas de convention dans l'EPIC, demander avant commit

## Anti-pattern interdit
- Committer sur `feature/*` sans vérification
- Créer un commit puis s'apercevoir de la mauvaise branche
- Push forcé pour corriger une dérive de branche

## Exemple d'application
```
EPIC cible : NEXUS, contrat pr_review_pipeline.yaml
→ Branche attendue : main
→ git branch --show-current : feature/tql-deprecation
→ Action : checkout main avant commit
→ Commit sur main, pas sur feature
```
