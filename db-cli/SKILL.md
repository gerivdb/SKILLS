---
name: db-cli
description: CLI d'inspection relationnelle avec sorties table/json/csv — description de tables, échantillonnage de lignes et requêtes en lecture seule formatées pour scripts ou agents. Pattern inspiré de https://github.com/jeffersongoncalves/db-cli
version: 1.0.0
intent_hash: 0xSKILL_DB_CLI_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/jeffersongoncalves/db-cli
source_url: https://github.com/jeffersongoncalves/db-cli
path: db-cli
---

# db-cli — Skill KiloCode

## Objectif

Fournir une CLI d'inspection relationnelle avec sorties formatées (`table`, `json`, `csv`) pour la description de tables, l'échantillonnage de lignes et les requêtes en lecture seule. Adapté à ENV2 pour l'exploration scriptable de bases SQLite.

## Déclencheur

Ce skill s'active quand :
- Il faut décrire les tables et le schéma d'une base SQLite
- Un échantillonnage de lignes est nécessaire pour inspection
- Des requêtes en lecture seule doivent retourner des sorties formatées pour scripts
- Une CLI structurée remplace les recherches brutes `grep`/`glob`

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `table_name` | string | ❌ | Nom de la table à décrire ou échantillonner |
| `sql_query` | string | ❌ | Requête SQL en lecture seule à exécuter |
| `output_format` | enum | ❌ | `table` / `json` / `csv` (défaut: `table`) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `table_schema` | object | Schéma de la table décrite |
| `sample_rows` | array | Lignes échantillonnées de la table |
| `query_result` | array | Résultats de la requête SQL |
| `output_format` | string | Format de sortie utilisé |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Inspection relationnelle

```
→ Lancer db-cli sur la base cible
→ Décrire le schéma de la table si table_name est fourni
→ Échantillonner les lignes de la table
→ Exécuter la requête SQL en lecture seule si fournie
→ Formater la sortie selon output_format
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée sur la base
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser `grep`/`glob` répétés au lieu d'une inspection relationnelle structurée
- ❌ Exécuter des requêtes d'écriture sans validation préalable
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
