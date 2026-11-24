---
name: n8n
description: Enchaînement de nœuds et scripts automatisés pour figer des suites d'actions répétitives. Pattern inspiré de https://github.com/n8n-io/n8n
version: 1.0.0
intent_hash: 0xSKILL_N8N_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/n8n-io/n8n
source_url: https://github.com/n8n-io/n8n
path: n8n
---

# n8n — Skill KiloCode

## Objectif

Enchaîner des nœuds et scripts automatisés pour figer des suites d'actions répétitives en workflows déterministes. Ce skill encapsule le pattern du repo externe `n8n` adapté à ENV2, avec respect des règles BDCP et exécution locale uniquement.

## Déclencheur

Ce skill s'active quand :
- Une suite d'actions répétitives doit être figée en workflow
- Plusieurs skills doivent être enchaînés dans un ordre déterministe
- Un workflow doit être déclenché par un événement (cron, webhook, fichier)
- La traçabilité de chaque étape du workflow doit être garantie

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `workflow_definition` | object | ✅ | Définition du workflow (nœuds, connexions, déclencheur) |
| `trigger_type` | enum | ✅ | cron / webhook / file / manual |
| `nodes` | array | ✅ | Liste des nœuds (skills ou commandes) à enchaîner |
| `error_handling` | enum | ❌ | stop / retry / skip (défaut: stop) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `workflow_id` | string | Identifiant unique du workflow |
| `execution_trace` | array | Trace d'exécution étape par étape |
| `final_status` | enum | success / partial / failed |
| `evidence_hash` | string | Hash SHA-256 de l'exécution du workflow |
| `timestamp_utc` | string | Horodatage UTC de l'exécution |

## Protocole Obligatoire

### Étape 1 — Définition du workflow

```
→ Déclarer les nœuds (skills ou commandes) dans l'ordre d'exécution
→ Définir les connexions entre nœuds (sortie de N → entrée de N+1)
→ Spécifier le déclencheur (cron, webhook, file, manual)
→ Définir la gestion d'erreur (stop, retry, skip)
```

### Étape 2 — Validation des nœuds

```
→ Pour chaque nœud, vérifier que le skill correspondant existe dans skills-index.json
→ Vérifier que chaque skill a un intent_hash et une version
→ Vérifier que les entrées/sorties sont compatibles entre nœuds consécutifs
```

### Étape 3 — Exécution et traçabilité

```
→ Déclencher le workflow selon le type de déclencheur
→ Pour chaque étape, capturer la preuve brute (stdout, code de retour, hash SHA-256, timestamp UTC)
→ Si une étape échoue et error_handling = stop → arrêter le workflow
→ Si error_handling = retry → relancer l'étape échouée (max 3 tentatives)
```

### Étape 4 — Enregistrement

```
→ Enregistrer la trace d'exécution complète dans le WAL (WAL-0x243)
→ Mettre à jour skills-index.json si de nouveaux skills sont invoqués
→ Vérifier que le working tree est propre après exécution
```

## Anti-patterns

- ❌ Chaîner des skills sans vérifier leur compatibilité d'entrée/sortie
- ❌ Exécuter un workflow sans capturer la preuve brute de chaque étape
- ❌ Utiliser un déclencheur réseau direct (interdit par BDCP, utiliser cron local uniquement)
- ❌ Oublier l'enregistrement WAL après exécution du workflow

## Référence ADR

- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
- **IntentHash** : 0xB05F1124CDC61605
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
