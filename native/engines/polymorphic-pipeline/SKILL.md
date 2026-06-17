---
name: polymorphic-pipeline
version: "1.0.0"
type: engine
domain: engines
status: active
author: gerivdb
license: MIT
created: "2026-06-17"
updated: "2026-06-17"
phi_weight: 0.011
intent_hash: 0xSKILLS_ENGINE_POLYMORPHIC_20260617
source_engine: CTULU/src/polymorphic_pipeline
api_endpoint: ctulu:8080/engines/polymorphic-pipeline
triggers:
  - polymorphic-pipeline
  - oae
  - pipeline modes
  - L0 L9 pipeline
  - multi-mode orchestration
consumes_from:
  - ecosystem-principles
provides_to:
  - BRAIN
  - AUTO-DEV
  - CAPTA-4D
---

# polymorphic-pipeline

Engine de composition polymorphique CTULU OAE v2.
8 modes de traitement, couverture L0->L9 du metacluster.

## Interface

```python
from ctulu.engines import polymorphic_pipeline
result = polymorphic_pipeline.run(
    payload=data,
    mode="kinematic",  # l'un des 8 modes OAE
    layer="L3"         # strate cible
)
```

## Modes disponibles (OAE v2)

| Mode | Usage typique |
|------|---------------|
| causal | Inference DAG |
| kinematic | Geometrie cables / spatial |
| narrative | Moteur recit vibe-loop |
| ontology | Sync semantique |
| safety | Validation garde-fous |
| profile | Matching citizens |
| governance | ADR + phi-CPS |
| raw | Pass-through debug |

## Overrides citizen.yaml

```yaml
skills:
  - id: polymorphic-pipeline
    source: gerivdb/SKILLS/native/engines/polymorphic-pipeline
    overrides:
      mode: kinematic
      layer: L3
```

## Conformite

[CONFORME_NEXUS] | strate L2_COMPOSITION
