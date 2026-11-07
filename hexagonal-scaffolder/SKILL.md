---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_HEXAGONAL_SCAFFOLDER_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/hexagonal-scaffolder/SKILL.md
---

# Skill — hexagonal-scaffolder

Générer la structure ports/adapters depuis un contrat.

## Objectifs
- Générer `application/ports/in/` et `application/ports/out/`
- Générer `infrastructure/adapters/in/` et `infrastructure/adapters/out/`
- Respecter l’architecture hexagonale

## Entrées
- `skill_path`: chemin de la skill
- `contract_path`: chemin du contrat d’interface

## Sorties
- `list[Path]`: fichiers créés

## Tests
- `tests/test_hexagonal_scaffolder.py`
