---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_SKILLS_VALIDATOR_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/skills-validator/SKILL.md
---

# Skill - skills-validator

Valider les skills contre la taxonomie SKILLS/TAXONOMY.md.

## Validations
- Frontmatter YAML valide
- Champs obligatoires presents
- Triggers non vides
- Type dans {foundational, domain, external}
- Status dans {active, draft, deprecated}
- Pas de doublons de nom
- Path existe dans le filesystem

## Commandes
- `skills-validator validate --skill <name>`
- `skills-validator validate --all`
- `skills-validator lint --path .kilo/skills/`
