---
name: dolt
description: Base de données SQL avec versionnage type Git (branches, diffs, merges au niveau des lignes/tables). Pattern inspiré de https://github.com/dolthub/dolt
version: 1.0.0
intent_hash: 0xSKILL_DOLT_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/dolthub/dolt
source_url: https://github.com/dolthub/dolt
path: dolt
---

# Dolt — Skill KiloCode

## Objectif

Fournir une référence canonique pour Dolt, base de données SQL avec versionnage type Git (branches, diffs, merges au niveau des lignes/tables). Adapté à ENV2 pour le versionnage structuré de données SQLite/SQL sans duplication de fichiers entiers.

## Déclencheur

Ce skill s'active quand :
- Il faut versionner des données SQL comme du code Git (branches, diffs, merges)
- Des diffs au niveau des lignes/tables sont nécessaires pour le traçage
- Un merge de modifications de données doit être effectué sans duplication
- L'environnement ENV2 nécessite un versionnage de données léger et local

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers la base Dolt/SQLite |
| `operation` | enum | ✅ | `branch` / `diff` / `merge` / `commit` / `log` |
| `branch_name` | string | ❌ | Nom de la branche pour l'opération |
| `target_table` | string | ❌ | Table cible pour le diff ou le merge |
| `commit_message` | string | ❌ | Message de commit pour l'opération |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `operation_result` | string | Résultat de l'opération Dolt |
| `diff_summary` | array | Résumé des différences (si opération diff) |
| `branches` | array | Liste des branches existantes |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence de la base Dolt sur ENV2
```

### Étape 2 — Opération de versionnage

```
→ Exécuter l'opération Dolt demandée (branch, diff, merge, commit, log)
→ Si operation = diff, cibler la table spécifique si fournie
→ Si operation = commit, inclure le message de commit
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier l'intégrité de la base après l'opération
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Dupliquer des fichiers entiers pour versionner des données (au lieu de diffs de lignes)
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte disque ENV2 pour les branches multiples

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
