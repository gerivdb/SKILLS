---
name: duckdb-sqlite
description: Extension permettant à DuckDB de lire/écrire directement des fichiers SQLite pour des coupes analytiques rapides. Pattern inspiré de https://github.com/duckdb/duckdb-sqlite
version: 1.0.0
intent_hash: 0xSKILL_DUCKDB_SQLITE_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/duckdb/duckdb-sqlite
source_url: https://github.com/duckdb/duckdb-sqlite
path: duckdb-sqlite
---

# DuckDB-SQLite — Skill KiloCode

## Objectif

Fournir une référence canonique pour l'extension DuckDB-SQLite permettant à DuckDB de lire/écrire directement des fichiers SQLite pour des coupes analytiques rapides. Adapté à ENV2 pour l'analyse analytique sur bases SQLite locales sans ingestion massive.

## Déclencheur

Ce skill s'active quand :
- Il faut effectuer des coupes analytiques (OLAP) sur une base SQLite locale
- DuckDB doit lire/écrire directement un fichier .sqlite sans conversion
- Une requête analytique complexe doit être exécutée sur des données SQLite
- L'environnement ENV2 nécessite un moteur analytique léger sans serveur

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `sqlite_db_path` | string | ✅ | Chemin absolu vers le fichier SQLite source |
| `duckdb_db_path` | string | ❌ | Chemin vers la base DuckDB cible (ou :memory:) |
| `analytic_query` | string | ✅ | Requête SQL analytique sur les données SQLite |
| `attach_mode` | boolean | ❌ | Attacher le fichier SQLite à DuckDB (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `analytic_result` | array | Résultats de la requête analytique |
| `tables_accessed` | array | Tables SQLite accessées via DuckDB |
| `rows_processed` | integer | Nombre de lignes traitées |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification des chemins

```
→ Confirmer que sqlite_db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Analyse analytique

```
→ Attacher le fichier SQLite à DuckDB (ou ouvrir en :memory:)
→ Exécuter la requête analytique sur les données SQLite
→ Retourner les résultats de la coupe analytique
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture non autorisée n'a été effectuée sur le SQLite source
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Convertir le fichier SQLite vers un autre format avant analyse (ingestion massive)
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte mémoire ENV2 pour DuckDB

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
