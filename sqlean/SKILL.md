---
name: sqlean
description: Bibliothèque d'extensions SQLite — ajoute regexp (PCRE2), fuzzy (Levenshtein, Jaro-Winkler, phonétique), text, stats, vsv et fileio. Pattern inspiré de https://github.com/nalgeon/sqlean
version: 1.0.0
intent_hash: 0xSKILL_SQLEAN_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/nalgeon/sqlean
source_url: https://github.com/nalgeon/sqlean
path: sqlean
---

# sqlean — Skill KiloCode

## Objectif

Fournir une bibliothèque d'extensions SQLite ajoutant `regexp` (PCRE2), `fuzzy` (Levenshtein, Jaro-Winkler, phonétique), `text`, `stats`, `vsv` et `fileio`. Adapté à ENV2 pour enrichir les capacités de requête SQLite sans dépendances lourdes.

## Déclencheur

Ce skill s'active quand :
- Il faut ajouter des fonctionnalités regexp, fuzzy ou text à une base SQLite
- Une recherche floue (Levenshtein, Jaro-Winkler, phonétique) est nécessaire
- Des extensions SQLite légères sont préférées à des outils externes lourds
- L'environnement ENV2 nécessite des capacités de requête étendues sans CGO

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `extension` | enum | ✅ | `regexp` / `fuzzy` / `text` / `stats` / `vsv` / `fileio` |
| `sql_query` | string | ✅ | Requête SQL utilisant l'extension chargée |
| `load_extension` | boolean | ❌ | Charger l'extension dans la session (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `extension_loaded` | string | Nom de l'extension chargée |
| `query_result` | array | Résultats de la requête SQL avec l'extension |
| `rows_returned` | integer | Nombre de lignes retournées |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Chargement de l'extension

```
→ Charger l'extension sqlean sélectionnée (regexp, fuzzy, text, stats, vsv, fileio)
→ Vérifier que l'extension est disponible dans la session SQLite
```

### Étape 3 — Exécution et preuve

```
→ Exécuter la requête SQL utilisant l'extension
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée sur la base
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Charger des extensions non vérifiées ou non documentées
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Modifier la base pendant l'utilisation d'une extension en lecture
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
