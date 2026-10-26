---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-26"
intent_hash: 0xSKILL_PTS_20261026
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/pending-tab-sentinel/SKILL.md
---

# Skill — pending-tab-sentinel

## Objectif

Détecter et éliminer les embryons de freeze UI dans l'Agent Manager. Surveille la clé `tabOrder.local` de `agent-manager.json` et neutralise toute entrée `pending:<uuid>` qui n'est pas associée à une session validée. Couche CRUD — opération Nettoyage + Prévention.

## Déclencheur

- `pending-tab-sentinel`, `freeze UI`, `tabOrder.local`, `pending:uuid`, `sessions orphelines`, `agent-manager.json`
- Avant toute opération de mise à jour de l'UI Agent Manager ou à la fin d'une session

## Entrées

- `agent_manager_json_path`: chemin vers le fichier `agent-manager.json` (obligatoire)
- `validate_sessions`: si true, vérifie que chaque `pending:<uuid>` correspond à une session active (défaut : true)

## Sorties

- Rapport : `pending_keys_found`, `pending_keys_neutralized`, `orphan_sessions`, `cleaned` (bool)
- Fichier `agent-manager.json` mis à jour avec les clés `pending:<uuid>` invalides retirées

## Règles

### 1. Détection des embryons de freeze

Toute clé du format `pending:<uuid>` dans `tabOrder.local` est suspecte. Elle indique un travail de tab non terminé qui peut figer l'interface.

### 2. Neutralisation conditionnelle

Une clé `pending:<uuid>` est neutralisée (retirée) si :
- Aucun UUID de session valide n'existe dans `sessions`, ou
- La session associée n'est plus dans l'état `active`

### 3. Préservation des sessions valides

Si une clé `pending:<uuid>` correspond à une session active et validée, elle est conservée et signalée comme "en cours".

### 4. Interdiction de suppression aveugle

Jamais supprimer une clé `pending:` sans avoir vérifié l'absence de session associée dans `agent-manager.json`.

## Script d'investigation

`scripts/pending_tab_sentinel.ps1` — voir ci-dessous.

## Tests

- `tests/test_pending_tab_sentinel.ps1` — créer un agent-manager.json avec clés pending valides et orphelines, vérifier le nettoyage.

## Probes

- Zéro clé `pending:<uuid>` orpheline conservée après exécution
- Zéro session active invalidée par erreur

## WAL NEXUS

```
[WAL_NEXUS] skill=pending-tab-sentinel action=scan timestamp=<ISO> pending_found=<n> pending_neutralized=<m> orphan_sessions=<k>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed