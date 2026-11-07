# Skill: verify-dispatcher-cycle

Vérifie le cycle complet dispatcher Agent Manager V9.10 :
mission → router → runners forensiques → callback → WAL.

## Usage

```powershell
powershell -File ".kilo/skills/verify-dispatcher-cycle/verify-dispatcher-cycle.ps1"
```

## Ce que le skill vérifie

- Ports 18010-18015 en écoute
- Endpoints HTTP des runners (POST)
- Runners répondent `status: completed`
- WAL forensique et cognitif mis à jour
- Pas d'erreur dans la sortie du dispatcher

## Sortie attendue

- `[OK]` pour chaque vérification
- Résumé final avec latences par runner
- Exit code 0 si tout est OK, 1 sinon

## Intégration

- Appeler ce skill après tout déploiement de runners
- Appeler ce skill en post-merge pour valider l'opérationnalité
- Intégrer à `.kiva/pipelines/worktree-runners-validation.yaml`

## Références

- PRD MOC : `act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/architecture/PRD-MOC-AGENT-MANAGER-V9.10-OPERATIONAL-RUNNERS-2026-08-10.md`
- README : `.kilo/orchestrator/README-FORENSIC.md`
