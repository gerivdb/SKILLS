---
name: moe-router
version: "1.0.0"
type: engine
domain: engines
status: active
author: gerivdb
license: MIT
created: "2026-06-17"
updated: "2026-06-17"
phi_weight: 0.013
intent_hash: 0xSKILLS_ENGINE_MOE_ROUTER_20260617
source_engine: CTULU/src/moe_router_intelligence
api_endpoint: ctulu:8080/engines/moe-router
triggers:
  - moe-router
  - routing intelligence
  - gate routing
  - jepa
  - energy-trit
  - dispatch engine
consumes_from:
  - ecosystem-principles
provides_to:
  - CITIZENS
  - BRAIN
  - WAZAA
---

# moe-router

Engine de routage intelligent CTULU (Mixture-of-Experts).
GATE-0->4, JEPA scoring, energy-trit.
C'est le cerveau de dispatch de l'ecosysteme : decide quel engine
consommer pour un payload donne.

## Interface

```python
from ctulu.engines import moe_router
route = moe_router.resolve(
    intent="solve_kinematics",
    context=citizen_context,
    energy_budget=0.8
)
# route: RouteResult(engine_id, confidence, gate_passed, trit_score)
```

## Relation avec CITIZENS/algorithms/router.py

moe-router est l'engine sous-jacent que router.py appelle.
CITIZENS fournit la topologie (qui peut faire quoi),
moe-router fournit la decision optimale (qui doit le faire).

## Overrides citizen.yaml

```yaml
skills:
  - id: moe-router
    source: gerivdb/SKILLS/native/engines/moe-router
    overrides:
      gate_level: 2
      energy_budget: 0.9
      trit_mode: conservative
```

## Conformite

[CONFORME_NEXUS] | strate L2_COMPOSITION | lien CITIZENS router.py
