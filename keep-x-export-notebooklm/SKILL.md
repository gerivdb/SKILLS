---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_KEEP_X_EXPORT_NOTEBOOKLM_20261121
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-21T23:00:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : Keep-X Export NotebookLM

## Déclencheur
Export des notes causales KEEP-X vers un bundle NotebookLM pour ingestion.

## Protocole

### Étape 1 — Lire les notes
Requêter toutes les notes depuis DuckDB `keep_entities`.

### Étape 2 — Dériver le titre
Prendre la première ligne du `body_text` comme titre, ou utiliser le champ `title` s'il existe.

### Étape 3 — Générer le bundle JSON
Créer un JSON avec structure : `target_format`, `source_file`, `source_timestamp_utc`, `generated_at`, `count`, `notes` (liste avec index, title, content, len, aria, source_selector, source_url).

### Étape 4 — Générer le bundle MD
Créer un markdown avec titre, métadonnées de génération, et chaque note précédée de `## N. titre` et séparée par `---`.

### Étape 5 — Horodatage UTC
Enregistrer l'horodatage UTC de génération du bundle.

## Dépendances
- `keep-x-causal-notes` (S-06)
- DuckDB `keep_entities` table

## Référence ADR
- **ADR** : PRD-MOC-KEEP-X-MASTER-20261121
- **IntentHash** : 0xSKILL_KEEP_X_EXPORT_NOTEBOOKLM_20261121
- **Dépôt** : gerivdb/KEEP-X (L2-PLATFORM)
