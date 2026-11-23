---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_REGISTRY_SYNC_EXTENDED_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : Registry Sync Extended

## Déclencheur
Vérification de cohérence des registres : `known_repositories.yaml`, `ECOS_ROOT.json`, TOPOS registry. Détecter les dépôts absents, les local_path invalides, et les mismatches.

## Protocole

### Étape 1 — Lire known_repositories.yaml
Vérifier que chaque dépôt référencé a un `full_name`, un `local_path`, et un `status` (active/dormant/deprecated/archived).

### Étape 2 — Vérifier ECOS_ROOT.json
Vérifier la cohérence entre les dépôts listés et ceux présents sur le disque.

### Étape 3 — Vérifier TOPOS registry
Vérifier le registre détaillé des dépôts (registre canonique ENV).

### Étape 4 — Détecter les erreurs
- `ERROR` : registre incohérent → STOP
- `WARN` : inventaire HITL → signaler

### Étape 5 — Horodatage UTC
Enregistrer l'horodatage UTC de la vérification.

## Dépendances
- `ONTOLOGY/ONTOLOGY.yaml`
- `known_repositories.yaml`
- `ECOS_ROOT.json`
- TOPOS registry (repos.json)

## Référence ADR
- **ADR** : PRD-MOC-QUANTX-MASTER-20261121
- **IntentHash** : 0xSKILL_REGISTRY_SYNC_EXTENDED_20261121
- **Dépôt** : gerivdb/QUANTX (L2-PLATFORM)
