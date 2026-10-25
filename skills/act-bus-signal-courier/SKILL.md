---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xACT_BUS_SIGNAL_COURIER_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/act-bus-signal-courier/SKILL.md
---

# Skill: act-bus-signal-courier

## Purpose
Rendre deterministe et fiable la communication inter-worktrees orchestree par GeriCode. Le skill valide la structure atomique des signaux (eNN-completed.json), assure le pontage avec le bus WAZAA en L4 et propose un fallback WAL 0x243.

## Context
La communication entre worktrees GeriCode repose sur des signaux atomiques deposes sur le bus. Sans validation de structure ni mecanisme de fallback, des signaux peuvent etre perdus ou mal interpretes.

## Scope
- Validation de la structure atomique des signaux (eNN-completed.json)
- Pontage avec le bus WAZAA en L4 (D:\DO\WEB\TOOLS\L4-TOOLS\WAZAA)
- Fallback WAL 0x243 en cas d indisponibilite du bus
- Rapport de livraison (LIVRE / FALLBACK / ECHOUE)

## Cibles
- .kilo/bus/
- D:\DO\WEB\TOOLS\L4-TOOLS\WAZAA
- WAL (0x243)

## Script d'investigation
`scripts/relay_signals.py` - Python, validation signaux, pontage WAZAA, fallback WAL.

## WAL NEXUS
| Intervention | Cible | Horodatage | Statut | Preuve |
|---|---|---|---|---|
| Creation skill act-bus-signal-courier | skills/act-bus-signal-courier/ | 2026-10-25 | CREE | SKILL.md + scripts/relay_signals.py |
| Enregistrement REGISTRY.yaml | REGISTRY.yaml | 2026-10-25 | EN_ATTENTE | id=ACT-BUS-SIGNAL-COURIER |
| Enregistrement MANIFEST.json | MANIFEST.json | 2026-10-25 | EN_ATTENTE | name=act-bus-signal-courier |

