---
name: sqlite-tui-megamanics
description: Navigateur SQLite TUI avec plugins de recherche — navigation vim, tri de colonnes et modes de recherche (mot-clé, FTS5, regex, filtre colonne, WHERE). Pattern inspiré de https://github.com/megamanics/sqlite-tui
version: 1.0.0
intent_hash: 0xSKILL_SQLITE_TUI_MEGAMANICS_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/megamanics/sqlite-tui
source_url: https://github.com/megamanics/sqlite-tui
path: sqlite-tui-megamanics
---

# SQLite TUI (megamanics) — Skill KiloCode

## Objectif

Fournir un navigateur SQLite TUI avec plugins de recherche : navigation vim, tri de colonnes et modes de recherche (mot-clé, FTS5, regex, filtre colonne, WHERE). Adapté à ENV2 pour l'exploration structurée et la recherche indexée dans les bases SQLite.

## Déclencheur

Ce skill s'active quand :
- Il faut naviguer dans des tables SQLite avec un mode vim
- Une recherche FTS5 ou regex est nécessaire sur des colonnes texte
- Le tri de colonnes et le filtrage WHERE sont requis
- Un TUI avec plugins de recherche est préféré à `grep`/`glob` répétés

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `search_mode` | enum | ❌ | `keyword` / `fts5` / `regex` / `column_filter` / `where` (défaut: `keyword`) |
| `search_pattern` | string | ❌ | Motif de recherche selon le mode sélectionné |
| `target_table` | string | ❌ | Table cible de la recherche |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `tables` | array | Tables navigées avec leur contenu |
| `search_matches` | array | Correspondances de recherche selon le mode |
| `columns_sorted` | array | Colonnes triées appliquées |
| `row_count` | integer | Nombre de lignes correspondantes |
| `evidence_hash` | string | Hash SHA-256 de l'exploration |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
```

### Étape 2 — Navigation et recherche

```
→ Lancer le TUI SQLite (megamanics) sur la base cible
→ Naviguer avec les raccourcis vim
→ Appliquer le mode de recherche sélectionné (keyword, FTS5, regex, column_filter, where)
→ Trier les colonnes si nécessaire
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

- ❌ Utiliser `grep`/`glob` répétés sur des fichiers bruts au lieu d'une recherche indexée FTS5/regex
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Modifier la base pendant l'exploration
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
