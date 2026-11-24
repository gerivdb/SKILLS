---
name: jdbrowser
description: Navigateur SQLite TUI en Rust — exploration rapide de tables et vues en ligne de commande avec copie presse-papiers. Pattern inspiré de https://github.com/Jkeyuk/JDbrowser
version: 1.0.0
intent_hash: 0xSKILL_JDBROWSER_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/Jkeyuk/JDbrowser
source_url: https://github.com/Jkeyuk/JDbrowser
path: jdbrowser
---

# JDbrowser — Skill KiloCode

## Objectif

Fournir un navigateur SQLite TUI en Rust pour l'exploration rapide de tables et vues en ligne de commande, avec copie presse-papiers. Adapté à ENV2 pour l'accès structuré aux bases SQLite sans rechargement répété de fichiers bruts.

## Déclencheur

Ce skill s'active quand :
- Il faut explorer des tables et vues SQLite rapidement en TUI
- Une copie presse-papiers des résultats est nécessaire
- Un navigateur Rust léger est préféré pour la performance sur ENV2
- La navigation doit éviter les allers-retours `grep`/`glob` répétés

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `table_name` | string | ❌ | Nom de la table à explorer prioritairement |
| `copy_results` | boolean | ❌ | Copier les résultats dans le presse-papiers (défaut: false) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `tables_views` | array | Tables et vues explorées |
| `selected_table_content` | array | Contenu de la table sélectionnée |
| `rows_count` | integer | Nombre de lignes dans la table |
| `results_copied` | boolean | True si copié dans le presse-papiers |
| `evidence_hash` | string | Hash SHA-256 de l'exploration |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Navigation JDbrowser

```
→ Lancer JDbrowser sur la base cible
→ Explorer les tables et vues disponibles
→ Afficher le contenu de la table cible si spécifiée
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
- ❌ Modifier la base pendant l'exploration (risque de corruption WAL)
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
