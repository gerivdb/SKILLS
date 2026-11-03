---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_CONTEXT_ENGINEERING_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/context-engineering/SKILL.md
---

# Skill - context-engineering

Gerer le contexte partage des agents.

## Objectifs
- Injecter du contexte dans `agent/memory/`
- Extraire le contexte pour un tour de conversation
- Mesurer la taille et la pertinence du contexte

## Entrees
- `context_path`: chemin vers le contexte
- `turn_id`: identifiant du tour

## Sorties
- `dict`: contexte injecte

## Tests
- `tests/test_context_engineering.py`
