---
name: sqlite-native
description: Moteur SQLite natif — B-trees, WITHOUT ROWID, index partiels/couverts, FTS5, R-Tree, tables virtuelles. Pattern inspiré de https://github.com/sqlite/sqlite
version: 1.0.0
intent_hash: 0xSKILL_SQLITE_NATIVE_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/sqlite/sqlite
source_url: https://github.com/sqlite/sqlite
path: sqlite-native
---

# SQLite Native — Skill KiloCode

## Objectif

Fournir la référence canonique du moteur SQLite natif pour le ciblage de « cases » (valeurs précises à l'intersection d'une ligne et d'une colonne) sur ENV2. B-trees (rowid ou WITHOUT ROWID), index partiels/couverts, FTS5, R-Tree, tables virtuelles. Adapté à la station HP Z600 (legacy, 24 Go RAM, CPU E5620) pour un accès structuré sans allers-retours réseau.

## Déclencheur

Ce skill s'active quand :
- Il faut cibler une valeur précise dans une table SQLite sans charger le fichier entier
- Une requête SELECT col_cible WHERE cle = ? est préférée à SELECT *
- Un index couvrant ou partiel doit être créé pour réduire l'empreinte mémoire/disque
- Une table virtuelle (FTS5, R-Tree, vec0) doit être utilisée pour le filtrage rapide

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite sur ENV2 |
| `table_name` | string | ✅ | Nom de la table cible |
| `key_column` | string | ✅ | Colonne de clé pour l'accès ciblé |
| `key_value` | string | ✅ | Valeur de la clé recherchée |
| `target_column` | string | ✅ | Colonne cible (la « case » à récupérer) |
| `use_covering_index` | boolean | ❌ | Créer un index couvrant si absent (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `cell_value` | string | Valeur de la case ciblée |
| `query_plan` | string | Résultat de EXPLAIN QUERY PLAN |
| `index_used` | string | Nom de l'index utilisé |
| `rows_scanned` | integer | Nombre de lignes scannées |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Ciblage de la case

```
→ Exécuter SELECT target_column FROM table_name WHERE key_column = ?
→ Vérifier que seule la colonne cible est retournée (pas de SELECT *)
→ Si un index couvrant est nécessaire : CREATE INDEX ... ON table(key_column, target_column)
```

### Étape 3 — Preuve d'exécution

```
→ Exécuter EXPLAIN QUERY PLAN pour valider l'utilisation de l'index
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture non autorisée n'a été effectuée
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser SELECT * au lieu de SELECT col_cible (charge les colonnes volumineuses)
- ❌ Découper le fichier .sqlite octet par octet au lieu d'utiliser les index B-tree
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
