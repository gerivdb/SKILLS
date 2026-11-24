---
name: astchunk
description: Boîte à outils Python basée sur Tree-sitter pour découper le code en segments syntaxiques cohérents (AST chunking/slicing). Pattern inspiré de https://github.com/yilinjz/astchunk
version: 1.0.0
intent_hash: 0xSKILL_ASTCHUNK_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/yilinjz/astchunk
source_url: https://github.com/yilinjz/astchunk
path: astchunk
---

# AST Chunk — Skill KiloCode

## Objectif

Fournir une référence canonique pour astchunk, boîte à outils Python basée sur Tree-sitter pour découper le code en segments syntaxiques cohérents (AST chunking/slicing). Adapté à ENV2 pour le découpage de code en tranches utilisables par une couche neurosymbolique sans chargement complet des fichiers.

## Déclencheur

Ce skill s'active quand :
- Il faut découper un fichier source en segments syntaxiques cohérents (chunks)
- Le découpage doit respecter la structure AST (pas de coupure au milieu d'une fonction)
- Les chunks doivent être utilisables pour l'indexation ou l'analyse neurosymbolique
- L'environnement ENV2 nécessite un découpage léger sans chargement complet des fichiers

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `file_path` | string | ✅ | Chemin absolu vers le fichier source à découper |
| `language` | string | ✅ | Langage de programmation (ex: python, zig, javascript) |
| `max_chunk_size` | integer | ❌ | Taille max d'un chunk en tokens/lignes (défaut: 500) |
| `respect_ast_boundaries` | boolean | ❌ | Respecter les frontières des nœuds AST (défaut: true) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `chunks` | array | Segments de code découpés avec leurs frontières AST |
| `chunk_count` | integer | Nombre de chunks produits |
| `boundaries` | array | Positions de début/fin de chaque chunk dans le fichier |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin fichier

```
→ Confirmer que file_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier sur ENV2
```

### Étape 2 — Découpage AST

```
→ Charger le parseur Tree-sitter pour le langage spécifié
→ Parser le fichier et identifier les nœuds AST
→ Découper le fichier en chunks respectant les frontières des nœuds
→ Limiter chaque chunk à max_chunk_size si spécifié
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 des chunks produits
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune modification n'a été apportée au fichier source
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Couper un fichier au milieu d'une fonction ou d'une classe (violation des frontières AST)
- ❌ Charger le fichier entier en mémoire avant le découpage
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
