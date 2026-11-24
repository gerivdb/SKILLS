---
name: sqlite-vtab-opendal
description: Tables virtuelles SQLite fédérées pour interroger des métadonnées/fichiers sans ingestion massive. Pattern inspiré de https://github.com/mukhtaronif/sqlite-vtab-opendal
version: 1.0.0
intent_hash: 0xSKILL_SQLITE_VTAB_OPENDAL_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/mukhtaronif/sqlite-vtab-opendal
source_url: https://github.com/mukhtaronif/sqlite-vtab-opendal
path: sqlite-vtab-opendal
---

# SQLite vtab-opendal — Skill KiloCode

## Objectif

Fournir une référence canonique pour sqlite-vtab-opendal, tables virtuelles SQLite fédérées permettant d'interroger des métadonnées et fichiers sans ingestion massive. Adapté à ENV2 pour l'accès fédéré à des sources de données hétérogènes via SQL.

## Déclencheur

Ce skill s'active quand :
- Il faut interroger des fichiers ou métadonnées externes via SQL sans les importer dans SQLite
- Une table virtuelle fédérée est nécessaire pour l'accès à des sources hétérogènes
- L'ingestion massive de fichiers doit être évitée sur ENV2
- L'accès SQL unifié à plusieurs sources de données est requis

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `vtab_name` | string | ✅ | Nom de la table virtuelle opendal à créer |
| `source_path` | string | ✅ | Chemin vers la source de données fédérée |
| `sql_query` | string | ✅ | Requête SQL sur la table virtuelle |
| `columns` | array | ❌ | Colonnes exposées par la table virtuelle |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `vtab_created` | string | Nom de la table virtuelle créée |
| `query_result` | array | Résultats de la requête sur la table virtuelle |
| `source_files_accessed` | array | Fichiers de la source fédérée accessés |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification des chemins

```
→ Confirmer que db_path et source_path sont absolus et explicites (règle explicit-path-compliance)
→ Vérifier l'existence de la base SQLite et de la source sur ENV2
```

### Étape 2 — Création de la table virtuelle

```
→ Créer la table virtuelle opendal pointant vers source_path
→ Définir les colonnes exposées si fournies
→ Exécuter la requête SQL sur la table virtuelle
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucun fichier source n'a été modifié
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Importer massivement des fichiers dans SQLite au lieu d'utiliser une table virtuelle fédérée
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte disque ENV2 pour les sources fédérées

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
