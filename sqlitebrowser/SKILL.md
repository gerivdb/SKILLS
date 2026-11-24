---
name: sqlitebrowser
description: Navigateur visuel open source pour inspecter les tables, cellules, schémas et requêtes SQLite. Pattern inspiré de https://github.com/sqlitebrowser/sqlitebrowser
version: 1.0.0
intent_hash: 0xSKILL_SQLITEBROWSER_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/sqlitebrowser/sqlitebrowser
source_url: https://github.com/sqlitebrowser/sqlitebrowser
path: sqlitebrowser
---

# SQLiteBrowser — Skill KiloCode

## Objectif

Fournir une référence canonique pour SQLiteBrowser, navigateur visuel open source pour inspecter les tables, cellules, schémas et requêtes SQLite. Adapté à ENV2 pour l'inspection visuelle locale des bases SQLite sans interface web lourde.

## Déclencheur

Ce skill s'active quand :
- Il faut inspecter visuellement les tables, cellules et schémas d'une base SQLite
- Une interface graphique légère est nécessaire pour l'exploration manuelle
- Des requêtes SQL doivent être exécutées via un navigateur visuel
- L'environnement ENV2 nécessite un outil d'inspection desktop léger

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `table_name` | string | ❌ | Nom de la table à inspecter prioritairement |
| `sql_query` | string | ❌ | Requête SQL à exécuter dans le navigateur |
| `read_only` | boolean | ❌ | Forcer le mode lecture seule (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `tables_inspected` | array | Tables inspectées via le navigateur |
| `schema_info` | object | Schéma des tables explorées |
| `cell_values` | array | Valeurs de cellules observées |
| `query_result` | array | Résultats de la requête SQL exécutée |
| `evidence_hash` | string | Hash SHA-256 de la session |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Inspection visuelle

```
→ Lancer SQLiteBrowser sur la base cible
→ Activer le mode lecture seule
→ Inspecter les tables, cellules et schémas
→ Exécuter la requête SQL si fournie
```

### Étape 3 — Preuve d'exécution

```
→ Capturer les informations observées (schéma, cellules, résultats)
→ Calculer le hash SHA-256 de la session
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée sur la base
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser un client graphique lourd ou cloud pour l'inspection SQLite
- ❌ Désactiver le mode lecture seule sans autorisation explicite
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
