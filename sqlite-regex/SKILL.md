---
name: sqlite-regex
description: Extension regex rapide en Rust — opérateur regexp, extraction de groupes, regex_find_all et RegexSet directement dans SQL. Pattern inspiré de https://github.com/asg017/sqlite-regex
version: 1.0.0
intent_hash: 0xSKILL_SQLITE_REGEX_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/asg017/sqlite-regex
source_url: https://github.com/asg017/sqlite-regex
path: sqlite-regex
---

# sqlite-regex — Skill KiloCode

## Objectif

Fournir une extension regex rapide en Rust pour SQLite avec opérateur `regexp`, extraction de groupes, `regex_find_all` et `RegexSet` directement dans SQL. Adapté à ENV2 pour la recherche par expression régulières dans les colonnes texte et blob sans rechargement de fichiers bruts.

## Déclencheur

Ce skill s'active quand :
- Il faut effectuer une recherche par expression régulière dans une base SQLite
- L'extraction de groupes de capture est nécessaire directement en SQL
- Une extension regex légère en Rust est préférée à `grep` sur fichiers bruts
- La recherche doit rester dans l'environnement SQL pour la cohérence

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `table_name` | string | ✅ | Nom de la table à rechercher |
| `column_name` | string | ✅ | Nom de la colonne texte ou blob à filtrer |
| `regex_pattern` | string | ✅ | Motif d'expression régulière (PCRE2) |
| `extract_groups` | boolean | ❌ | Extraire les groupes de capture (défaut: false) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `matching_rows` | array | Lignes correspondant au motif regex |
| `extracted_groups` | array | Groupes de capture extraits (si activé) |
| `match_count` | integer | Nombre de lignes correspondantes |
| `evidence_hash` | string | Hash SHA-256 des résultats |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
→ Vérifier que l'extension sqlite-regex est chargée dans la session
```

### Étape 2 — Recherche regex SQL

```
→ Exécuter une requête SQL utilisant l'opérateur regexp sur la colonne cible
→ Extraire les groupes de capture si extract_groups est true
→ Retourner les lignes correspondantes
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 des résultats
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée sur la base
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser `grep` sur des fichiers bruts au lieu d'une recherche regex SQL structurée
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Modifier la base pendant la recherche regex en lecture
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
