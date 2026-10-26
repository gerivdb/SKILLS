---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-26"
intent_hash: 0xSKILL_WSBJ_20261026
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-synaptic-bus-joiner/SKILL.md
---

# Skill — worktree-synaptic-bus-joiner

## Objectif

Enrôlement automatique du nouveau worktree dans le bus inter-worktrees `.kilo/bus/` et publication d'un signal `session-spawned.json` capté par GeriCode et relayé au bus métacluster `WAZAA`. Dès son premier souffle, le worktree annonce sa naissance à l'écosystème. Couche Worktree Engineering — opération d'enregistrement.

## Déclencheur

- `worktree-synaptic-bus-joiner`, `bus worktree`, `session-spawned.json`, `WAZAA`, `enrôlement worktree`
- À chaque création de worktree via `wt:spawn-clean` ou `agent_manager worktree`

## Entrées

- `worktree_path`: chemin physique du nouveau worktree (défaut : `$env:WORKTREE_PATH`)
- `worktree_id`: ID du worktree dans agent-manager.json (optionnel)
- `session_id`: ID de la session Agent Manager (optionnel)
- `branch_name`: nom de la branche (optionnel)

## Sorties

- Dossier `.kilo/bus/` créé dans le worktree
- Fichier `session-spawned.json` émis
- Entrée WAL NEXUS horodatée

## Règles

### 1. Création du bus local

Le worktree crée son propre sous-dossier `.kilo/bus/` à la racine. Ce dossier est le point d'entrée pour tous les signaux de ce worktree.

### 2. Signal de présence

Le fichier `session-spawned.json` contient :
- `worktree_id`, `session_id`, `branch_name`, `timestamp_utc`, `project_id`
- Il est lisible par GeriCode et relayé vers WAZAA (L4-TOOLS)

### 3. Découverte automatique

Les autres sessions détectent le nouveau worktree en surveillant `.kilo/bus/` sur chaque worktree connu.

## Script d'investigation

`scripts/join_bus.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_synaptic_bus_joiner.ps1` — créer un worktree, vérifier la création de `.kilo/bus/` et du fichier signal.

## Probes

- Chaque worktree créé possède `.kilo/bus/session-spawned.json`
- Le signal est lisible par GeriCode

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-synaptic-bus-joiner action=join timestamp=<ISO> worktree=<PATH> session=<SESSION_ID> branch=<BRANCH>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
