---
name: comfyui-mcp
description: Transforme des graphes/pipelines d'exécution en actions appelables. Pattern inspiré de https://github.com/artokun/comfyui-mcp
version: 1.0.0
intent_hash: 0xSKILL_COMFYUI_MCP_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/artokun/comfyui-mcp
source_url: https://github.com/artokun/comfyui-mcp
path: comfyui-mcp
---

# ComfyUI MCP — Skill KiloCode

## Objectif

Transformer des graphes et pipelines d'exécution en actions MCP appelables. Ce skill encapsule le pattern du repo externe `comfyui-mcp` adapté à ENV2, avec respect des règles de chemins explicites, de preuve fraîche et de décomposition atomique.

## Déclencheur

Ce skill s'active quand :
- Un graphe ou pipeline d'exécution doit être transformé en actions MCP appelables
- Un workflow visuel doit être encapsulé en outils invoquables
- Une exécution par graphe doit être décomposée en étapes atomiques
- Un pipeline doit être exposé via MCP local

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `graph_definition` | object | ✅ | Définition du graphe ou pipeline (nœuds, arêtes) |
| `entry_nodes` | array | ✅ | Nœuds d'entrée du graphe |
| `exit_nodes` | array | ✅ | Nœuds de sortie du graphe |
| `atomic_steps` | boolean | ❌ | Décomposer en étapes atomiques (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `mcp_actions` | array | Liste des actions MCP générées depuis le graphe |
| `action_paths` | array | Chemins absolus vers les définitions d'actions |
| `execution_trace` | array | Trace d'exécution du graphe transformé |
| `evidence_hash` | string | Hash SHA-256 des actions générées |

## Protocole Obligatoire

### Étape 1 — Analyse du graphe

```
→ Lire la définition du graphe (nœuds, arêtes, connexions)
→ Identifier les nœuds d'entrée et de sortie
→ Vérifier l'absence de cycle (règle no-cycle-m3-tree)
→ Déterminer l'ordre d'exécution (topologique)
```

### Étape 2 — Transformation en actions MCP

```
→ Pour chaque nœud, générer une action MCP appelable
→ Décomposer les nœuds complexes en étapes atomiques (règle slm-fragmented-approach)
→ Créer le répertoire de chaque action sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\comfyui-mcp\actions\
→ Générer le SKILL.md pour chaque action avec frontmatter et protocole
```

### Étape 3 — Décomposition atomique

```
→ Chaque action MCP doit être atomique (1 action = 1 outil = 1 résultat vérifiable)
→ Vérifier que chaque action a une preuve brute correspondante
→ Documenter les dépendances entre actions
→ Valider que l'ordre d'exécution respecte le graphe d'origine
```

### Étape 4 — Exposition et preuve

```
→ Exposer les actions MCP via le serveur MCP local
→ Tester l'exécution du graphe transformé (chaîne d'actions)
→ Capturer la preuve brute de chaque action (stdout, code de retour, hash SHA-256, timestamp UTC)
→ Enregistrer dans le WAL (WAL-0x243)
→ Mettre à jour skills-index.json
```

## Anti-patterns

- ❌ Transformer un graphe sans vérifier l'absence de cycle (règle no-cycle-m3-tree)
- ❌ Générer des actions MCP non atomiques (viole slm-fragmented-approach)
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
- **Règle** : no-cycle-m3-tree
