---
name: sqlite-vec
description: Recherche vectorielle embarquée dans SQLite — extension C sans dépendance externe pour requêtes de similarité vectorielle dans des tables virtuelles vec0. Pattern inspiré de https://github.com/asg017/sqlite-vec
version: 1.0.0
intent_hash: 0xSKILL_SQLITE_VEC_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/asg017/sqlite-vec
source_url: https://github.com/asg017/sqlite-vec
path: sqlite-vec
---

# sqlite-vec — Skill KiloCode

## Objectif

Fournir une recherche vectorielle embarquée dans SQLite via une extension C sans dépendance externe, supportant les requêtes de similarité vectorielle dans des tables virtuelles `vec0`. Adapté à ENV2 pour la recherche vectorielle locale légère.

## Déclencheur

Ce skill s'active quand :
- Il faut effectuer une recherche de similarité vectorielle dans SQLite
- Une extension C légère sans dépendance externe est préférée
- Des tables virtuelles `vec0` sont utilisées pour le stockage vectoriel
- L'environnement ENV2 nécessite une recherche vectorielle sans serveur externe

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite avec extension vec |
| `vec_table` | string | ✅ | Nom de la table virtuelle vec0 cible |
| `query_vector` | array | ✅ | Vektor de requête pour la recherche de similarité |
| `similarity_metric` | enum | ❌ | `cosine` / `l2` / `dot_product` (défaut: `cosine`) |
| `top_k` | integer | ❌ | Nombre de résultats les plus similaires à retourner (défaut: 10) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `similar_vectors` | array | Vektors les plus similaires avec leurs scores |
| `similarity_scores` | array | Scores de similarité pour chaque résultat |
| `top_k_returned` | integer | Nombre de résultats retournés |
| `evidence_hash` | string | Hash SHA-256 des résultats de recherche |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite avec extension vec sur ENV2
→ Vérifier que la table virtuelle vec0 existe
```

### Étape 2 — Recherche vectorielle

```
→ Charger l'extension sqlite-vec dans la session SQLite
→ Exécuter une requête de similarité vectorielle sur la table vec0
→ Retourner les top_k résultats les plus similaires
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

- ❌ Utiliser un serveur vectoriel externe (Pinecone, Weaviate, etc.) au lieu de sqlite-vec local
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Modifier la base pendant la recherche vectorielle en lecture
- ❌ Oublier le hash SHA-256 et l'horodatage UTC

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
