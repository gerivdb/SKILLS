---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_REGISTRY_SYNC_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/registry-sync/SKILL.md
---

# Skill — registry-sync

Synchroniser REGISTRY.yaml ↔ registry.json ↔ citizens.yaml.

## Objectifs
- `REGISTRY.yaml` est la source de vérité.
- `registry.json` est régénéré depuis `REGISTRY.yaml`.
- `citizens.yaml` est enrichi depuis `REGISTRY.yaml`.

## Commandes
- `registry-sync sync` — synchronise tous les registres.
- `registry-sync validate` — valide la cohérence.
