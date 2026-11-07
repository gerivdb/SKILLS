---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-08"
intent_hash: 0xSKILL_WAL_AUTO_LOGGER_20260808
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/wal-auto-logger/SKILL.md
---

# Skill — wal-auto-logger

Logger automatiquement les modifications dans WAL.

## Objectifs
- Fournir un décorateur/context manager pour logging automatique
- Écrire dans `.kilo/wal/`
- Journaliser les modifications de fichiers

## Entrées
- `wal_path`: chemin vers `.kilo/wal/`
- `event_type`: type d’événement

## Sorties
- `Path`: chemin du fichier WAL écrit

## Tests
- `tests/test_wal_auto_logger.py`
