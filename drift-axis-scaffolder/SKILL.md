---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_DRIFT_AXIS_SCAFFOLDER_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/drift-axis-scaffolder/SKILL.md
---

# Skill — drift-axis-scaffolder

Ajouter un axe à DRIFT-ENGINE.

## Objectifs
- Injecter un nouvel axe dans la config DRIFT-ENGINE
- Générer le metric correspondant
- Valider la conformité

## Entrées
- `axis_name`: nom de l’axe
- `config_path`: chemin vers la config DRIFT-ENGINE

## Sorties
- `Path`: fichier de config modifié

## Tests
- `tests/test_drift_axis_scaffolder.py`
