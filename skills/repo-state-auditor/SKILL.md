# Skill: repo-state-auditor

## Contexte
Un repo peut exister localement avec un etat avance (phases implementees, binaire builde) alors que les EPICs le declarent `planned`/`active`. Ce decalage genere des fausses alertes et des blocages injustifies.

## Regle
Avant tout plan d'implementation multi-repo :
1. Pour chaque repo dans `known_repositories.yaml`, verifier `Test-Path <local_path>`
2. Si existe : lire `git log --oneline -5` + `git branch --show-current`
3. Comparer les commits recents avec les EPICs associes
4. Si EPIC `planned`/`active` mais commits correspondent a `completed`, proposer mise a jour automatique
5. Si repo n'existe pas, marquer `DO_NOT_CREATE` violation
6. Generer un rapport d'etat avant toute action

## Rapport d'etat
Pour chaque repo :
- `EXISTS` / `MISSING`
- `CLEAN` / `DIRTY` (working tree)
- `STATUS_MATCH` / `STATUS_MISMATCH` (EPIC vs commits)
- `REMOTE_OK` / `REMOTE_BROKEN`

## Anti-pattern interdit
- Declarer un repo `planned` sans verifier le filesystem
- Marquer `completed` sans preuve de commit
- Ignorer un repo existant avec du code avance

## Exemple d'application
```
Repo : diffscope-fork
-> Test-Path : OK
-> git log : 8bdf4b6 phase-d: add kiva binary...
-> EPIC declare : planned
-> Detection : phases A/B/C/D implementees
-> Action : marquer EPICs A/B/C/D/COORD completed
```
