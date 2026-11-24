---
name: harlequin
description: IDE SQL terminal avec catalogue & CLI headless (`hsql`) — exploration de catalogue/schéma, exécution de requêtes et compagnon CLI pour scripts/agents. Pattern inspiré de https://github.com/tconbeer/harlequin
version: 1.0.0
intent_hash: 0xSKILL_HARLEQUIN_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/tconbeer/harlequin
source_url: https://github.com/tconbeer/harlequin
path: harlequin
---

# Harlequin — Skill KiloCode

## Objectif

Fournir un IDE SQL terminal avec catalogue et schéma, exécution de requêtes et compagnon CLI `hsql` pour scripts et agents. Adapté à ENV2 pour l'exploration structurée de bases SQLite sans interface graphique lourde.

## Déclencheur

Ce skill s'active quand :
- Il faut explorer le catalogue et le schéma d'une base SQLite
- Une requête SQL complexe doit être exécutée avec affichage formaté
- Un CLI headless (`hsql`) est nécessaire pour l'automatisation par scripts
- La navigation interactive dans le catalogue est requise

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `sql_query` | string | ✅ | Requête SQL à exécuter |
| `output_format` | enum | ❌ | `table` / `json` / `csv` (défaut: `table`) |
| `headless` | boolean | ❌ | Utiliser `hsql` en mode headless (défaut: false) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `catalog` | array | Catalogue des tables et schémas |
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

### Étape 2 — Exploration et exécution

```
→ Lancer Harlequin (mode interactif) ou hsql (mode headless)
→ Explorer le catalogue et le schéma de la base
→ Exécuter la requête SQL fournie
→ Formater la sortie selon output_format
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée (mode lecture seule)
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser un IDE SQL graphique lourd sur ENV2
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
