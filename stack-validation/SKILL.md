---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_STACK_VALIDATION_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/stack-validation/SKILL.md
---

# Skill — stack-validation

Valider la chaîne complète TDD → BDD → ATDD → DDD → DbC → Hexagonal pour une skill.

## Objectifs
- Vérifier la présence des tests TDD, BDD, ATDD, DDD, DbC, Hexagonal
- Produire un rapport de conformité par couche

## Entrées
- `skill_path`: chemin de la skill

## Sorties
- `dict`: rapport par couche

## Tests
- `tests/test_stack_validation.py`
