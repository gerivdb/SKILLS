---
name: minisqlite
description: Implémentation éducative/modulaire d'un moteur type SQLite en Go (B-trees de tables/index, index couvrants, curseurs). Pattern inspiré de https://github.com/cursor/minisqlite
version: 1.0.0
intent_hash: 0xSKILL_MINISQLITE_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/cursor/minisqlite
source_url: https://github.com/cursor/minisqlite
path: minisqlite
---

# minisqlite — Skill KiloCode

## Objectif

Fournir une référence canonique pour minisqlite, implémentation éducative/modulaire d'un moteur type SQLite en Go (B-trees de tables/index, index couvrants, curseurs). Adapté à ENV2 pour la compréhension et l'enseignement des mécanismes internes de SQLite sans dépendance au binaire officiel.

## Déclencheur

Ce skill s'active quand :
- Il faut comprendre les mécanismes internes de SQLite (B-trees, curseurs, index)
- Une implémentation modulaire et éducative est préférée au binaire monolithique
- Le code source du moteur doit être lu pour diagnostiquer un comportement
- L'environnement ENV2 nécessite un moteur léger pour l'apprentissage

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier de base minisqlite |
| `operation` | enum | ✅ | `read` / `inspect-btree` / `inspect-cursor` / `inspect-index` |
| `target_table` | string | ❌ | Table cible pour l'inspection |
| `target_index` | string | ❌ | Index cible pour l'inspection |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `btree_structure` | object | Structure du B-tree de la table/index |
| `cursor_position` | object | Position actuelle du curseur |
| `index_entries` | array | Entrées de l'index inspecté |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier sur ENV2
```

### Étape 2 — Inspection du moteur

```
→ Ouvrir la base avec minisqlite (implémentation Go)
→ Exécuter l'opération demandée (read, inspect-btree, inspect-cursor, inspect-index)
→ Retourner la structure interne observée
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture non autorisée n'a été effectuée
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser le binaire SQLite officiel quand une implémentation modulaire suffit
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte mémoire ENV2

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
