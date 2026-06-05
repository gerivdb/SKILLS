# Skill: repo-state-auditor

## Contexte
Un repo peut exister localement avec un état avancé (phases implémentées, binaire buildé) alors que les EPICs le déclarent `planned`/`active`. Ce décalage génère des fausses alertes et des blocages injustifiés.

## Règle
Avant tout plan d'implémentation multi-repo :
1. Pour chaque repo dans `known_repositories.yaml`, vérifier `Test-Path <local_path>`
2. Si existe : lire `git log --oneline -5` + `git branch --show-current`
3. Comparer les commits récents avec les EPICs associés
4. Si EPIC `planned`/`active` mais commits correspondent à `completed`, proposer mise à jour automatique
5. Si repo n'existe pas, marquer `DO_NOT_CREATE` violation
6. Générer un rapport d'état avant toute action

## Rapport d'état
Pour chaque repo :
- `EXISTS` / `MISSING`
- `CLEAN` / `DIRTY` (working tree)
- `STATUS_MATCH` / `STATUS_MISMATCH` (EPIC vs commits)
- `REMOTE_OK` / `REMOTE_BROKEN`

## Anti-pattern interdit
- Déclarer un repo `planned` sans vérifier le filesystem
- Marquer `completed` sans preuve de commit
- Ignorer un repo existant avec du code avancé

## Exemple d'application
```
Repo : diffscope-fork
→ Test-Path : OK
→ git log : 8bdf4b6 phase-d: add kiva binary...
→ EPIC déclaré : planned
→ Détection : phases A/B/C/D implémentées
→ Action : marquer EPICs A/B/C/D/COORD completed
```
