---
name: teaqlite
description: Navigateur & éditeur TUI clavier en Go — parcours de tables, recherche floue (/), vue ligne par ligne et exécution SQL dans le terminal. Pattern inspiré de https://github.com/taigrr/teaqlite
version: 1.0.0
intent_hash: 0xSKILL_TEAQLITE_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/taigrr/teaqlite
source_url: https://github.com/taigrr/teaqlite
path: teaqlite
---

# TeaQLite — Skill KiloCode

## Objectif

Naviguer et éditer des bases SQLite via un TUI clavier en Go, avec recherche floue, exécution SQL inline et vue ligne par ligne. Adapté à ENV2 pour l'exploration interactive légère sans rechargement répété de fichiers bruts.

## Déclencheur

Ce skill s'active quand :
- Il faut parcourir des tables SQLite avec recherche floue (`/`)
- Une exécution SQL ad hoc est nécessaire dans un terminal TUI
- La navigation ligne par ligne est requise pour inspecter des données tabulaires
- Un éditeur SQLite clavier léger est préféré à `grep`/`glob` répétés

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `query` | string | ❌ | Requête SQL à exécuter (lecture seule recommandée) |
| `search_pattern` | string | ❌ | Motif de recherche floue dans les tables |
| `max_results` | integer | ❌ | Nombre max de résultats (défaut: 100) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `navigated_tables` | array | Tables parcourues avec leur contenu |
| `query_result` | array | Résultats de la requête SQL exécutée |
| `search_matches` | array | Correspondances de recherche floue |
| `row_count` | integer | Nombre de lignes retournées |
| `evidence_hash` | string | Hash SHA-256 de la session TUI |

## Protocole Obligatoire

### Étape 1 — Préparation du chemin DB

```
→ Vérifier que db_path est absolu et explicite (règle explicit-path-compliance)
→ Confirmer l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Navigation TUI

```
→ Lancer teaqlite sur la base cible
→ Parcourir les tables avec les raccourcis clavier
→ Appliquer la recherche floue si search_pattern est fourni
→ Exécuter la requête SQL si fournie (mode lecture seule)
```

### Étape 3 — Capture et preuve

```
→ Capturer la sortie du terminal (stdout) de la session TUI
→ Calculer le hash SHA-256 de la capture
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune modification n'a été apportée à la base
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Exécuter des requêtes SQL d'écriture sans autorisation explicite
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte mémoire ENV2 (<40 Mo recommandé)

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
