---
name: fzql
description: Recherche floue interactive sur résultats SQLite — pipe les sorties sqlite3 vers fzf pour filtrer et sélectionner des lignes à la volée. Pattern inspiré de https://github.com/benewberg/fzql
version: 1.0.0
intent_hash: 0xSKILL_FZQL_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/benewberg/fzql
source_url: https://github.com/benewberg/fzql
path: fzql
---

# fzql — Skill KiloCode

## Objectif

Fournir une recherche floue interactive sur les résultats SQLite en pipeant les sorties `sqlite3` vers `fzf` pour filtrer et sélectionner des lignes à la volée. Adapté à ENV2 pour l'exploration rapide sans rechargement répété de fichiers bruts.

## Déclencheur

Ce skill s'active quand :
- Il faut filtrer des résultats SQLite de manière floue et interactive
- La sélection de lignes à la volée est nécessaire
- Un pipe `sqlite3 | fzf` est préféré à `grep`/`glob` répétés
- L'exploration doit rester légère sur ENV2

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `sql_query` | string | ✅ | Requête SQL dont les résultats seront filtrés par fzf |
| `fzf_options` | string | ❌ | Options supplémentaires pour fzf |
| `select_rows` | boolean | ❌ | Sélectionner les lignes filtrées (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `query_result` | array | Résultats bruts de la requête SQL |
| `filtered_rows` | array | Lignes filtrées par fzf |
| `selected_rows` | array | Lignes sélectionnées |
| `rows_count` | integer | Nombre de lignes filtrées |
| `evidence_hash` | string | Hash SHA-256 de la session |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Exécution et filtrage

```
→ Exécuter la requête SQL via sqlite3
→ Piper les résultats vers fzf pour filtrage flou interactif
→ Sélectionner les lignes si select_rows est true
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 de la capture
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée sur la base
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser `grep` sur des fichiers bruts au lieu d'une recherche floue indexée
- ❌ Exécuter des requêtes d'écriture dans le pipe
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
