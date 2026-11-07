---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_SKILL_TEST_SCAFFOLDER_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/skill-test-scaffolder/SKILL.md
---

# Skill — skill-test-scaffolder

Générer la structure de tests pour une skill.

## Objectifs
- Créer `tests/test_<skill>.py`, `conftest.py`, `features/*.feature`
- Générer les steps BDD
- Respecter les conventions TDD/BDD

## Entrées
- `skill_path`: chemin de la skill

## Sorties
- `list[Path]`: fichiers créés

## Tests
- `tests/test_skill_test_scaffolder.py`
