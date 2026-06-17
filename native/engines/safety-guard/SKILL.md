---
name: safety-guard
version: "1.0.0"
type: engine
domain: engines
status: active
author: gerivdb
license: MIT
created: "2026-06-17"
updated: "2026-06-17"
phi_weight: 0.015
intent_hash: 0xSKILLS_ENGINE_SAFETY_GUARD_20260617
source_engine: GOVERNANCE-HUB/rules
api_endpoint: ctulu:8080/engines/safety-guard
triggers:
  - safety-guard
  - phi-cps validation
  - governance rules
  - garde-fous
  - safety validate
consumes_from:
  - ecosystem-principles
provides_to:
  - "*"  # tout citizen l'instancie
---

# safety-guard

Engine de validation de securite et gouvernance.
Source: GOVERNANCE-HUB/rules + phi-CPS >= 4.559.
C'est le seul engine instancie par TOUS les citizens sans exception.

## Interface

```python
from ctulu.engines import safety_guard
result = safety_guard.validate(
    payload=action_payload,
    citizen_id="CAPTA-4D",
    phi_threshold=4.559
)
# result: SafetyResult(valid, phi_score, violations, hitl_required)
```

## Niveaux de validation

| Niveau | Declencheur | Action |
|--------|-------------|--------|
| L0 | phi < 4.559 | BLOCK + HITL obligatoire |
| L1 | drift > 0.8 | WARN + log WAL |
| L2 | schema invalide | REJECT + raison |
| L3 | encoding non-ASCII | GATE-6 triggered |

## Overrides citizen.yaml

```yaml
skills:
  - id: safety-guard
    source: gerivdb/SKILLS/native/engines/safety-guard
    overrides:
      phi_threshold: 4.559  # ne pas baisser
      hitl_on_block: true
      log_level: WAL
```

## Conformite

[CONFORME_NEXUS] | strate L0_CONSTITUTIONAL | phi-CPS souverain
