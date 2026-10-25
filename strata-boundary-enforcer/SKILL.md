---
type: SKILL
name: strata-boundary-enforcer
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_STRATA_BOUNDARY_ENFORCER_20261025
citizen: L4-TOOLS
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/strata-boundary-enforcer/SKILL.md
---

# Skill — strata-boundary-enforcer

## Objectif
Interdit formellement à un skill L4 de modifier un fichier L0 sans mandat explicite d'un Citoyen habilité. Garantit l'intégrité du socle inviolable (L0-CANON) en appliquant les limites de strate de l'écosystème gerivdb.

## Declencheur
- Un skill L4 tente d'écrire dans un fichier sous D:\DO\WEB\TOOLS\L0-CANON\
- Une modification de fichier L0 est demandée sans mandat Citoyen
- Une tentative de contournement des limites de strate est détectée
- Un audit de conformité des strates est requis

## Entrees
- `skill_id`: identifiant du skill demandeur (doit être L4)
- `target_path`: chemin du fichier cible
- `target_stratum`: strate du fichier cible (L0, L1, L2, etc.)
- `citizen_mandate`: mandat explicite du Citoyen habilité (optionnel, requis pour L0)
- `operation`: type d'opération (read, write, delete, modify)

## Sorties
- `authorized`: boolean indiquant si l'opération est autorisée
- `reason`: motif de l'autorisation ou du refus
- `mandate_required`: boolean indiquant si un mandat Citoyen est requis
- `audit_entry`: entrée d'audit pour le WAL

## Regles d'application
1. L4 -> L0 : INTERDIT sans mandat explicite d'un Citoyen habilité
2. L4 -> L1/L2/L3 : AUTORISÉ avec notification
3. L4 -> L4 : AUTORISÉ (même strate)
4. L4 -> L5/L6 : AUTORISÉ avec notification

## WAL NEXUS
Chaque tentative d'accès inter-strate est consignée dans le WAL avec l'identifiant du skill, le chemin cible, la strate, la décision (autorisé/refusé) et l'horodatage UTC.

## Reference ADR
- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **IntentHash** : 0xSKILL_STRATA_BOUNDARY_ENFORCER_20261025
- **Depot** : gerivdb/SKILLS
- **Statut ADR** : proposed

## Script cible
scripts/enforce.ps1
