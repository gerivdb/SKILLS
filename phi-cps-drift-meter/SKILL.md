---
type: SKILL
name: phi-cps-drift-meter
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_PHI_CPS_DRIFT_METER_20261025
citizen: L4-TOOLS
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/phi-cps-drift-meter/SKILL.md
---

# Skill — phi-cps-drift-meter

## Objectif
Mesure la friction (F) et l'entropie (H) lors de l'exécution d'un Combo. Fournit des métriques de drift (écart de comportement) pour détecter l'instabilité des exécutions et déclencher des actions de recalibrage.

## Declencheur
- Un Combo est exécuté et doit être surveillé
- Une dérive de comportement est suspectée (drift)
- Le f-CPS scoring nécessite une mesure d'entropie
- Une analyse de friction est requise avant promotion d'un skill

## Entrees
- `combo_id`: identifiant du Combo à mesurer
- `execution_trace`: trace d'exécution du Combo (étapes, durées, résultats)
- `baseline_metrics`: métriques de référence pour comparaison
- `expected_entropy`: entropie attendue (optionnel)

## Sorties
- `friction_score`: valeur F (friction) entre 0 et 1
- `entropy_value`: valeur H (entropie) en bits
- `drift_detected`: boolean indiquant un écart significatif
- `drift_magnitude`: amplitude du drift détecté

## Metriques
- **Friction (F)** : mesure de la résistance rencontrée lors de l'exécution (retards, tentatives répétées, blocages)
- **Entropie (H)** : mesure du désordre ou de l'imprévisibilité dans l'exécution du Combo
- **Drift** : écart entre l'exécution observée et le comportement de référence

## WAL NEXUS
Chaque mesure de drift et d'entropie est consignée dans le WAL avec l'identifiant du Combo, les valeurs F et H, et l'horodatage UTC. Permet le suivi temporel de la dérive des exécutions.

## Reference ADR
- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **IntentHash** : 0xSKILL_PHI_CPS_DRIFT_METER_20261025
- **Depot** : gerivdb/SKILLS
- **Statut ADR** : proposed

## Script cible
scripts/meter.ps1
