---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xACT_AUTOMODE_SENTINEL_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/act-automode-sentinel/SKILL.md
---

# Skill: act-automode-sentinel

## Purpose
Securiser l execution de act.autoMode pour qu elle ne parte jamais en boucle infinie autonome. Le sentinel surveille l activite du worker ACT (seuil 60s), active un coupe circuit d urgence et verifie l etat idle de la session N.

## Context
act.autoMode peut entrer en boucle infinie si le worker ACT ne repond plus ou si la session reste bloquee. Un watchdog avec coupe circuit est necessaire pour arreter toute ex autonomie desactivee.

## Scope
- Surveillance activite worker ACT (seuil 60s)
- Coupe circuit d urgence en cas de depassement
- Verification etat idle session N
- Rapport de securite (OK / ALERTE / COUPE-CIRCUIT)

## Cibles
- Processus ACT
- Etat idle session N
- WAL

## Script d'investigation
`scripts/automode_watchdog.ps1` - PowerShell, encodage CP1252, pas de caracteres Unicode speciaux.

## WAL NEXUS
| Intervention | Cible | Horodatage | Statut | Preuve |
|---|---|---|---|---|
| Creation skill act-automode-sentinel | skills/act-automode-sentinel/ | 2026-10-25 | CREE | SKILL.md + scripts/automode_watchdog.ps1 |
| Enregistrement REGISTRY.yaml | REGISTRY.yaml | 2026-10-25 | EN_ATTENTE | id=ACT-AUTOMODE-SENTINEL |
| Enregistrement MANIFEST.json | MANIFEST.json | 2026-10-25 | EN_ATTENTE | name=act-automode-sentinel |

