---
name: sqlite-utils
description: Utilitaire CLI & bibliothèque SQLite — inspection de tables, requêtes SQL, jointures rapides en mémoire et chargement de données structurées. Pattern inspiré de https://github.com/simonw/sqlite-utils
version: 1.0.0
intent_hash: 0xSKILL_SQLITE_UTILS_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/simonw/sqlite-utils
source_url: https://github.com/simonw/sqlite-utils
path: sqlite-utils
---

# sqlite-utils — Skill KiloCode

## Objectif

Fournir un utilitaire CLI et bibliothèque SQLite pour l'inspection de tables, les requêtes SQL, les jointures rapides en mémoire et le chargement de données structurées. Adapté à ENV2 pour l'automatisation scriptable de l'accès aux bases SQLite.

## Déclencheur

Ce skill s'active quand :
- Il faut inspecter les tables et le schéma d'une base SQLite via CLI
- Une requête SQL doit être exécutée avec sortie structurée
- Des jointures rapides en mémoire sont nécessaires
- Des données structurées doivent être chargées dans SQLite

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `sql_query` | string | ✅ | Requête SQL à exécuter |
| `output_format` | enum | ❌ | `table` / `json` / `csv` (défaut: `table`) |
| `insert_data` | array | ❌ | Données à insérer (si mode écriture autorisé) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `tables_info` | array | Informations sur les tables inspectées |
| `query_result` | array | Résultats de la requête SQL |
| `row_count` | integer | Nombre de lignes retournées |
| `output_format` | string | Format de sortie utilisé |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Inspection et exécution

```
→ Utiliser sqlite-utils CLI pour inspecter les tables et le schéma
→ Exécuter la requête SQL fournie
→ Formater la sortie selon output_format
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture non autorisée n'a été effectuée
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Exécuter des requêtes d'écriture sans validation préalable
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte mémoire ENV2

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
