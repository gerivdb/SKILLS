---
name: tables-import
description: Chargement de CSV / JSON / NDJSON / HTML en SQLite — importe des sources tabulaires ou flux JSON en tables relationnelles indexées. Pattern inspiré de https://github.com/zzolo/tables
version: 1.0.0
intent_hash: 0xSKILL_TABLES_IMPORT_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/zzolo/tables
source_url: https://github.com/zzolo/tables
path: tables-import
---

# tables-import — Skill KiloCode

## Objectif

Fournir un chargement de sources tabulaires (CSV, JSON, NDJSON, HTML) en tables relationnelles indexées dans SQLite. Adapté à ENV2 pour l'ingestion structurée de données tabulaires sans rechargement répété de fichiers bruts.

## Déclencheur

Ce skill s'active quand :
- Il faut importer des données tabulaires (CSV, JSON, NDJSON, HTML) dans SQLite
- Les données doivent être structurées en tables relationnelles indexées
- L'ingestion doit éviter les allers-retours `grep`/`glob` sur fichiers bruts
- L'environnement ENV2 nécessite une ingestion locale légère

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `source_file` | string | ✅ | Chemin absolu vers le fichier source (CSV, JSON, NDJSON, HTML) |
| `db_path` | string | ✅ | Chemin absolu vers la base SQLite cible |
| `target_table` | string | ✅ | Nom de la table cible dans SQLite |
| `file_format` | enum | ✅ | `csv` / `json` / `ndjson` / `html` |
| `index_columns` | array | ❌ | Colonnes à indexer après chargement |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `rows_imported` | integer | Nombre de lignes importées |
| `table_created` | string | Nom de la table créée ou mise à jour |
| `columns_indexed` | array | Colonnes indexées après chargement |
| `evidence_hash` | string | Hash SHA-256 de l'opération d'importation |

## Protocole Obligatoire

### Étape 1 — Vérification des chemins

```
→ Confirmer que source_file et db_path sont absolus et explicites (règle explicit-path-compliance)
→ Vérifier l'existence du fichier source sur ENV2
→ Vérifier que la base SQLite cible est accessible
```

### Étape 2 — Chargement structuré

```
→ Détecter le format du fichier source (CSV, JSON, NDJSON, HTML)
→ Importer les données dans la table cible de SQLite
→ Créer les index sur les colonnes spécifiées si index_columns est fourni
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout) de l'importation
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier l'intégrité des données importées (comptage des lignes)
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser `grep`/`glob` sur des fichiers bruts au lieu d'une ingestion structurée SQLite
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Charger des données sans indexer les colonnes clés
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
