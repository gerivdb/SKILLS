---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_REPO_CITIZEN_MANAGER_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/repo-citizen-manager/SKILL.md
---

# Skill — repo-citizen-manager

Gérer la citoyennisation des repos de l'écosystème gerivdb.

## Objectifs
- Vérifier qu'un repo existe dans `known_repositories.yaml`.
- Créer/maintenir le verse dans `VERSES/verses/<repo>-verse.md`.
- Déclarer le citizen dans `citizens.yaml`.
- Créer le bridge dans `TOPOS/BRIDGES.yaml`.
- Mettre à jour `ONTOLOGY/glossary.yaml` si nouveau concept.
- Logger dans WAL.

## Entrées
- `repo_name`: nom du repo.
- `full_name`: nom complet `gerivdb/<REPO>`.
- `layer`: strate L0-L5.

## Sorties
- `dict`: résultat de la citoyennisation.

## Règles
- Un repo citoyen DOIT avoir un verse dans VERSES.
- Un repo citoyen DOIT être déclaré dans `citizens.yaml`.
- Un repo citoyen DOIT avoir un bridge dans `TOPOS/BRIDGES.yaml`.
- Toute création/modification est loggée dans WAL.

## Tests
- `tests/test_repo_citizen_manager.py`: 100% passants requis.

## Probes
- P-801: tous les repos actifs sont des citoyens déclarés
- P-802: tous les citoyens ont un verse dans VERSES
- P-806: tout skill est déclaré dans REGISTRY.yaml
