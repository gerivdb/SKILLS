---
name: causal-chain
version: "1.0.0"
type: engine
domain: engines
status: active
author: gerivdb
license: MIT
created: "2026-06-17"
updated: "2026-06-17"
phi_weight: 0.012
intent_hash: 0xSKILLS_ENGINE_CAUSAL_CHAIN_20260617
source_engine: CTULU/src/causal_chain_orchestrator
api_endpoint: ctulu:8080/engines/causal-chain
triggers:
  - causal-chain
  - cause drift resolve
  - causal dag
  - counterfactual
  - intervention
  - notears
  - lingam
  - fci
consumes_from:
  - ecosystem-principles
provides_to:
  - CAPTA-4D
  - TINA
  - BRAIN
---

# causal-chain

Engine de causalite base sur CTULU/causal_chain_orchestrator.
Impl: NOTEARS, FCI, LiNGAM + DoWhy Pearl L1-L3.
Produit des DAGs de contraintes consommables par tout citizen.

## Interface

```python
# Invoke via CITIZENS router
from ctulu.engines import causal_chain
result = causal_chain.run(
    data=df,
    config={"max_joints": 8, "rope_model": "catenary"}  # overrides citizen
)
# result: DAGResult(nodes, edges, phi_score, interventions)
```

## Overrides citizen.yaml

```yaml
skills:
  - id: causal-chain
    source: gerivdb/SKILLS/native/engines/causal-chain
    overrides:
      max_joints: 8
      rope_model: catenary
      max_iter: 500
```

## Capacites

- Inference causale (cause -> drift -> resolve)
- Contrefactuels et interventions Pearl
- Production de DAGs JSON/YAML vers NEXUS
- Gate phi-CPS >= 4.559 avant promotion

## Conformite

[CONFORME_NEXUS] | strate L2_CAUSAL_ENGINE | consomme depuis TINA
