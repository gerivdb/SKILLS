---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_KEEP_X_SCRAPE_DOM_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : Keep-X Scrape DOM

## Déclencheur
Extraction des notes Google Keep via scraping DOM / CDP depuis une page `keep.google.com` ouverte.

## Protocole

### Étape 1 — Ouvrir Keep via CDP
Ouvrir `keep.google.com` dans Chrome (port 9222). Vérifier l'authentification (interface visible, libellés présents).

### Étape 2 — Extraire le DOM
Utiliser des sélecteurs CSS pour identifier les cartes de notes : `.U26pjb`, `.IKo2Vc`, `.J3Qhde`, `.sWZjRc`, `[role="listitem"]`, `.kA5tIf`, `.p1I5lc`, `.ABaVId`, `.NM3ZH`, `.MRbN4e`.

### Étape 3 — Extraire le contenu
Pour chaque note trouvée, extraire `title` (première ligne) et `body_text` (reste du texte).

### Étape 4 — Calculer le hash SHA-256
`hash_sha256 = SHA-256(title + body_text)` pour déduplication.

### Étape 5 — Insérer dans Keep-X
Transmettre à `keep-x-core` pour stockage dans DuckDB.

## Dépendances
- `sidekeep-x-collector` (S-10)
- `keep-x-causal-notes` (S-06)
- `sidekeep-x` citizen (C-09 dans vex.yaml)

## Référence ADR
- **ADR** : PRD-MOC-KEEP-X-MASTER-20261121
- **IntentHash** : 0xSKILL_KEEP_X_SCRAPE_DOM_20261121
- **Dépôt** : gerivdb/KEEP-X (L2-PLATFORM)
