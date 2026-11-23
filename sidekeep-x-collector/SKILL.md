---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_SIDKEEP_X_COLLECTOR_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : SideKeep-X Collector

## Déclencheur
Collecte des notes Google Keep via l'extension Chrome MV3 SideKeep-X (frontend/collecteur).

## Protocole

### Étape 1 — Installer l'extension
Charger l'extension non empaquetée depuis `D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\sidekeep-x\` dans Chrome (mode développeur).

### Étape 2 — Ouvrir Keep
Ouvrir `keep.google.com` dans Chrome. L'extension SideKeep-X (side panel) devient disponible.

### Étape 3 — Collecter les notes
SideKeep-X interagit avec Google Keep via le navigateur, collecte les notes par scraping DOM/CDP.

### Étape 4 — Transmettre à Keep-X
Les notes collectées sont transmises à Keep-X (backend DuckDB) pour stockage dans `keep_entities`.

### Étape 5 — Horodatage UTC
Enregistrer l'horodatage UTC de la collecte.

## Manifeste (manifest v3)
- `manifest_version`: 3
- `name`: SideKeep-X
- `version`: 1.0.2
- `permissions`: declarativeNetRequestWithHostAccess, sidePanel, storage
- `host_permissions`: https://keep.google.com/*
- `background.service_worker`: background/background.js
- `side_panel.default_path`: panel/index.html

## Dépendances
- `keep-x-causal-notes` (S-06)
- `keep-x-scrape-dom` (S-07)
- Chrome avec CDP (port 9222)

## Référence ADR
- **ADR** : PRD-MOC-KEEP-X-MASTER-20261121
- **IntentHash** : 0xSKILL_SIDKEEP_X_COLLECTOR_20261121
- **Dépôt** : gerivdb/KEEP-X (L2-PLATFORM)
