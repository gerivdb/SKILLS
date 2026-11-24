---
name: litecli
description: CLI SQLite avec autocomplétion & coloration — édition interactive rapide de requêtes SQLite dans le terminal. Pattern inspiré de https://github.com/dbcli/litecli
version: 1.0.0
intent_hash: 0xSKILL_LITECLI_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/dbcli/litecli
source_url: https://github.com/dbcli/litecli
path: litecli
---

# litecli — Skill KiloCode

## Objectif

Fournir une CLI SQLite avec autocomplétion et coloration syntaxique pour l'édition interactive rapide de requêtes dans le terminal. Adapté à ENV2 pour l'exploration SQL interactive légère sans interface graphique.

## Déclencheur

Ce skill s'active quand :
- Il faut exécuter des requêtes SQLite de manière interactive dans un terminal
- L'autocomplétion et la coloration syntaxique sont nécessaires pour la productivité
- Une édition SQL rapide est requise sans client graphique lourd
- L'exploration doit rester légère sur ENV2

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `sql_query` | string | ❌ | Requête SQL à exécuter de manière interactive |
| `auto_completion` | boolean | ❌ | Activer l'autocomplétion (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `query_result` | array | Résultats de la requête SQL exécutée |
| `rows_returned` | integer | Nombre de lignes retournées |
| `auto_completion_used` | boolean | True si l'autocomplétion a été utilisée |
| `evidence_hash` | string | Hash SHA-256 de la session |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Édition SQL interactive

```
→ Lancer litecli sur la base cible
→ Activer l'autocomplétion et la coloration syntaxique
→ Exécuter la requête SQL fournie de manière interactive
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

- ❌ Utiliser un client graphique lourd sur ENV2
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
