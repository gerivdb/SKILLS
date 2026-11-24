---
name: aider
description: Assistant de programmation en terminal utilisant des cartes de symboles/graphes pour cibler les bons extraits de code. Pattern inspiré de https://github.com/Aider-AI/aider
version: 1.0.0
intent_hash: 0xSKILL_AIDER_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/Aider-AI/aider
source_url: https://github.com/Aider-AI/aider
path: aider
---

# Aider — Skill KiloCode

## Objectif

Fournir une référence canonique pour Aider, assistant de programmation en terminal utilisant des cartes de symboles/graphes pour cibler les bons extraits de code. Adapté à ENV2 pour l'assistance au codage locale sans serveur externe, avec ciblage précis des extraits de code via graphes de symboles.

## Déclencheur

Ce skill s'active quand :
- Il faut obtenir une assistance de programmation dans un terminal sur ENV2
- Des cartes de symboles/graphes doivent être utilisées pour cibler les extraits de code
- L'assistance doit être locale et souveraine (pas de cloud externe)
- L'environnement ENV2 nécessite un assistant de codage léger

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `repo_path` | string | ✅ | Chemin absolu vers le dépôt cible |
| `symbol_map` | boolean | ❌ | Générer ou utiliser une carte de symboles (défaut: true) |
| `code_query` | string | ✅ | Requête de code ou instruction d'assistance |
| `target_files` | array | ❌ | Fichiers cibles pour l'assistance |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `code_suggestions` | array | Suggestions de code générées |
| `symbol_map_used` | boolean | True si une carte de symboles a été utilisée |
| `files_modified` | array | Fichiers modifiés par l'assistance |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin repo

```
→ Confirmer que repo_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du dépôt sur ENV2
```

### Étape 2 — Assistance de codage

```
→ Générer ou charger la carte de symboles du dépôt
→ Cibler les extraits de code pertinents via le graphe de symboles
→ Exécuter l'assistance demandée (code_query sur target_files)
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier l'intégrité des fichiers modifiés
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser un assistant de codage cloud externe au lieu de Aider local sur ENV2
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Modifier des fichiers sans vérification de la carte de symboles

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
