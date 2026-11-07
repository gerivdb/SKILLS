---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_GITIGNORE_HARMONIZER_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/gitignore-harmonizer/SKILL.md
---

# Skill — gitignore-harmonizer

Corriger les `.gitignore` pour supporter Hexagonal/BDD/ATDD.

## Règles
- Remplacer `out/` par `infrastructure/adapters/out/`
- Ajouter `infrastructure/adapters/in/`
- Ajouter `features/steps/`
- Ajouter `acceptance/`
- Préserver les patterns existants

## Commandes
- `gitignore-harmonizer fix --repo <path>`
- `gitignore-harmonizer check --repo <path>`
- `gitignore-harmonizer template --skill <name>`
