---
type: SKILL
name: wal-event-notary
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_WAL_EVENT_NOTARY_20261025
citizen: L4-TOOLS
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/wal-event-notary/SKILL.md
---

# Skill — wal-event-notary

## Objectif
Notarise chaque transition d'état d'un Citizen, d'un Méta-Skill ou d'un Combo dans le journal d'audit append-only (WAL/0x243.log). Garantit l'immuabilité et la traçabilité complète des changements d'état dans l'écosystème gerivdb.

## Declencheur
- Une transition d'état est détectée sur un Citizen (ex: hot -> warm -> cold)
- Un Méta-Skill change de version ou de statut
- Un Combo exécute une transition de phase
- Une écriture WAL doit être notarisée avec horodatage UTC

## Entrees
- `citizen_id`: identifiant du Citizen, Méta-Skill ou Combo concerné
- `from_state`: état précédent
- `to_state`: état cible
- `combo_id`: identifiant du Combo (optionnel, si applicable)
- `timestamp_utc`: horodatage UTC de la transition

## Sorties
- `wal_entry_id`: identifiant unique de l'entrée WAL
- `wal_path`: chemin vers le fichier WAL/0x243.log
- `confirmed`: boolean indiquant que l'entrée a été appendée

## Protocole de notarisation
1. Recevoir les paramètres de transition d'état
2. Générer un identifiant d'entrée WAL (hash SHA-256 du contenu)
3. Écrire l'entrée au format `timestamp|citizen_id|from_state|to_state|combo_id|entry_id` dans WAL/0x243.log
4. Retourner wal_entry_id et confirmed

## WAL NEXUS
Chaque entrée est appendée dans `WAL/0x243.log` avec horodatage UTC au format ISO-8601. Le journal est append-only : aucune modification ni suppression n'est autorisée après écriture.

## Reference ADR
- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **IntentHash** : 0xSKILL_WAL_EVENT_NOTARY_20261025
- **Depot** : gerivdb/SKILLS
- **Statut ADR** : proposed

## Script cible
scripts/notarize.ps1
