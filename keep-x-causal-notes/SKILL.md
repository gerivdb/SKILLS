---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_KEEP_X_CAUSAL_NOTES_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : Keep-X Causal Notes

## Déclencheur
Toute opération de gestion des notes causales KEEP : stockage, lecture, déduplication, merkle seal.

## Protocole

### Étape 1 — Créer la table keep_entities
Schéma : id (VARCHAR PRIMARY KEY), timestamp (TIMESTAMP), title (VARCHAR), body_text (TEXT), labels (JSON), merkle_seal (VARCHAR), hash_sha256 (VARCHAR UNIQUE).

### Étape 2 — Insérer une note
Calculer hash_sha256 = SHA-256(title + body_text). Appliquer déduplication (ON CONFLICT DO NOTHING). Appliquer merkle_seal WAL-0x243-KEEP-ENTITY-PASS. Enregistrer timestamp UTC.

### Étape 3 — Lire une note
Requêter par entity_id ou hash_sha256.

### Étape 4 — Supprimer une note
Supprimer par entity_id avec vérification du merkle seal.

## Dépendances
- DuckDB (`WAL/do_core_inference.duckdb`, table `keep_entities`)
- `keep-x` citizen (C-06 dans vex.yaml)

## Référence ADR
- **ADR** : PRD-MOC-KEEP-X-MASTER-20261121
- **IntentHash** : 0xKEEP_X_CAUSAL_NOTES_20261121
- **Dépôt** : gerivdb/KEEP-X (L2-PLATFORM)
