---
name: keel-vdb-tql
version: "1.0.0"
description: "Indexation VDB des Thought-Commits KEEL + TQL live. Vectorise via UAE (1/√d), indexe dans VDB, execute des requêtes TQL live (~sim, path_from, .functor:, .adjoint:). Utiliser quand l'utilisateur mentionne 'TQL live', 'indexer graph KEEL', 'VDB KEEL', 'recherche similarité KEEL', 'path_from'."
triggers:
  - "TQL live"
  - "indexer graph KEEL"
  - "VDB KEEL"
  - "recherche similarité KEEL"
  - "path_from"
  - "indexer Thought-Commit"
layer: "L1_SOT"
nexusTags: ["CONFORME_NEXUS", "KEEL"]
prerequisites:
  - "gerivdb/BRAIN/src/brain/vdb/keel_indexer.py"
  - "gerivdb/BRAIN/src/brain/tql/tql_live.py"
  - "gerivdb/BRAIN/src/brain/parsers/ (parser PEG)"
  - "TAXONOMY/graph.yaml (SKILLS)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Version initiale — VDB indexation + TQL live KEEL v0.7"}
---

# KEEL-VDB-TQL — Indexation VDB + TQL live

## Domaine et périmètre

Ce skill documente l'indexation vectorielle des Thought-Commits KEEL et l'exécution de requêtes TQL live sur le graphe de dépendances.

**Implémentation de référence** : `gerivdb/BRAIN` commit `7725aff`

## Architecture

```
Thought-Commit → Parser PEG → AST → UAE Embedding (1/√d) → VDB
                                                          ↓
TQL Query → Parser TQL → VDB Query → Résultats (ranked by UAE score)
```

## API publique

```python
from vdb.keel_indexer import KeelVDBIndexer
from tql.tql_live import TQLLiveEngine

# Indexation
indexer = KeelVDBIndexer(vdb_path="data/vdb")
indexer.index_from_graph_yaml("TAXONOMY/graph.yaml")
indexer.index_thought_commit(commit_obj)

# TQL live
engine = TQLLiveEngine(indexer=indexer)
result = engine.execute("FIND ◈ WHERE ~sim:'audit governance' DEPTH T3")
results = engine.search_similar("governance", limit=10)
paths = engine.path_from("skills-agentic", max_depth=5)
```

## Requêtes TQL supportées

| Syntaxe | Description |
|---------|-------------|
| `FIND ◈ WHERE ~sim:"text" DEPTH T3` | Recherche par similarité |
| `FIND 𝔽 WHERE source_verse = "governance"` | Recherche de foncteurs |
| `FIND ◈ WHERE path_from("skill") AND cost < 0.5 DEPTH T4` | Traversée du graphe |
| `FIND 𝔹ranch WHERE .adjoint:𝔹ranch⊣𝕄erge DEPTH T3` | Recherche par adjonction |

## Schéma VDB

| Collection | Clés | Champs |
|------------|------|--------|
| `keel_thought_commits` | sha7 (PK) | scope, description, intent_hash, embedding[768], env, vague, timestamp |
| `keel_functors` | name (PK) | source_verse, target_verse, embedding, preserves_composition, preserves_identity |
| `keel_graph_edges` | source→target | functor, cost, condition |

## Sync graph.yaml ↔ VDB

```python
counters = indexer.sync_graph_yaml("TAXONOMY/graph.yaml")
# Retourne: {"indexed": N, "updated": N, "removed": N}
```

## Intégration

- **Dépôts** : BRAIN (VDB + TQL), SKILLS (graph.yaml), UAE (embedding)
- **Couche EECS** : L1_SOT
- **Skills dépendants** : keel-peg-parser (fournit l'AST à indexer)
