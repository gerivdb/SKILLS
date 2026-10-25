---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xGERICODE_KILO_BOUNDARY_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/gericode-kilo-boundary-arbiter/SKILL.md
---

# Skill: gericode-kilo-boundary-arbiter

## Purpose
Garantir l etancheite stricte entre Kilo Code et GeriCode ACT. L arbitre definit les territoires Kilo (chat, prompts, agent-manager.json) et les territoires GeriCode (surveillance autonome, signature GPG, bus .kilo/bus/).

## Context
Kilo Code et GeriCode ACT partagent le meme environnement ENV2. Sans delimitation claire, des conflits peuvent apparaitre sur les fichiers de configuration, les hooks partagés et le bus de communication.

## Scope
- Territoire Kilo : chat, prompts, agent-manager.json
- Territoire GeriCode : surveillance autonome, signature GPG, bus .kilo/bus/
- Verification des frontieres entre les deux domaines
- Rapport d arbitrage (OK / VIOLATION / INDEFINI)

## Cibles
- .kilo/bus/
- agent-manager.json
- Hooks partagés

## Script d'investigation
`scripts/arbitrate_coexistence.ps1` - PowerShell, encodage CP1252, pas de caracteres Unicode speciaux.

## WAL NEXUS
| Intervention | Cible | Horodatage | Statut | Preuve |
|---|---|---|---|---|
| Creation skill gericode-kilo-boundary-arbiter | skills/gericode-kilo-boundary-arbiter/ | 2026-10-25 | CREE | SKILL.md + scripts/arbitrate_coexistence.ps1 |
| Enregistrement REGISTRY.yaml | REGISTRY.yaml | 2026-10-25 | EN_ATTENTE | id=GERICODE-KILO-BOUNDARY |
| Enregistrement MANIFEST.json | MANIFEST.json | 2026-10-25 | EN_ATTENTE | name=gericode-kilo-boundary-arbiter |

