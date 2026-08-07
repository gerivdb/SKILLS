# Skill: branch-guard

## Contexte
Un commit cree sur la mauvaise branche (ex: `feature/tql-deprecation` au lieu de `main`) necessite des operations de recuperation (cherry-pick, rebase) et expose a des conflits.

## Regle
Avant tout commit :
1. Lire l'EPIC/PRD pour determiner la branche cible (champ `repo:` ou convention `main`)
2. Executer `git branch --show-current`
3. Si mismatch, proposer checkout cible ou demander confirmation
4. Interdire commit sur branche feature sans ordre explicite
5. Logger la branche utilisee dans le commit message

## Convention
- `main` = branche par defaut pour livraisons
- `feature/*` = branche de travail, ne se commit pas directement sans ordre
- Si pas de convention dans l'EPIC, demander avant commit

## Anti-pattern interdit
- Committer sur `feature/*` sans verification
- Creer un commit puis s'apercevoir de la mauvaise branche
- Push force pour corriger une derive de branche

## Exemple d'application
```
EPIC cible : NEXUS, contrat pr_review_pipeline.yaml
-> Branche attendue : main
-> git branch --show-current : feature/tql-deprecation
-> Action : checkout main avant commit
-> Commit sur main, pas sur feature
```
