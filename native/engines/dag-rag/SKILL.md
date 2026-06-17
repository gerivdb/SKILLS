---
name: dag-rag
version: "1.0.0"
type: engine
domain: engines
status: active
author: gerivdb
license: MIT
created: "2026-06-17"
updated: "2026-06-17"
phi_weight: 0.010
intent_hash: 0xSKILLS_ENGINE_DAG_RAG_20260617
source_engine: CTULU/src/epic_074_dag_rag
api_endpoint: ctulu:8080/engines/dag-rag
triggers:
  - dag-rag
  - dag traversal
  - rag
  - kv cache
  - retrieval augmented
  - epic 074
consumes_from:
  - semantic-search
  - embedding
provides_to:
  - BRAIN
  - MIMIR
  - NEXUS
---

# dag-rag

Engine de traversal DAG avec RAG integre (CTULU epic_074).
KV cache 3600s. Combine navigation structuree du DAG + retrieval
semantique pour contexte enrichi.

## Interface

```python
from ctulu.engines import dag_rag
result = dag_rag.run(
    query="contraintes cable scene X",
    dag=nexus_dag,
    cache_ttl=3600
)
# result: RAGResult(nodes_traversed, chunks, score)
```

## Overrides citizen.yaml

```yaml
skills:
  - id: dag-rag
    source: gerivdb/SKILLS/native/engines/dag-rag
    overrides:
      cache_ttl: 7200
      top_k: 5
      dag_source: NEXUS
```

## Conformite

[CONFORME_NEXUS] | strate L2_COMPOSITION | KV cache souverain
