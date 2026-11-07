---
name: meta-governance-auto
description: Skill de méta-gouvernance automatique TALEX/AUTO-DEV. Détecte les besoins écosystémiques via 7 sources (unified-design, citizens, SKILLS, PRIMUS, REPO-STANDARDS, LOOPX, personae), classifie, génère PRD/MOC, planifie tâches atomiques, exécute et trace. Utiliser pour meta-governance, auto-detection, besoin écosystémique, méta-gouvernance, ACT auto.
version: 1.0.0
author: gerivdb
license: MIT
triggers:
  - meta-governance-auto
  - meta-governance
  - auto-detection
  - besoin écosystémique
  - méta-gouvernance
  - ACT auto
inputs:
  - name: detection
    type: dict
    description: Résultat du scan des 7 sources méta
  - name: repo_cible
    type: string
    description: Repo cible pour l'implémentation
outputs:
  - name: plan
    type: dict
    description: Plan d'action avec PRD/MOC et tâches
  - name: trace
    type: dict
    description: Traçabilité NEXUS/WAZAA/MIMIR
tools:
  - meta_detector
  - meta_planner
  - meta_executor
  - meta_trace
  - cycle_runner
  - auto_debug_integrator
related_skills:
  - atomic-task-planner
  - slm-micro-executor
  - friction-analysis
  - talex-structural-fixes-applier
---

# Meta-Governance Auto

Skill de méta-gouvernance automatique TALEX/AUTO-DEV.

## Mission

Détecter automatiquement, via les runners cognitifs et les repos structurels de l'écosystème, les besoins qui motivent actuellement des prompts manuels, puis produire et implémenter les PRD/MOC/corrections correspondants.

## Sources méta

| Repo | Rôle | Artefacts |
|------|------|-----------|
| `unified-design` | Designs, friction_guard, MDU | `designs/`, `friction_guard/`, `mdu/` |
| `citizens` | Modules citoyens | `citizens/*.yaml`, `citizens/*.py` |
| `SKILLS` | Registre compétences | `skills/*/SKILL.md` |
| `PRIMUS` | Primitives atomiques | `REGISTRY.yaml`, `primitives/` |
| `REPO-STANDARDS` | Standards | `STANDARDS.md`, `PIANO/`, hooks |
| `LOOPX` | Routines | `routines/*.yaml`, `LOOPX-routines/` |
| `personae` | Collèges | `personae/*.yaml`, `colleges/*.yaml` |

## Séquencement

```
S0 — MetaDetection
S1 — MetaClassification
S2 — MetaPlanning
S3 — MetaExecution
S4 — MetaTrace
```

## Intégration AUTO-DEV

- `agents/meta_detector.py`
- `agents/meta_planner.py`
- `agents/meta_executor.py`
- `agents/meta_trace.py`
- `agents/meta_writers.py`
- `agents/cycle_runner.py` (phase S0)
- `src/auto_debug_integrator.py` (`detect_meta_needs()`)

## Références

- `PRD-021-auto-dev-meta-governance-auto.md`
- `MOC-025-auto-dev-meta-governance-auto.md`
- `RESEARCH_DIRECTIONS.md` Axe 4
- `TALEX/ONTOLOGY_DECLARATION.yaml`
- `TALEX/designs/meta-governance-auto.yaml`
- `TALEX/pipelines/meta-governance-auto.md`
