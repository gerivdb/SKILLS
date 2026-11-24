---
name: mcp-server-modular
description: Expose des fonctions, workflows et ressources sous forme d'outils standards. Pattern inspiré de https://github.com/converged-computing/mcp-server
version: 1.0.0
intent_hash: 0xSKILL_MCP_SERVER_MODULAR_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/converged-computing/mcp-server
source_url: https://github.com/converged-computing/mcp-server
path: mcp-server-modular
---

# MCP Server Modular — Skill KiloCode

## Objectif

Exposer des fonctions, workflows et ressources sous forme d'outils MCP standards, invoquables de manière déterministe. Ce skill encapsule le pattern du repo externe `mcp-server` adapté à ENV2, avec respect des règles BDCP et de chemins explicites.

## Déclencheur

Ce skill s'active quand :
- Une fonction ou un workflow doit être exposé comme outil MCP invoquable
- Une ressource doit être exposée via MCP local
- Un skill doit être encapsulé dans une interface MCP standardisée
- La taille de payload MCP doit être gérée avec stratégie de retry

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `function_definition` | string | ✅ | Définition de la fonction à exposer |
| `tool_name` | string | ✅ | Nom de l'outil MCP |
| `input_schema` | object | ✅ | Schéma d'entrée de l'outil |
| `output_schema` | object | ✅ | Schéma de sortie de l'outil |
| `mcp_endpoint` | string | ❌ | Endpoint MCP local (défaut: serveur MCP configuré) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `mcp_tool_name` | string | Nom de l'outil MCP exposé |
| `tool_path` | string | Chemin absolu vers la définition de l'outil |
| `input_schema_validated` | bool | True si le schéma d'entrée est valide |
| `output_schema_validated` | bool | True si le schéma de sortie est valide |
| `evidence_hash` | string | Hash SHA-256 de la définition de l'outil |

## Protocole Obligatoire

### Étape 1 — Définition de la fonction

```
→ Déclarer la fonction ou le workflow à exposer
→ Définir le schéma d'entrée (types, contraintes, requis)
→ Définir le schéma de sortie (types, codes de retour)
→ Vérifier que la fonction respecte les règles BDCP (pas de réseau direct, CDP uniquement)
```

### Étape 2 — Génération de l'outil MCP

```
→ Créer le répertoire de l'outil sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\mcp-server-modular\tools\
→ Générer la définition JSON de l'outil MCP (inputSchema, outputSchema, handler)
→ Lier l'outil à un skill existant dans skills-index.json (si applicable)
→ Valider que l'outil est invoquable via MCP local
```

### Étape 3 — Validation des schémas

```
→ Valider le schéma d'entrée contre JSON Schema
→ Valider le schéma de sortie contre JSON Schema
→ Vérifier que tous les chemins dans les schémas sont absolus et explicites
→ Documenter les codes d'erreur possibles
```

### Étape 4 — Exposition et enregistrement

```
→ Exposer l'outil via le serveur MCP local
→ Tester l'invocation de l'outil avec des entrées de test
→ Capturer la preuve brute (stdout, code de retour, hash SHA-256, timestamp UTC)
→ Enregistrer dans le WAL (WAL-0x243)
→ Mettre à jour skills-index.json
```

## Anti-patterns

- ❌ Exposer une fonction sans schéma d'entrée/sortie valide
- ❌ Utiliser des chemins relatifs dans les schémas MCP (règle explicit-path-compliance)
- ❌ Exposer un outil qui viole les règles BDCP (accès réseau direct)
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
