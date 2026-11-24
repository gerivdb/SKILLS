---
name: fts5-expose
description: Inspection interne du tokenizer FTS5 — expose fts5_tokenize() pour vérifier comment SQLite découpe les chaînes selon le tokenizer choisi. Pattern inspiré de https://github.com/FaFre/fts5_expose
version: 1.0.0
intent_hash: 0xSKILL_FTS5_EXPOSE_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/FaFre/fts5_expose
source_url: https://github.com/FaFre/fts5_expose
path: fts5-expose
---

# fts5-expose — Skill KiloCode

## Objectif

Fournir une inspection interne du tokenizer FTS5 via `fts5_tokenize()` pour vérifier comment SQLite découpe les chaînes selon le tokenizer choisi. Adapté à ENV2 pour le diagnostic et l'optimisation des index FTS5.

## Déclencheur

Ce skill s'active quand :
- Il faut inspecter le tokenizer FTS5 d'une base SQLite
- Le découpage des chaînes par le tokenizer doit être vérifié pour le diagnostic
- L'optimisation des index FTS5 est nécessaire sur ENV2
- Une compréhension interne du tokenisation est requise avant requêtage

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite avec index FTS5 |
| `tokenizer_name` | string | ❌ | Nom du tokenizer FTS5 à inspecter (défaut: default) |
| `input_string` | string | ✅ | Chaîne à tokenizer pour inspection |
| `fts5_table` | string | ❌ | Nom de la table virtuelle FTS5 cible |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `tokens` | array | Tokens produits par le tokenizer FTS5 |
| `token_positions` | array | Positions des tokens dans la chaîne d'entrée |
| `tokenizer_used` | string | Nom du tokenizer utilisé |
| `evidence_hash` | string | Hash SHA-256 de l'inspection |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite avec index FTS5 sur ENV2
```

### Étape 2 — Inspection du tokenizer

```
→ Exécuter fts5_tokenize() sur la chaîne d'entrée fournie
→ Inspecter les tokens produits et leurs positions
→ Vérifier le tokenizer utilisé par la table FTS5 cible si spécifiée
```

### Étape 3 — Preuve d'exécution

```
→ Capturer la sortie brute (stdout)
→ Calculer le hash SHA-256 des tokens inspectés
→ Enregistrer l'horodatage UTC
→ Vérifier qu'aucune écriture n'a été effectuée sur la base
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Utiliser `grep` sur des fichiers bruts au lieu d'une inspection FTS5 structurée
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Modifier la base pendant l'inspection du tokenizer
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
