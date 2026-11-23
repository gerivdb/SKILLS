---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_M3_BRANCH_VERSIONING_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : M3 Branch Versioning

## Déclencheur
Gestion des branches M3 : v1 séquentiel, v2 collaboratif, v3 Dry-Run, v3-keep-x Dry-Run + Notes Causal.

## Protocole

### Étape 1 — Créer une branche
Définir l'ID, le nom, la description, et le statut (KEEP / SUPERSEDED).

### Étape 2 — Ajouter des nœuds
Chaque nœud a un ID, un nom, une description, et un statut.

### Étape 3 — Définir les dépendances
Une branche peut dépendre d'une branche précédente (ex: v2 dépend de v1).

### Étape 4 — Documenter les synapses
Connexions transverses entre personas, sections, et mécanismes.

### Étape 5 — Horodatage UTC
Enregistrer l'horodatage UTC de chaque création/modification de branche.

## Branches définies

| Branche | Nom | Statut | Description |
|---------|-----|--------|-------------|
| v1 | Format séquentiel | SUPERSEDED | Tour à tour → délibérations → DAG ASCII Bellard |
| v2 | Document collaboratif unique | KEEP | Édition parallèle, sections spécialisées, gardien tournant |
| v3 | Dry-Run Enhanced | KEEP — STABLE | Intelligence = Pruning Dry-Run, Gardien MDU, section #mdu |
| v3-keep-x | Dry-Run + Notes Causal | KEEP — NOUVEAU | Section #keep-x, SideKeep-X collecteur, pré-prompt v3 étendu |

## Dépendances
- `m3-tree-tim1g` (S-11)

## Référence ADR
- **ADR** : PRD-MOC-QUANTX-MASTER-20261121
- **IntentHash** : 0xSKILL_M3_BRANCH_VERSIONING_20261121
- **Dépôt** : gerivdb/QUANTX (L2-PLATFORM)
