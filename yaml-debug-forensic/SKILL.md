---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_YAML_DEBUG_FORENSIC_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/yaml-debug-forensic/SKILL.md
---

# Skill — yaml-debug-forensic

Diagnostiquer les erreurs YAML courantes sans modifier le fichier.

## Objectifs
- Détecter clés dupliquées, quoted strings cassées, ancres invalides.
- Générer un rapport de corruption immuable.

## Entrées
- `target_path`: chemin du fichier YAML.

## Sorties
- `dict`: rapport de diagnostic.

## Règles
- Ne jamais modifier le fichier cible.
- Toujours écrire le rapport dans `.kilo/wal/`.

## Tests
- `tests/test_yaml_debug_forensic.py`

## Probes
- Aucune corruption de `known_repositories.yaml` pendant 30 jours
