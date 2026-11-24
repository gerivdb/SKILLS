---
name: sqlit
description: Client TUI léger multi-bases inspiré de lazygit — parcourir les tables, lancer des requêtes et copier les résultats. Pattern inspiré de https://github.com/Maxteabag/sqlit
version: 1.0.0
intent_hash: 0xSKILL_SQLIT_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/Maxteabag/sqlit
source_url: https://github.com/Maxteabag/sqlit
path: sqlit
---

# sqlit — Skill KiloCode

## Objectif

Fournir un client TUI léger multi-bases inspiré de `lazygit` pour parcourir les tables SQLite, lancer des requêtes et copier les résultats. Adapté à ENV2 pour l'exploration rapide sans rechargement répété de fichiers bruts.

## Déclencheur

Ce skill s'active quand :
- Il faut parcourir rapidement plusieurs tables SQLite dans un TUI
- Des requêtes SQL doivent être lancées depuis un terminal clavier
- Les résultats doivent être copiables pour réutilisation
- Une navigation style `lazygit` est préférée pour la productivité

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `query` | string | ❌ | Requête SQL à exécuter |
| `copy_results` | boolean | ❌ | Copier les résultats dans le presse-papiers (défaut: false) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `tables_browsed` | array | Tables parcourues dans le TUI |
| `query_result` | array | Résultats de la requête SQL |
| `rows_returned` | integer | Nombre de lignes retournées |
| `results_copied` | boolean | True si les résultats ont été copiés |
| `evidence_hash` | string | Hash SHA-256 de la session |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Navigation TUI sqlit

```
→ Lancer sqlit sur la base cible
→ Parcourir les tables avec les raccourcis clavier (style lazygit)
→ Lancer la requête SQL si fournie
→ Copier les résultats si copy_results est true
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

- ❌ Utiliser un client graphique lourd sur ENV2
- ❌ Écrire dans la base pendant l'exploration
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
