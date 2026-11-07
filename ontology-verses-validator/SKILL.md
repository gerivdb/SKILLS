---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_ONTOLOGY_VERSES_VALIDATOR_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/ontology-verses-validator/SKILL.md
---

# Skill — ontology-verses-validator

Valider la cohérence ONTOLOGY ↔ VERSES ↔ TQL ↔ SPIDX.

## Objectifs
- Vérifier que tout concept dans `ONTOLOGY/ONTOLOGY.yaml` a un verse
- Vérifier que tout verse est référencé dans un bridge
- Vérifier que TQL peut requêter chaque concept

## Entrées
- `ontology_path`: chemin vers `ONTOLOGY/ONTOLOGY.yaml`
- `verses_path`: chemin vers `VERSES/verses/`

## Sorties
- `dict`: rapport de validation

## Tests
- `tests/test_ontology_verses_validator.py`
