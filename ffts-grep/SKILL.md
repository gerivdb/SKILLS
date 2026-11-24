---
name: ffts-grep
description: Indexeur plein texte rapide basé sur SQLite FTS5 — indexation FTS5 avec classement BM25 et requêtes sub-10ms sur arborescences de fichiers. Pattern inspiré de https://github.com/mneves75/ffts-grep
version: 1.0.0
intent_hash: 0xSKILL_FFTS_GREP_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/mneves75/ffts-grep
source_url: https://github.com/mneves75/ffts-grep
path: ffts-grep
---

# ffts-grep — Skill KiloCode

## Objectif

Fournir un indexeur plein texte rapide basé sur SQLite FTS5 avec classement BM25 et requêtes sub-10ms sur des arborescences de fichiers. Adapté à ENV2 pour remplacer les recherches `grep` répétitives par une indexation structurée.

## Déclencheur

Ce skill s'active quand :
- Il faut indexer des fichiers texte pour une recherche plein texte rapide
- Une recherche BM25 sur des arborescences de fichiers est nécessaire
- Des requêtes sub-10ms sont requises sur de gros volumes de texte
- L'indexation doit remplacer les allers-retours `grep` répétés

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `source_dir` | string | ✅ | Chemin absolu vers le répertoire à indexer |
| `db_path` | string | ✅ | Chemin absolu vers la base SQLite FTS5 cible |
| `search_query` | string | ❌ | Requête de recherche plein texte (FTS5) |
| `bm25_ranking` | boolean | ❌ | Appliquer le classement BM25 (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `indexed_files` | integer | Nombre de fichiers indexés |
| `search_results` | array | Résultats de la recherche FTS5 |
| `bm25_scores` | array | Scores BM25 des résultats |
| `query_latency_ms` | integer | Latence de la requête en ms |
| `evidence_hash` | string | Hash SHA-256 de l'indexation/recherche |

## Protocole Obligatoire

### Étape 1 — Vérification des chemins

```
→ Confirmer que source_dir et db_path sont absolus et explicites (règle explicit-path-compliance)
→ Vérifier l'existence de source_dir sur ENV2
→ Créer ou ouvrir la base SQLite FTS5 cible
```

### Étape 2 — Indexation FTS5

```
→ Indexer les fichiers de source_dir dans la base FTS5
→ Appliquer le classement BM25 si activé
→ Vérifier l'intégrité de l'index
```

### Étape 3 — Recherche et preuve

```
→ Exécuter la requête de recherche si fournie
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 du résultat
→ Enregistrer l'horodatage UTC et la latence
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser `grep` répété sur des fichiers bruts au lieu d'une indexation FTS5 structurée
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte mémoire ENV2 pour l'indexation

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
