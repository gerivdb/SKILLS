---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_BRIDGE_AUDITOR_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/bridge-auditor/SKILL.md
---

# Skill — bridge-auditor

Valider BRIDGES.yaml et détecter les orphelins.

## Validations
- Tous les bridges référencent des repos existants dans known_repositories.yaml
- Tous les repos actifs ont un bridge
- Pas de cycles dans les bridges
- Pas de bridges orphelins

## Commandes
- `bridge-auditor audit`
- `bridge-auditor orphans`
- `bridge-auditor cycles`
- `bridge-auditor repair`
