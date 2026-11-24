---
name: awesome-omni-skill
description: Modèles de conception de workflows d'agents, gestion d'état et découpage de tâches. Pattern inspiré de https://github.com/diegosouzapw/awesome-omni-skill
version: 1.0.0
intent_hash: 0xSKILL_AWESOME_OMNI_SKILL_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/diegosouzapw/awesome-omni-skill
source_url: https://github.com/diegosouzapw/awesome-omni-skill
path: awesome-omni-skill
---

# Awesome Omni Skill — Skill KiloCode

## Objectif

Fournir des modèles de conception de workflows d'agents, de gestion d'état et de découpage de tâches. Ce skill encapsule le pattern du repo externe `awesome-omni-skill` adapté à ENV2, avec respect des règles de gouvernance des skills et de fragmentation SLM.

## Déclencheur

Ce skill s'active quand :
- Un workflow d'agent doit être conçu selon un pattern de référence
- La gestion d'état d'un agent doit être formalisée
- Une tâche complexe doit être découpée en sous-tâches atomiques
- Un modèle de skill doit être sélectionné pour un cas d'usage donné

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `task_complexity` | enum | ✅ | simple / medium / complex |
| `domain` | string | ✅ | Domaine de la tâche (ex: git, cdp, memory, mcp, governance) |
| `state_management` | enum | ❌ | none / local / distributed / wal |
| `decomposition_level` | integer | ❌ | Niveau de découpage (1 = tâche unique, N = sous-tâches atomiques) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `workflow_pattern` | string | Pattern de conception recommandé |
| `task_decomposition` | array | Découpage de la tâche en sous-tâches atomiques |
| `skill_recommendations` | array | Skills recommandés pour chaque sous-tâche |
| `state_schema` | object | Schéma de gestion d'état recommandé |
| `evidence_hash` | string | Hash SHA-256 de l'analyse |

## Protocole Obligatoire

### Étape 1 — Évaluation de la complexité

```
→ Analyser la tâche pour déterminer sa complexité (simple / medium / complex)
→ Identifier le domaine de la tâche
→ Déterminer le niveau de découpage nécessaire
```

### Étape 2 — Sélection du pattern de workflow

```
→ simple → pattern linéaire (compétence unique)
→ medium → pattern séquentiel (chaîne de compétences)
→ complex → pattern arborescent (branches conditionnelles, parallélisation)
```

### Étape 3 — Découpage de tâches

```
→ Décomposer la tâche en sous-tâches atomiques (1 action = 1 outil)
→ Pour chaque sous-tâche, identifier le skill correspondant dans skills-index.json
→ Si aucun skill ne correspond → créer un skill draft (règle skill-citizen-prealable)
→ Ordonner les sous-tâches par dépendance
```

### Étape 4 — Gestion d'état

```
→ Définir le schéma de gestion d'état (local, distributed, WAL)
→ Pour chaque sous-tâche, enregistrer l'état dans le WAL (WAL-0x243)
→ Vérifier la réversibilité de chaque état (règle m3tree)
```

## Anti-patterns

- ❌ Découper une tâche sans vérifier qu'un skill existe pour chaque sous-tâche
- ❌ Utiliser un pattern de workflow trop complexe pour une tâche simple
- ❌ Oublier la gestion d'état (pas de trace dans le WAL)
- ❌ Ne pas respecter la fragmentation SLM (une action = un outil = un résultat vérifiable)

## Référence ADR

- **ADR** : ADR-PRIM-001-MASSIVE-DECOMPOSITION
- **IntentHash** : 0x77B660FF9E015192
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : slm-fragmented-approach
- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : m3tree
