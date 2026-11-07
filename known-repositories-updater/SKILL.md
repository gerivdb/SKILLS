---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_KNOWN_REPOSITORIES_UPDATER_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/known-repositories-updater/SKILL.md
---

# Skill — known-repositories-updater

Met à jour known_repositories.yaml proprement.

## Opérations
- Ajouter un repo
- Mettre à jour verse_mapping
- Mettre à jour local_path
- Supprimer un repo (avec archivage)
- Préserver les ancres YAML

## Commandes
- `known-repositories-updater add <repo> <path> <layer>`
- `known-repositories-updater update <repo> --field <value>`
- `known-repositories-updater remove <repo> --archive`
- `known-repositories-updater validate`
