---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_SWV_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/skill-synapse-weaver/SKILL.md
---

# Skill — skill-synapse-weaver

## Objectif

Tisseur topologique : analyse les entrées/sorties de tous les skills existants pour déduire automatiquement les Combos possibles et détecter les impasses. Construit la carte synaptique globale de l'écosystème L4-TOOLS. Couche Méta-Skills & Cycle de Vie.

## Déclencheur

- Avant la création d'un nouveau Combo
- Lors d'un audit de topologie des skills
- Pour détecter les impasses dans les pipelines de skills

## Entrées

- `skills_repo`: chemin vers le dépôt SKILLS (défaut : `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS`)
- `output_path`: chemin du fichier de sortie de la carte synaptique (optionnel)

## Sorties

- Carte synaptique JSON (entrées/sorties de chaque skill)
- Liste des Combos déductibles (chaînes de compétences compatibles)
- Liste des impasses (skills sans sortie compatible avec un autre skill)
- Entrée WAL NEXUS horodatée

## Règles

### 1. Analyse des entrées/sorties

Chaque skill doit déclarer ses entrées et ses sorties dans son SKILL.md. Le tisseur extrait ces métadonnées pour construire le graphe.

### 2. Déduction des Combos

Un Combo est déductible si la sortie d'un skill A correspond à l'entrée d'un skill B (même type de données).

### 3. Détection des impasses

Un skill est en impasse si :
- Il n'a pas de sortie compatible avec l'entrée d'un autre skill
- Il n'a pas d'entrée compatible avec la sortie d'un autre skill (sauf s'il est un skill d'entrée)

## Script d'investigation

`scripts/weave.ps1` — voir ci-dessous.

## Tests

- `tests/test_skill_synapse_weaver.ps1` — créer des skills avec entrées/sorties déclarées, vérifier la déduction des Combos et des impasses.

## Probes

- Chaque skill a au moins une entrée ou une sortie déclarée
- Zéro impasse non documentée dans l'écosystème

## WAL NEXUS

```
[WAL_NEXUS] skill=skill-synapse-weaver action=weave timestamp=<ISO> skills_analyzed=<n> combos_deduced=<m> deadends=<k>
```

## Référence ADR

- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
- **IntentHash** : 0xB05F1124CDC61605
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
