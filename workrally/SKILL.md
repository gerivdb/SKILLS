---
name: workrally
description: Transforme des chaînes de traitements complexes en interfaces et APIs réutilisables. Pattern inspiré de https://github.com/Tencent/workrally
version: 1.0.0
intent_hash: 0xSKILL_WORKRALLY_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/Tencent/workrally
source_url: https://github.com/Tencent/workrally
path: workrally
---

# Workrally — Skill KiloCode

## Objectif

Transformer des chaînes de traitements complexes en interfaces et APIs réutilisables. Ce skill encapsule le pattern du repo externe `workrally` adapté à ENV2, avec respect des règles de gouvernance et d'exposition des skills.

## Déclencheur

Ce skill s'active quand :
- Une chaîne de traitements complexe doit être encapsulée en interface réutilisable
- Un skill doit être exposé comme API invoquable localement
- Un traitement par lots doit être standardisé en interface
- Une interface doit être générée pour un ensemble de skills liés

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `treatment_chain` | array | ✅ | Chaîne de traitements (skills ou commandes ordonnés) |
| `interface_type` | enum | ✅ | skill / cli / mcp_tool / api_local |
| `input_schema` | object | ❌ | Schéma des entrées de l'interface |
| `output_schema` | object | ❌ | Schéma des sorties de l'interface |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `interface_name` | string | Nom de l'interface générée |
| `interface_path` | string | Chemin absolu vers l'interface générée |
| `api_specification` | object | Spécification de l'API (entrées, sorties, codes de retour) |
| `wrapped_skills` | array | Skills encapsulés par l'interface |
| `evidence_hash` | string | Hash SHA-256 de l'interface générée |

## Protocole Obligatoire

### Étape 1 — Analyse de la chaîne de traitements

```
→ Lister tous les skills ou commandes de la chaîne
→ Vérifier que chaque skill existe dans skills-index.json
→ Identifier les entrées et sorties de chaque maillon
→ Déduire le schéma global d'entrée et de sortie
```

### Étape 2 — Génération de l'interface

```
→ Créer le répertoire de l'interface sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\
→ Générer le SKILL.md avec frontmatter et spécification API
→ Envelopper la chaîne de traitements dans l'interface choisie (skill, CLI, MCP, API)
→ Valider que chaque maillon de la chaîne est exécutable indépendamment
```

### Étape 3 — Définition de l'API

```
→ Spécifier le schéma d'entrée (types, contraintes, requis)
→ Spécifier le schéma de sortie (types, codes de retour)
→ Définir les codes d'erreur possibles pour chaque maillon
→ Documenter les anti-patterns bloquants
```

### Étape 4 — Test et enregistrement

```
→ Tester l'interface avec des entrées de test
→ Capturer la preuve brute (stdout, code de retour, hash SHA-256, timestamp UTC)
→ Enregistrer dans le WAL (WAL-0x243)
→ Mettre à jour skills-index.json
```

## Anti-patterns

- ❌ Générer une interface sans valider que chaque maillon de la chaîne existe
- ❌ Exposer une interface sans spécification d'entrée/sortie claire
- ❌ Utiliser des chemins relatifs au lieu de chemins absolus (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skills-lifecycle-governance
- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
