---
name: meta-planner
description: Skill de planification méta-gouvernance AUTO-DEV. Classifie les besoins détectés, génère PRD/MOC, planifie tâches atomiques. Utiliser pour meta-planning, classification besoin, génération PRD/MOC, planification atomique, ACT auto.
version: 1.0.0
author: gerivdb
license: MIT
triggers:
  - meta-planner
  - meta-planning
  - classification besoin
  - génération PRD/MOC
  - planification atomique
inputs:
  - name: detection
    type: dict
    description: Résultat du scan méta
  - name: need_index
    type: int
    description: Index du besoin à planifier
outputs:
  - name: plan
    type: dict
    description: Plan d'action avec PRD/MOC paths et tâches
  - name: tasks
    type: list
    description: Liste des tâches atomiques
tools:
  - yaml-writer
  - markdown-generator
  - task-planner
related_skills:
  - meta-governance-auto
  - atomic-task-planner
  - governance-doc-writer
---

# Meta-Planner

Skill de planification méta-gouvernance AUTO-DEV.

## Mission

Classifier les besoins détectés, générer PRD/MOC, planifier tâches atomiques.

## Catégories de besoins

| Catégorie | Détection | Action |
|-----------|-----------|--------|
| **Friction/ERR** | `unified-design` friction_guard + MDU | PRD/MOC fix + implémentation atomique |
| **Duplication** | `SKILLS` + `PRIMUS` vs `agents/`, `tools/` | PRD/MOC dedup + refactor |
| **Conformité** | `REPO-STANDARDS` vs code/docs | PRD/MOC standards + correction |
| **Routine manquante** | `LOOPX` routines vs workflows manuels | PRD/MOC automation + routine LOOPX |
| **Citizen absent** | `citizens` registry vs usage | PRD/MOC citizen + intégration |
| **Primitive absente** | `PRIMUS` registry vs besoins | PRD/MOC primitive + implémentation |
| **Collège invoqué** | `personae` colleges vs décisions | MOC invocation + traçabilité |

## Intégration AUTO-DEV

- `agents/meta_planner.py`
- `agents/meta_executor.py`

## Références

- `PRD-021-auto-dev-meta-governance-auto.md`
- `MOC-025-auto-dev-meta-governance-auto.md`
- `TALEX/ONTOLOGY_DECLARATION.yaml` (concept: meta-planner)
