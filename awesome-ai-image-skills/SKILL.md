---
name: awesome-ai-image-skills
description: Exemples concrets de couplage SKILL.md + CLI/MCP pour figer des séquences d'exécution. Pattern inspiré de https://github.com/zhuyansen/awesome-ai-image-skills
version: 1.0.0
intent_hash: 0xSKILL_AWESOME_AI_IMAGE_SKILLS_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/zhuyansen/awesome-ai-image-skills
source_url: https://github.com/zhuyansen/awesome-ai-image-skills
path: awesome-ai-image-skills
---

# Awesome AI Image Skills — Skill KiloCode

## Objectif

Fournir des exemples concrets de couplage SKILL.md + CLI/MCP pour figer des séquences d'exécution. Ce skill encapsule le pattern du repo externe `awesome-ai-image-skills` adapté à ENV2, avec respect des règles de gouvernance, de chemins explicites et de preuve fraîche.

## Déclencheur

Ce skill s'active quand :
- Une séquence d'exécution doit être figée en skill + CLI/MCP
- Un exemple concret de skill doit être créé pour référence
- Un skill doit être couplé avec une interface CLI ou MCP
- La réutilisabilité d'un skill doit être démontrée par un exemple

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `execution_sequence` | array | ✅ | Séquence d'actions à figer |
| `interface_type` | enum | ✅ | skill / cli / mcp / hybride |
| `example_domain` | string | ✅ | Domaine de l'exemple (ex: image, git, cdp, mcp) |
| `reusable` | boolean | ❌ | Le skill doit être réutilisable (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `frozen_skill` | string | Nom du skill figé |
| `skill_path` | string | Chemin absolu vers le SKILL.md |
| `cli_definition` | object | Définition de l'interface CLI (si interface_type inclut cli) |
| `mcp_definition` | object | Définition de l'outil MCP (si interface_type inclut mcp) |
| `execution_proof` | object | Preuve d'exécution de la séquence figée |
| `evidence_hash` | string | Hash SHA-256 du skill figé |

## Protocole Obligatoire

### Étape 1 — Définition de la séquence

```
→ Lister toutes les actions de la séquence d'exécution
→ Vérifier que chaque action est atomique (1 outil = 1 résultat vérifiable)
→ Définir l'ordre d'exécution et les dépendances
→ Déterminer le type d'interface (skill, cli, mcp, hybride)
```

### Étape 2 — Création du skill figé

```
→ Créer le répertoire sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\awesome-ai-image-skills\
→ Générer le SKILL.md avec frontmatter (name, description, version, intent_hash)
→ Définir les triggers et anti_triggers basés sur la séquence
→ Spécifier le protocole obligatoire étape par étape
```

### Étape 3 — Couplage CLI/MCP

```
→ Si interface_type inclut cli → générer la définition CLI (commande, arguments, sortie)
→ Si interface_type inclut mcp → générer la définition d'outil MCP (inputSchema, outputSchema, handler)
→ Vérifier que tous les chemins sont absolus et explicites
→ Lier le skill aux interfaces générées
```

### Étape 4 — Test et preuve

```
→ Exécuter la séquence figée via l'interface choisie
→ Capturer la preuve brute (stdout, code de retour, hash SHA-256, timestamp UTC)
→ Vérifier que le skill est réutilisable (même entrée → même sortie)
→ Enregistrer dans le WAL (WAL-0x243)
→ Mettre à jour skills-index.json
```

## Anti-patterns

- ❌ Figer une séquence sans vérifier l'atomicité de chaque action
- ❌ Créer un skill sans interface d'invocation (CLI ou MCP)
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
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
- **Règle** : slm-fragmented-approach
