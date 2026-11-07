---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_YAML_SAFE_INJECTOR_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/yaml-safe-injector/SKILL.md
---

# Skill — yaml-safe-injector

Injecter des champs dans un YAML complexe sans corrompre la structure, avec validation et rollback.

## Objectifs
- Préserver quoted strings multiline, ancres YAML, commentaires, ordre des clés.
- Produire un diff minimal et valide.
- Fournir un mode dry-run et un rollback automatique.

## Entrées
- `target_path`: chemin du fichier YAML cible.
- `updates`: dict des champs à injecter/mettre à jour.
- `dry_run`: booléen, ne pas écrire le fichier.

## Sorties
- `(Path, str)`: chemin cible et diff unifié.

## Règles
- Toute écriture passe par `_apply_update()`.
- Toujours valider avec `yaml.safe_load` avant et après écriture.
- Logger chaque injection dans WAL.
- En cas d’échec de validation post-écriture, rollback immédiat.

## Tests
- `tests/test_yaml_safe_injector.py`: 100% passants requis.

## Probes
- P-301: 100% tests passants
- P-302: 0 corruption sur jeu de tests représentatif
- P-303: dry-run ne modifie pas le fichier
- P-304: rollback en < 30s
