---
name: tree-sitter
description: Parseur incrémental de référence pour extraire des nœuds syntaxiques précis et faire du slicing de fichiers/code. Pattern inspiré de https://github.com/tree-sitter/tree-sitter
version: 1.0.0
intent_hash: 0xSKILL_TREE_SITTER_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/tree-sitter/tree-sitter
source_url: https://github.com/tree-sitter/tree-sitter
path: tree-sitter
---

# Tree-sitter — Skill KiloCode

## Objectif

Fournir une référence canonique pour Tree-sitter, parseur incrémental de référence pour extraire des nœuds syntaxiques précis et faire du slicing de fichiers/code. Adapté à ENV2 pour le découpage syntaxique fin (AST) sans charger les fichiers entiers, en lien avec le file slicing et le database slicing.

## Déclencheur

Ce skill s'active quand :
- Il faut extraire des nœuds syntaxiques précis depuis un fichier source
- Un slicing de code est nécessaire pour isoler les segments utiles sans chargement complet
- Un parseur incrémental est requis pour maintenir un AST à jour après modifications
- Le slicing syntaxique doit alimenter une couche neurosymbolique sur ENV2

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `file_path` | string | ✅ | Chemin absolu vers le fichier source à parser |
| `language` | string | ✅ | Langage de programmation (ex: python, zig, javascript) |
| `query` | string | ❌ | Requête Tree-sitter pour extraire des nœuds spécifiques |
| `slice_node_type` | string | ❌ | Type de nœud à isoler (ex: function_definition, class_definition) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `ast_nodes` | array | Nœuds AST extraits selon la requête |
| `sliced_segments` | array | Segments de code isolés (slicing) |
| `node_positions` | array | Positions (ligne/colonne) des nœuds dans le fichier |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin fichier

```
→ Confirmer que file_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier sur ENV2
```

### Étape 2 — Parsing et slicing

```
→ Charger le parseur Tree-sitter pour le langage spécifié
→ Parser le fichier de manière incrémentale
→ Extraire les nœuds selon la requête ou le type de nœud cible
→ Isoler les segments de code pertinents (slicing)
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune modification n'a été apportée au fichier source
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Charger le fichier entier en mémoire au lieu d'extraire seulement les nœuds pertinents
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Modifier le fichier source pendant le parsing
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
