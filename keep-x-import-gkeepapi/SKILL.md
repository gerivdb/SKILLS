---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_KEEP_X_IMPORT_GKEEPAPI_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : Keep-X Import gKeepAPI

## Déclencheur
Import des notes Google Keep via l'API interne non officielle (gkeepapi) nécessitant un master token.

## Protocole

### Étape 1 — Authentification
Obtenir le master token via variable d'environnement `KEEP_MASTER_TOKEN` ou keyring (`gerivdb-keep-reader` / `master_token`).

### Étape 2 — Connexion gKeepAPI
Authentifier via `gkeepapi.Keep().authenticate(email, master_token)`.

### Étape 3 — Récupérer les notes
Appeler `keep.all()` pour récupérer toutes les notes Google Keep.

### Étape 4 — Formater et insérer
Pour chaque note : extraire `title`, `body_text`, `labels`, `timestamp`. Calculer `hash_sha256`. Insérer dans DuckDB `keep_entities` avec déduplication.

### Étape 5 — Horodatage UTC
Enregistrer l'horodatage UTC de l'import.

## Dépendances
- `gkeepapi` installé
- `keep-x-causal-notes` (S-06)
- Master token configuré

## Référence ADR
- **ADR** : PRD-MOC-KEEP-X-MASTER-20261121
- **IntentHash** : 0xSKILL_KEEP_X_IMPORT_GKEEPAPI_20261121
- **Dépôt** : gerivdb/KEEP-X (L2-PLATFORM)
