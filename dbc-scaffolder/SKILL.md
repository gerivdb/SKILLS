---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_DBC_SCAFFOLDER_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/dbc-scaffolder/SKILL.md
---

# Skill — dbc-scaffolder

Générer des contrats DbC depuis un contrat YAML.

## Objectifs
- Générer `contracts/preconditions.py`, `postconditions.py`, `invariants.py`
- Utiliser `deal` comme moteur de contrat

## Entrées
- `skill_path`: chemin de la skill
- `contract_path`: chemin du contrat YAML

## Sorties
- `list[Path]`: fichiers créés

## Tests
- `tests/test_dbc_scaffolder.py`
