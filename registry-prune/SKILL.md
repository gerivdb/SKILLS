---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_REGISTRY_PRUNE_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/registry-prune/SKILL.md
---

# Skill — registry-prune

Nettoyer les entrées orphelines dans tous les registres.

## Opérations
- Supprimer les skills dont le `path` n'existe plus
- Supprimer les citizens dont le repo n'existe plus
- Supprimer les bridges dont le repo n'existe plus
- Supprimer les verses dont le `source_repo` n'existe plus

## Commandes
- `registry-prune audit`
- `registry-prune dry-run`
- `registry-prune prune`
