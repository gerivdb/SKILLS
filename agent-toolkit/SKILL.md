---
name: agent-toolkit
description: Skills packagés avec dossiers scripts/ et references/ pour standardiser des tâches récurrentes. Pattern inspiré de https://github.com/softaworks/agent-toolkit
version: 1.0.0
intent_hash: 0xSKILL_AGENT_TOOLKIT_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/softaworks/agent-toolkit
source_url: https://github.com/softaworks/agent-toolkit
path: agent-toolkit
---

# Agent Toolkit — Skill KiloCode

## Objectif

Packager des skills avec dossiers scripts/ et references/ pour standardiser des tâches récurrentes. Ce skill encapsule le pattern du repo externe `agent-toolkit` adapté à ENV2, avec respect des règles de gouvernance et de chemins explicites.

## Déclencheur

Ce skill s'active quand :
- Une tâche récurrente doit être packagée en skill réutilisable
- Des scripts et références doivent être associés à un skill
- Un skill doit être standardisé pour réutilisation entre plusieurs sessions
- La structure d'un skill doit être auditée pour conformité au canon

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `task_name` | string | ✅ | Nom de la tâche récurrente |
| `scripts` | array | ✅ | Scripts associés à la tâche |
| `references` | array | ❌ | Références documentaires |
| `standardization_level` | enum | ❌ | basic / strict / canonical (défaut: strict) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `toolkit_name` | string | Nom du toolkit généré |
| `toolkit_path` | string | Chemin absolu vers le répertoire du toolkit |
| `script_inventory` | array | Inventaire des scripts avec chemins absolus et hash SHA-256 |
| `reference_inventory` | array | Inventaire des références avec sources |
| `evidence_hash` | string | Hash SHA-256 du toolkit |

## Protocole Obligatoire

### Étape 1 — Identification de la tâche récurrente

```
→ Identifier la tâche récurrente à packager
→ Vérifier qu'aucun skill existant dans skills-index.json ne couvre déjà ce besoin
→ Si un skill existe → l'utiliser ou l'étendre (pas de doublon)
```

### Étape 2 — Création de la structure du toolkit

```
→ Créer le répertoire sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS/<toolkit_name>/
→ Créer le fichier SKILL.md avec frontmatter (name, description, version, intent_hash)
→ Créer le sous-répertoire scripts/ pour les scripts
→ Créer le sous-répertoire references/ pour les références
```

### Étape 3 — Standardisation des scripts

```
→ Pour chaque script, vérifier que le chemin est absolu et explicite
→ Calculer le hash SHA-256 de chaque script
→ Documenter l'usage de chaque script dans le SKILL.md
→ Vérifier que chaque script retourne un code de retour (0 = succès)
```

### Étape 4 — Références et enregistrement

```
→ Documenter chaque référence avec sa source et son URL
→ Calculer le hash SHA-256 de la structure complète
→ Enregistrer dans le WAL (WAL-0x243)
→ Mettre à jour skills-index.json
```

## Anti-patterns

- ❌ Packager une tâche sans vérifier l'absence de skill existant (anti-doublon)
- ❌ Utiliser des chemins relatifs dans les scripts (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 pour chaque script et référence
- ❌ Ne pas mettre à jour skills-index.json après création du toolkit

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skills-lifecycle-governance
- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
