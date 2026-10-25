---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xGERICODE_BEADS_INTEGRITY_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/gericode-beads-integrity/SKILL.md
---

# Skill: gericode-beads-integrity

## Purpose
Prevenir la corruption ou le verrouillage de la base de graphes de connaissances (2.1 Mo). Le skill verifie l integrite du fichier beads.json, detecte les verrous Windows et cree un backup tournant.

## Context
La base beads.json est un graphe de connaissances critique pour GeriCode ACT. Un verrou Windows ou une corruption JSON peut bloquer l'ensemble du pipeline ACT.

## Scope
- Verification de la structure JSON de beads.json
- Detection des verrous Windows sur le fichier
- Creation d'un backup tournant (rotation conservee)
- Rapport d integrite (OK / CORROMPU / VERROUILLE)

## Cibles
- L2-PLATFORM/GeriCode/beads.json

## Script d'investigation
`scripts/verify_beads.py` - Python, verifie JSON, detecte locks Windows, backup tournant.

## WAL NEXUS
| Intervention | Cible | Horodatage | Statut | Preuve |
|---|---|---|---|---|
| Creation skill gericode-beads-integrity | skills/gericode-beads-integrity/ | 2026-10-25 | CREE | SKILL.md + scripts/verify_beads.py |
| Enregistrement REGISTRY.yaml | REGISTRY.yaml | 2026-10-25 | EN_ATTENTE | id=GERICODE-BEADS-INTEGRITY |
| Enregistrement MANIFEST.json | MANIFEST.json | 2026-10-25 | EN_ATTENTE | name=gericode-beads-integrity |

