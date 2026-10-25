---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xGERICODE_ACT_PREFLIGHT_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/gericode-act-preflight/SKILL.md
---

# Skill: gericode-act-preflight

## Purpose
Verifier que l'environnement ENV2 est apte a reactiver l'extension gerivdb.act-vscode-0.2.0 sans provoquer de conflit. Le preflight valide la presence du binaire VSIX, la cle GPG locale et l'etat des caches L1/L2 avant toute installation.

## Context
L'extension ACT (act-vscode-0.2.0) est distribuee sous forme de VSIX signe GPG. Une reactivation sans verification peut entrainer des conflits de signature, des caches corrompus ou une installation partielle.

## Scope
- Verification du binaire VSIX : L2-PLATFORM/GeriCode/act-vscode-0.2.0.vsix
- Verification de la cle GPG locale pour verification de signature
- Purge des caches L1 et L2 lies a ACT
- Rapport de preflight (OK / BLOQUE)

## Cibles
- L2-PLATFORM/GeriCode/act-vscode-0.2.0.vsix
- Cle GPG locale (gpg.exe)
- Caches L1/L2 (D:\DO\WEB\TOOLS\L1-*, L2-PLATFORM/*)

## Script d'investigation
`scripts/act_preflight.ps1` - PowerShell, encodage CP1252, pas de caracteres Unicode speciaux.

## WAL NEXUS
| Intervention | Cible | Horodatage | Statut | Preuve |
|---|---|---|---|---|
| Creation skill gericode-act-preflight | skills/gericode-act-preflight/ | 2026-10-25 | CREE | SKILL.md + scripts/act_preflight.ps1 |
| Enregistrement REGISTRY.yaml | REGISTRY.yaml | 2026-10-25 | EN_ATTENTE | id=GERICODE-ACT-PREFLIGHT |
| Enregistrement MANIFEST.json | MANIFEST.json | 2026-10-25 | EN_ATTENTE | name=gericode-act-preflight |

