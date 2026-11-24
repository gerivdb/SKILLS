---
name: minimax-mcp
description: Exemple d'encapsulation d'actions/API en outils invoquables de manière standardisée. Pattern inspiré de https://github.com/MiniMax-AI/MiniMax-MCP
version: 1.0.0
intent_hash: 0xSKILL_MINIMAX_MCP_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/MiniMax-AI/MiniMax-MCP
source_url: https://github.com/MiniMax-AI/MiniMax-MCP
path: minimax-mcp
---

# MiniMax MCP — Skill KiloCode

## Objectif

Encapsuler des actions/API en outils invoquables de manière standardisée. Ce skill encapsule le pattern du repo externe `MiniMax-MCP` adapté à ENV2, avec respect des règles de chemins explicites et de preuve fraîche.

## Déclencheur

Ce skill s'active quand :
- Une action ou un appel API doit être encapsulé en outil MCP standardisé
- Une action répétitive doit être figée en outil réutilisable
- Une interface d'outils doit être générée pour un ensemble d'actions liées
- La standardisation des outils MCP doit être imposée

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `action_definition` | string | ✅ | Définition de l'action à encapsuler |
| `api_endpoint` | string | ❌ | Endpoint API cible (si applicable, doit respecter BDCP) |
| `tool_name` | string | ✅ | Nom de l'outil encapsulé |
| `input_parameters` | object | ✅ | Paramètres d'entrée de l'outil |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `encapsulated_tool` | string | Nom de l'outil encapsulé |
| `tool_path` | string | Chemin absolu vers la définition de l'outil |
| `standardization_level` | enum | basic / strict / canonical |
| `invocation_proof` | object | Preuve d'invocation (hash, timestamp, code de retour) |
| `evidence_hash` | string | Hash SHA-256 de l'outil encapsulé |

## Protocole Obligatoire

### Étape 1 — Définition de l'action

```
→ Déclarer l'action ou l'appel API à encapsuler
→ Définir les paramètres d'entrée avec types et contraintes
→ Définir le résultat attendu et les codes de retour
→ Si un endpoint API est ciblé, vérifier qu'il respecte BDCP (pas de réseau direct)
```

### Étape 2 — Encapsulation standardisée

```
→ Créer le répertoire de l'outil sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\minimax-mcp\tools\
→ Générer la définition de l'outil (input, output, handler, schema)
→ Lier l'outil à un skill existant dans skills-index.json (si applicable)
→ Vérifier que tous les chemins sont absolus et explicites
```

### Étape 3 — Standardisation

```
→ Appliquer le niveau de standardisation choisi (basic / strict / canonical)
→ Pour canonical → exiger SKILL.md + preuve d'exécution + hash SHA-256
→ Documenter les anti-patterns bloquants
→ Valider que l'outil est invoquable de manière déterministe
```

### Étape 4 — Invocation et preuve

```
→ Tester l'invocation de l'outil avec des paramètres de test
→ Capturer la preuve brute (stdout, code de retour, hash SHA-256, timestamp UTC)
→ Enregistrer dans le WAL (WAL-0x243)
→ Mettre à jour skills-index.json
```

## Anti-patterns

- ❌ Encapsuler une action sans définition claire des paramètres d'entrée
- ❌ Utiliser des chemins relatifs dans la définition de l'outil (règle explicit-path-compliance)
- ❌ Invoquer un outil sans capturer la preuve brute
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : mcp-write-guard
