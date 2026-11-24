---
name: sqlitebiter
description: Convertisseur multi-formats vers SQLite — transforme CSV, TSV, JSON, LDJSON, Markdown, HTML ou feuilles tabulaires en bases SQLite. Pattern inspiré de https://github.com/thombashi/sqlitebiter
version: 1.0.0
intent_hash: 0xSKILL_SQLITEBITER_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/thombashi/sqlitebiter
source_url: https://github.com/thombashi/sqlitebiter
path: sqlitebiter
---

# sqlitebiter — Skill KiloCode

## Objectif

Fournir un convertisseur multi-formats vers SQLite transformant CSV, TSV, JSON, LDJSON, Markdown, HTML ou feuilles tabulaires en bases SQLite. Adapté à ENV2 pour la conversion structurée de données tabulaires sans rechargement répété de fichiers bruts.

## Déclencheur

Ce skill s'active quand :
- Il faut convertir des fichiers tabulaires (CSV, TSV, JSON, LDJSON, Markdown, HTML) en base SQLite
- Une base SQLite doit être générée depuis des sources tabulaires hétérogènes
- La conversion doit éviter les allers-retours `grep`/`glob` sur fichiers bruts
- L'environnement ENV2 nécessite une conversion locale légère

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `source_file` | string | ✅ | Chemin absolu vers le fichier source tabulaire |
| `db_path` | string | ✅ | Chemin absolu vers la base SQLite cible |
| `source_format` | enum | ✅ | `csv` / `tsv` / `json` / `ldjson` / `markdown` / `html` |
| `target_table` | string | ❌ | Nom de la table cible dans SQLite (défaut: dérivé du nom de fichier) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `database_created` | string | Chemin de la base SQLite créée |
| `tables_created` | array | Noms des tables créées dans SQLite |
| `rows_converted` | integer | Nombre de lignes converties |
| `source_format_used` | string | Format source détecté et utilisé |
| `evidence_hash` | string | Hash SHA-256 de l'opération de conversion |

## Protocole Obligatoire

### Étape 1 — Vérification des chemins

```
→ Confirmer que source_file et db_path sont absolus et explicites (règle explicit-path-compliance)
→ Vérifier l'existence du fichier source sur ENV2
```

### Étape 2 — Conversion vers SQLite

```
→ Détecter le format du fichier source (CSV, TSV, JSON, LDJSON, Markdown, HTML)
→ Convertir les données en base SQLite avec la table cible
→ Vérifier l'intégrité de la base créée
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout) de la conversion
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier l'intégrité de la base SQLite créée
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser `grep`/`glob` sur des fichiers bruts au lieu d'une conversion structurée SQLite
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Convertir des données sans vérifier l'intégrité de la base résultante
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
