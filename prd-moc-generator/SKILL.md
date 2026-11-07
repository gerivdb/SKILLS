---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_PRD_MOC_GENERATOR_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/prd-moc-generator/SKILL.md
---

# Skill — prd-moc-generator

Générer un PRD MOC depuis un plan repo.

## Objectifs
- Lire `act-protocol/PRD/<repo>/`
- Extraire les métadonnées
- Générer le fichier PRD MOC avec frontmatter + sections

## Entrées
- `repo_name`: nom du repo
- `plans_path`: chemin vers les plans

## Sorties
- `Path`: fichier PRD MOC généré

## Tests
- `tests/test_prd_moc_generator.py`
