---
name: sqlite-vss
description: Extension historique de recherche vectorielle SQLite basée sur Faiss — référence d'intégration vectorielle/SQLite. Pattern inspiré de https://github.com/asg017/sqlite-vss
version: 1.0.0
intent_hash: 0xSKILL_SQLITE_VSS_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/asg017/sqlite-vss
source_url: https://github.com/asg017/sqlite-vss
path: sqlite-vss
---

# SQLite VSS — Skill KiloCode

## Objectif

Fournir une référence canonique pour sqlite-vss, extension historique de recherche vectorielle SQLite basée sur Faiss. Adapté à ENV2 pour la recherche de similarité vectorielle embarquée sans serveur externe.

## Déclencheur

Ce skill s'active quand :
- Il faut effectuer une recherche vectorielle dans SQLite
- Une extension basée sur Faiss est nécessaire pour la similarité approximée
- L'environnement ENV2 nécessite une recherche vectorielle locale sans réseau
- L'index vectoriel doit être intégré aux requêtes SQL

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `db_path` | string | ✅ | Chemin absolu vers le fichier SQLite |
| `vector_table` | string | ✅ | Nom de la table virtuelle vectorielle |
| `query_vector` | array | ✅ | Vektor de requête pour la similarité |
| `top_k` | integer | ❌ | Nombre de résultats les plus similaires (défaut: 10) |
| `distance_metric` | enum | ❌ | `l2` / `cosine` / `dot` (défaut: `l2`) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `similar_items` | array | Items les plus similaires avec leurs distances |
| `distances` | array | Distances de similarité pour chaque résultat |
| `top_k_returned` | integer | Nombre de résultats retournés |
| `evidence_hash` | string | Hash SHA-256 du résultat |

## Protocole Obligatoire

### Étape 1 — Vérification du chemin DB

```
→ Confirmer que db_path est absolu et explicite (règle explicit-path-compliance)
→ Vérifier l'existence du fichier SQLite sur ENV2
→ Vérifier que l'extension sqlite-vss est chargée
```

### Étape 2 — Recherche vectorielle

```
→ Charger l'extension sqlite-vss (basée sur Faiss)
→ Exécuter la requête de similarité sur la table vectorielle
→ Retourner les top_k résultats les plus proches
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

- ❌ Utiliser un serveur vectoriel externe (Pinecone, Weaviate) au lieu de sqlite-vss local
- ❌ Utiliser des chemins relatifs (règle explicit-path-compliance)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Négliger la contrainte mémoire ENV2 pour l'index Faiss

## Référence ADR

- **ADR** : ADR-2026-05-28-001-WSL1-RUNTIME-Z600
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
- **Règle** : slm-fragmented-approach
