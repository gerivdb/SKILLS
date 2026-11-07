---
name: dry-run-causal
description: Skill de dry-run causal AUTO-DEV. Vérifie la production readiness avant implémentation. Utiliser pour dry-run, causal verification, production readiness, ACT auto, validation avant implémentation.
version: 1.0.0
author: gerivdb
license: MIT
triggers:
  - dry-run-causal
  - dry run
  - causal verification
  - production readiness
  - validation avant implémentation
inputs:
  - name: target
    type: string
    description: Cible de vérification (repo, design, PRD/MOC)
  - name: scope
    type: list
    description: Périmètre de vérification
outputs:
  - name: report
    type: dict
    description: Rapport de dry-run causal
  - name: ready
    type: boolean
    description: Production ready ou non
tools:
  - git-diff
  - pytest
  - yaml-validator
  - filesystem-proof
related_skills:
  - meta-governance-auto
  - friction-analysis
  - talex-structural-fixes-applier
---

# Dry-Run Causal

Skill de dry-run causal AUTO-DEV.

## Mission

Vérifier la production readiness avant implémentation.

## Protocole

1. Lire le PRD/MOC cible
2. Vérifier les dépendances
3. Valider les bridges
4. Tester les readers/writers
5. Générer le rapport

## Intégration AUTO-DEV

- `src/auto_debug_integrator.py`
- `agents/meta_detector.py`
- `agents/meta_executor.py`

## Références

- `PRD-021-auto-dev-meta-governance-auto.md`
- `MOC-025-auto-dev-meta-governance-auto.md`
- `TALEX/ONTOLOGY_DECLARATION.yaml` (concept: dry-run-causal)
