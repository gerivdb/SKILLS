---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_SKILL_AUTO_ENROLLER_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/skill-auto-enroller/SKILL.md
---

# Skill - skill-auto-enroller

Enroll automatiquement un skill dans tous les registres.

## Pipeline
1. Verifier le skill dans `.kilo/skills/<repo>/<skill>/`
2. Creer la structure TDD/BDD/ATDD/DDD/DbC/Hexagonal si absente
3. Enregistrer dans REGISTRY.yaml
4. Creer citizen dans citizens.yaml si repo pas encore citizen
5. Creer verse dans VERSES/verses/ si absente
6. Creer bridge dans BRIDGES.yaml si absent
7. Mettre a jour .gitignore si necessaire
8. Valider la coherence (P-801..P-807)
9. Logger dans WAL

## Commandes
- `skill-auto-enroller enroll <skill_name> --repo <repo_name>`
- `skill-auto-enroller audit <skill_name>`
- `skill-auto-enroller rollback <skill_name>`
