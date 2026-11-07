---
name: meta-trace
description: Skill de traçabilité méta-gouvernance AUTO-DEV. Trace les événements méta vers NEXUS WAL, WAZAA topics, MIMIR log. Utiliser pour meta-trace, traçabilité méta, NEXUS, WAZAA, MIMIR, ACT auto.
version: 1.0.0
author: gerivdb
license: MIT
triggers:
  - meta-trace
  - traçabilité méta
  - NEXUS
  - WAZAA
  - MIMIR
inputs:
  - name: plan
    type: dict
    description: Plan d'action méta-gouvernance
  - name: result
    type: dict
    description: Résultat de l'exécution
outputs:
  - name: trace
    type: dict
    description: Traçabilité NEXUS/WAZAA/MIMIR
tools:
  - nexus-wal-writer
  - wazaa-event-publisher
  - mimir-log-appender
related_skills:
  - meta-governance-auto
  - wal-reconciler
  - prd-moc-proof-updater
---

# Meta-Trace

Skill de traçabilité méta-gouvernance AUTO-DEV.

## Mission

Tracer les événements méta vers NEXUS WAL, WAZAA topics, MIMIR log.

## Destinations

| Destination | Format | Usage |
|-------------|--------|-------|
| NEXUS WAL | YAML cycle event | Shared state |
| WAZAA | JSON event | Event bus |
| MIMIR | Markdown append | Discovery log |
| output/meta/meta_trace.json | JSON | Local trace |

## Intégration AUTO-DEV

- `agents/meta_trace.py`
- `agents/meta_writers.py`

## Références

- `PRD-021-auto-dev-meta-governance-auto.md`
- `MOC-025-auto-dev-meta-governance-auto.md`
- `TALEX/ONTOLOGY_DECLARATION.yaml` (concept: meta-trace)
