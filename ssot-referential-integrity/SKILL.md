---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_SRI_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/ssot-referential-integrity/SKILL.md
---

# Skill — ssot-referential-integrity

## Objectif

Auditer la relation d'intégrité formelle sur les fichiers d'état local (`agent-manager.json`, `metadata.json`). Vérifier les clés étrangères et purger les onglets orphelins `pending:<uuid>` dans `tabOrder.local`. Couche Graphe d'État & JSON.

## Déclencheur

- Rupture de clé étrangère (`activeTarget` pointant sur une session inexistante).
- Fichier d'état agent corrompu après crash ou reload non terminé.
- Onglets orphelins `pending:<uuid>` bloquant la navigation agent.

## Entrées

- `state_path`: chemin du fichier `agent-manager.json` (défaut : `.kilo/agent-manager.json`).
- `metadata_path`: chemin du fichier `metadata.json` (optionnel).

## Sorties

- Rapport JSON d'intégrité des clés étrangères.
- Liste des sessions orphelines détectées.
- Liste des onglets `pending:<uuid>` purgés.
- Entrée WAL NEXUS horodatée.

## Règles

### 1. Vérifier l'existence de la clé étrangère activeTarget

- Lire `state.activeTarget.sessionId`.
- Vérifier que `state.activeTarget.sessionId ∈ keys(state.sessions)`.
- Si absent → session orpheline signalée.

### 2. Auditer toutes les sessions

- Pour chaque session dans `state.sessions`, vérifier que ses dépendances (fichiers ouverts, onglets) existent sur le filesystem.
- Signaler les sessions dont les fichiers référencés sont absents.

### 3. Purger les onglets orphelins pending:<uuid>

- Parcourir `state.tabOrder.local`.
- Détecter les entrées au format `pending:<uuid>`.
- Vérifier si l'UUID correspond à une session existante dans `state.sessions`.
- Si non → supprimer l'entrée orpheline.

### 4. Purge sécurisée

- Sauvegarder le fichier avant toute modification (`.bak` avec horodatage).
- Ne jamais supprimer une session active (celle pointée par `activeTarget`).
- Ne jamais supprimer un onglet non-pending.

## Script d'investigation

`scripts/audit.ps1` — voir ci-dessous.

## Tests

- `tests/test_ssot_referential_integrity.ps1` — créer un `agent-manager.json` de test avec session orpheline, vérifier la détection et la purge.

## Probes

- `activeTarget.sessionId` toujours présent dans `keys(state.sessions)`.
- Zéro entrée `pending:<uuid>` orpheline dans `tabOrder.local` après audit.

## WAL NEXUS

```
[WAL_NEXUS] skill=ssot-referential-integrity action=audit timestamp=<ISO> state_file=<PATH> activeTarget_valid=<bool> orphans=<n>
[WAL_NEXUS] skill=ssot-referential-integrity action=purge timestamp=<ISO> purged_tabs=<list> sessions_removed=<list>
```

## Référence ADR

- **ADR** : ADR-2026-06-07-001-ADR-GOVERNANCE-GATE
- **IntentHash** : 0xADR_GOVERNANCE_GATE_20260607
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
