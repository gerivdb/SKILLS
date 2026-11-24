---
name: agentic-flow
description: Skills dédiés à l'automatisation de workflows, pipelines et coordination d'exécution. Pattern inspiré de https://github.com/ruvnet/agentic-flow
version: 1.0.0
intent_hash: 0xSKILL_AGENTIC_FLOW_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/ruvnet/agentic-flow
source_url: https://github.com/ruvnet/agentic-flow
path: agentic-flow
---

# Agentic Flow — Skill KiloCode

## Objectif

Fournir des skills dédiés à l'automatisation de workflows, pipelines et coordination d'exécution. Ce skill encapsule le pattern du repo externe `agentic-flow` adapté à ENV2, avec respect des règles BDCP et de la gouvernance des skills.

## Déclencheur

Ce skill s'active quand :
- Un pipeline d'exécution doit être orchestré entre plusieurs skills
- Une coordination d'exécution multi-agents doit être mise en place
- Un workflow doit être conditionnel (si/alors/sinon) basé sur des résultats de skills
- La réessai et la gestion d'erreur doivent être automatisées dans un pipeline

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `pipeline_definition` | object | ✅ | Définition du pipeline (étapes, conditions, boucles) |
| `entry_skill` | string | ✅ | Skill d'entrée du pipeline |
| `context` | object | ❌ | Contexte d'exécution (variables partagées entre étapes) |
| `max_retries` | integer | ❌ | Nombre max de tentatives par étape (défaut: 3) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `pipeline_id` | string | Identifiant unique du pipeline |
| `execution_trace` | array | Trace d'exécution de chaque étape |
| `context_final` | object | Contexte final après exécution |
| `final_status` | enum | success / partial / failed |
| `evidence_hash` | string | Hash SHA-256 de l'exécution du pipeline |

## Protocole Obligatoire

### Étape 1 — Définition du pipeline

```
→ Déclarer les étapes du pipeline avec leurs skills respectifs
→ Définir les conditions de transition entre étapes (si/alors/sinon)
→ Spécifier les boucles et les itérations
→ Définir le contexte partagé (variables entre étapes)
```

### Étape 2 — Validation des compétences

```
→ Pour chaque étape, vérifier que le skill existe dans skills-index.json
→ Vérifier que le skill est en statut active (pas draft/superseded/archived)
→ Vérifier que les entrées du skill sont fournies par le contexte ou l'étape précédente
```

### Étape 3 — Exécution coordonnée

```
→ Exécuter l'entrée du pipeline
→ Capturer la preuve brute de chaque étape (stdout, code de retour, hash SHA-256, timestamp UTC)
→ Mettre à jour le contexte après chaque étape
→ En cas d'échec, appliquer la politique de retry (max max_retries)
→ Si toutes les tentatives échouent, marquer l'étape comme failed et arrêter
```

### Étape 4 — Clôture et enregistrement

```
→ Enregistrer la trace complète dans le WAL (WAL-0x243)
→ Mettre à jour skills-index.json avec les stats d'utilisation
→ Vérifier que le working tree est propre
→ Produire le hash SHA-256 final de l'exécution
```

## Anti-patterns

- ❌ Orchestrer un pipeline sans valider que chaque skill est actif
- ❌ Exécuter un pipeline sans capturer la preuve brute de chaque étape
- ❌ Utiliser des chemins relatifs au lieu de chemins absolus (règle explicit-path-compliance)
- ❌ Oublier l'enregistrement WAL après exécution du pipeline

## Référence ADR

- **ADR** : ADR-SKILLS-LIFECYCLE-GOUVERNANCE.md
- **IntentHash** : 0xGOUV-SKILLS-LIFECYCLE_20261123
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
