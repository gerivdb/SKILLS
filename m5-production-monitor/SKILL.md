---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_M5_PRODUCTION_MONITOR_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/m5-production-monitor/SKILL.md
---

# Skill — m5-production-monitor

Surveiller la production ontologique et conversationnelle.

## Objectifs
- Mesurer le lifecycle des concepts.
- Détecter les anaphores orphelines.
- Mesurer la stabilité sémantique.
- Détecter les quiproquos.

## Entrées
- `conversation_trace_path`: chemin de la trace de conversation.
- `ontology_path`: chemin vers `ONTOLOGY/glossary.yaml`.
- `verses_path`: chemin vers `VERSES/verses/`.

## Sorties
- `dict`: métriques M5.

## Probes
- P-912: M5 production ontologique
- P-913: conversational_birth_detector
- P-914: conversation_semantic_stability
- P-915: quiproquo_lifecycle

## Tests
- `tests/test_m5_production_monitor.py`
