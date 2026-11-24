---
name: refly
description: Convertit des workflows et SOP en skills versionnés, exécutables et exposables en outils/MCP avec garde-fous déterministes. Pattern inspiré de https://github.com/refly-ai/refly
version: 1.0.0
intent_hash: 0xSKILL_REFLY_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/refly-ai/refly
source_url: https://github.com/refly-ai/refly
path: refly
---

# Refly — Skill KiloCode

## Objectif

Convertir des workflows et SOP (Standard Operating Procedures) en skills versionnés, exécutables et exposables en outils/MCP, avec garde-fous déterministes. Ce skill encapsule le pattern du repo externe `refly` adapté à ENV2.

## Déclencheur

Ce skill s'active quand :
- Un workflow répétitif doit être figé en skill exécutable
- Une SOP doit être convertie en skill versionné
- Un skill doit être exposé comme outil MCP invoquable
- Des garde-fous déterministes doivent être ajoutés à un skill existant

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `workflow_definition` | string | ✅ | Définition du workflow ou SOP à convertir |
| `target_format` | enum | ✅ | skill / mcp_tool / cli_command |
| `guardrails` | array | ❌ | Garde-fous déterministes à appliquer |
| `version` | string | ❌ | Version semver initiale (défaut: 1.0.0) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `generated_skill` | string | Nom du skill généré |
| `skill_path` | string | Chemin absolu vers le SKILL.md généré |
| `mcp_tool_definition` | object | Définition de l'outil MCP (si target_format = mcp_tool) |
| `guardrail_spec` | array | Spécification des garde-fous appliqués |
| `evidence_hash` | string | Hash SHA-256 du skill généré |

## Protocole Obligatoire

### Étape 1 — Analyse du workflow/SOP

```
→ Lire la définition du workflow ou SOP
→ Identifier les étapes atomiques (1 action = 1 outil)
→ Déterminer les entrées, sorties et garde-fous de chaque étape
→ Vérifier que chaque étape a une preuve brute correspondante
```

### Étape 2 — Génération du SKILL.md

```
→ Créer le répertoire du skill sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\
→ Écrire le SKILL.md avec frontmatter (name, description, version, intent_hash)
→ Définir les triggers et anti_triggers basés sur le workflow
→ Spécifier le protocole obligatoire étape par étape
→ Lier les références ADR et règles applicables
```

### Étape 3 — Application des garde-fous

```
→ Pour chaque étape, ajouter un garde-fou déterministe (ex: vérification de hash, de code de retour, de statut git)
→ Vérifier que chaque garde-fou est vérifiable automatiquement
→ Documenter les anti-patterns bloquants
```

### Étape 4 — Exposition MCP (optionnel)

```
→ Si target_format = mcp_tool, générer la définition d'outil MCP
→ Exposer le skill comme outil invoquable via MCP local
→ Enregistrer dans le WAL (WAL-0x243)
→ Mettre à jour skills-index.json
```

## Anti-patterns

- ❌ Convertir un workflow en skill sans garde-fous déterministes
- ❌ Exposer un skill non validé comme outil MCP
- ❌ Utiliser des chemins relatifs au lieu de chemins absolus (règle explicit-path-compliance)
- ❌ Oublier l'enregistrement dans skills-index.json

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skills-lifecycle-governance
- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
