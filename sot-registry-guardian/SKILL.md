---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_SOT_REGISTRY_GUARDIAN_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/sot-registry-guardian/SKILL.md
---

# Skill - sot-registry-guardian

Proteger `known_repositories.yaml` contre les modifications non validees.

## Objectifs
- Bloquer les writes directs non autorises.
- Forcer l'usage du mapping local ou du skill `yaml-safe-injector`.
- Logger toute tentative de modification dans WAL.

## Entrees
- `target_path`: chemin du fichier SOT.
- `action`: `read` | `validate` | `block_write`.

## Sorties
- `bool`: autorise ou bloque.

## Regles
- `validate` parse le YAML et verifie le schema minimal.
- `block_write` refuse toute ecriture non issue de `yaml-safe-injector`.
- Toute tentative suspecte est loguee dans WAL.

## Tests
- `tests/test_sot_registry_guardian.py`

## Probes
- P-801: tous les repos actifs sont des citoyens declares
- P-802: tous les citoyens ont un verse dans VERSES/verses/
- P-806: tout skill .kilo/skills/<repo>/ est declare dans REGISTRY.yaml
- P-807: REGISTRY.yaml contient source_repo pour chaque skill
