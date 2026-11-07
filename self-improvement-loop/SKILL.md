---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_SELF_IMPROVEMENT_LOOP_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/self-improvement-loop/SKILL.md
---

# Skill — self-improvement-loop

Exécuter la boucle evaluate → propose → changelog.

## Objectifs
- Scanner `scaffold/self_improvement/evaluators/`
- Exécuter les évaluateurs
- Collecter les scores
- Invoquer les mutators
- Écrire le changelog

## Entrées
- `scaffold_path`: chemin de `scaffold/`

## Sorties
- `dict`: rapport de mutation

## Tests
- `tests/test_self_improvement_loop.py`
