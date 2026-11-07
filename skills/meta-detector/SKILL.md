---
name: meta-detector
description: Skill de détection méta-gouvernance AUTO-DEV. Scanne les 7 sources méta (unified-design, citizens, SKILLS, PRIMUS, REPO-STANDARDS, LOOPX, personae) pour détecter les besoins écosystémiques. Utiliser pour meta-detection, scan méta, besoin écosystémique, ACT auto.
version: 1.0.0
author: gerivdb
license: MIT
triggers:
  - meta-detector
  - meta-detection
  - scan méta
  - besoin écosystémique
inputs:
  - name: source
    type: string
    description: Source méta à scanner (unified-design, citizens, SKILLS, PRIMUS, REPO-STANDARDS, LOOPX, personae)
  - name: base_path
    type: string
    description: Chemin de base du repo source
outputs:
  - name: detection
    type: dict
    description: Résultat du scan avec status, files, counts
tools:
  - filesystem
  - yaml-parser
  - json-writer
related_skills:
  - meta-governance-auto
  - friction-analysis
  - ontology-auditor
---

# Meta-Detector

Skill de détection méta-gouvernance AUTO-DEV.

## Mission

Scanner les 7 sources méta pour détecter les besoins écosystémiques.

## Sources

| Source | Rôle | Artefacts |
|--------|------|-----------|
| `unified-design` | Designs, friction_guard, MDU | `designs/`, `friction_guard/`, `mdu/` |
| `citizens` | Modules citoyens | `citizens/*.yaml`, `citizens/*.py` |
| `SKILLS` | Registre compétences | `skills/*/SKILL.md` |
| `PRIMUS` | Primitives atomiques | `REGISTRY.yaml`, `primitives/` |
| `REPO-STANDARDS` | Standards | `STANDARDS.md`, `PIANO/`, hooks |
| `LOOPX` | Routines | `routines/*.yaml`, `LOOPX-routines/` |
| `personae` | Collèges | `personae/*.yaml`, `colleges/*.yaml` |

## Intégration AUTO-DEV

- `agents/meta_detector.py`
- `agents/meta_executor.py`

## Références

- `PRD-021-auto-dev-meta-governance-auto.md`
- `MOC-025-auto-dev-meta-governance-auto.md`
- `TALEX/ONTOLOGY_DECLARATION.yaml` (concept: meta-detector)
