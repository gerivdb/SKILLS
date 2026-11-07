---
name: meta-executor
description: Skill d'exécution méta-gouvernance AUTO-DEV. Orchestre P1→P7 via cycle_runner pour implémenter les PRD/MOC générés. Utiliser pour meta-execution, orchestration cycle, implémentation PRD/MOC, ACT auto.
version: 1.0.0
author: gerivdb
license: MIT
triggers:
  - meta-executor
  - meta-execution
  - orchestration cycle
  - implémentation PRD/MOC
inputs:
  - name: detection
    type: dict
    description: Résultat du scan méta
  - name: repo_cible
    type: string
    description: Repo cible pour l'implémentation
outputs:
  - name: result
    type: dict
    description: Résultat du cycle avec meta_result
tools:
  - cycle_runner
  - auto_debug_integrator
  - git-workflow-guardian
  - kiva-pr-workflow
related_skills:
  - meta-governance-auto
  - slm-micro-executor
  - kiva-pr-workflow
---

# Meta-Executor

Skill d'exécution méta-gouvernance AUTO-DEV.

## Mission

Orchestrer P1→P7 via cycle_runner pour implémenter les PRD/MOC générés.

## Séquencement

```
S0 — MetaDetection (meta_detector.py)
S1 — MetaClassification (meta_planner.py)
S2 — MetaPlanning (meta_planner.py)
S3 — MetaExecution (cycle_runner.py P1→P7)
S4 — MetaTrace (meta_trace.py)
```

## Intégration AUTO-DEV

- `agents/meta_executor.py`
- `agents/cycle_runner.py` (phase S0)

## Références

- `PRD-021-auto-dev-meta-governance-auto.md`
- `MOC-025-auto-dev-meta-governance-auto.md`
- `TALEX/ONTOLOGY_DECLARATION.yaml` (concept: meta-executor)
