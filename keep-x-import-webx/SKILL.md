---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_KEEP_X_IMPORT_WEBX_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:45:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : Keep-X Import via WEBX

## Déclencheur
Toute opération d'importation de notes Google Keep dans la base DuckDB `keep_entities` sans dépendre de gkeepapi ni d'un dialogue LLM à chaque requête.

## Protocole

### Étape 1 — Lancement du navigateur via WEBX
Utiliser `WebCluster` pour lancer un navigateur headless (CamoFox, Obscura, Lightpanda, Chrome) ou se connecter à un navigateur déjà ouvert (Chrome CDP port 9222).

### Étape 2 — Navigation vers Google Keep
Naviguer vers `https://keep.google.com` avec le navigateur lancé ou déjà ouvert.

### Étape 3 — Extraction DOM via CDP
Utiliser `ScrapeDom` pour extraire le contenu des notes depuis le DOM de Google Keep via sélecteurs CSS avec fallback JavaScript.

### Étape 4 — Insertion dans DuckDB
Insérer chaque note dans la table `keep_entities` avec :
- `entity_id` : `keep-` + 8 premiers caractères du hash SHA-256
- `timestamp` : horodatage UTC
- `title` : première ligne du texte
- `body_text` : reste du texte
- `labels` : `[]` (JSON vide)
- `merkle_seal` : `WAL-0x243-KEEP-IMPORT-WEBX`
- `hash_sha256` : SHA-256(title + body_text) pour déduplication

### Étape 5 — Déduplication
`ON CONFLICT (hash_sha256) DO NOTHING` pour éviter les doublons.

## Dépendances
- `WEBX` (D:\DO\WEB\TOOLS\L2-PLATFORM\WEBX\src) — bibliothèques Python
- `duckdb` — base de données locale
- `playwright` — pour connexion CDP

## Navigateurs supportés
| Navigateur | Driver | Port CDP | Headless | Anti-detect | Souverain |
|------------|--------|----------|----------|-------------|-----------|
| CamoFox | firefox-headless | 9225 | Oui | Oui | Non |
| Obscura | rust-cdp | 9226 | Oui | Oui | Oui |
| Lightpanda | wsl-gecko | 9224 | Oui | Non | Non |
| Chrome | chrome-cdp | 9222 | Oui | Non | Non |
| Playwright | playwright | variable | Oui | Non | Non |

## Fichiers
- `keep_x_import_webx.py` — implémentation principale
- `test_webx_drivers.py` — test des drivers WEBX

## Référence ADR
- **ADR** : PRD-MOC-KEEP-X-MASTER-20261121
- **IntentHash** : 0xSKILL_KEEP_X_IMPORT_WEBX_20261121
- **Dépôt** : gerivdb/KEEP-X (L2-PLATFORM)
