---
name: ctxgrep
description: Recherche locale contexte / texte / regex / FTS5 — CLI locale sur SQLite + FTS5 combinant recherche exacte, regex, sémantique et mémoire. Pattern inspiré de https://github.com/yetone/ctxgrep
version: 1.0.0
intent_hash: 0xSKILL_CTXGREP_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/yetone/ctxgrep
source_url: https://github.com/yetone/ctxgrep
path: ctxgrep
---

# ctxgrep — Skill KiloCode

## Objectif

Fournir une CLI locale de recherche sur SQLite + FTS5 combinant recherche exacte, regex, sémantique et mémoire. Adapté à ENV2 pour remplacer les recherches `grep`/`glob` par une recherche indexée et structurée.

## Déclencheur

Ce skill s'active quand :
- Il faut effectuer une recherche locale combinant texte exact, regex et FTS5
- Une recherche sémantique sur une base SQLite est nécessaire
- La mémoire de contexte doit être préservée entre les recherches
- L'indexation SQLite remplace les recherches brutes répétitives

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers la base SQLite + FTS5 |
| `search_mode` | enum | ✅ | `exact` / `regex` / `fts5` / `semantic` |
| `search_pattern` | string | ✅ | Motif de recherche selon le mode |
| `context_window` | integer | ❌ | Fenêtre de contexte autour des résultats (défaut: 3) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `search_results` | array | Résultats de la recherche avec contexte |
| `match_count` | integer | Nombre de correspondances trouvées |
| `search_mode_used` | string | Mode de recherche appliqué |
| `context_lines` | array | Lignes de contexte autour des matchs |
| `evidence_hash` | string | Hash SHA-256 des résultats |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence de la base SQLite + FTS5 sur ENV2
```

### Étape 2 — Recherche indexée

```
→ Lancer ctxgrep sur la base cible
→ Appliquer le mode de recherche sélectionné (exact, regex, fts5, semantic)
→ Retourner les résultats avec fenêtre de contexte
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

- ❌ Utiliser `grep`/`glob` répétés au lieu d'une recherche indexée FTS5
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Modifier la base pendant la recherche
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
