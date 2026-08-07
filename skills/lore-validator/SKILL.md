---
type: skill
version: "1.0.0"
date: "2026-08-02"
intent_hash: 0xSKL002_LORE_VALIDATOR_20260802
status: active
---

# Skill: SKL002 — Lore Validator (ADMG/TALEX)

## Purpose
Validates narrative lore consistency against Victorian-era canon (or any defined lore corpus). Uses ternary logic to represent lore rules as constraints, computes satisfaction via ternary matrix operations, and produces validation reports with IntentHash locking.

## Context
TALEX narratives must maintain coherence with established lore (Victorian London, BATVERSE mythology, etc.). The Lore Validator encodes lore rules as ternary constraints and checks narrative events against them.

## Kernel Components

### 1. Lore Rule Encoder
- Input: Lore rules (natural language or structured)
- Process: Each rule → ternary constraint vector (243 trits)
- Storage: Rule registry as `WaveArray` collection

### 2. Constraint Matrix
- 81×81 matrix where M[i,j] = rule i constrains slot j
- Values: POS (requires), NEG (forbids), ZERO (neutral)
- Built via `TernaryMatrix.from_trits()`

### 3. Validation Engine
- For each narrative event (WaveArray):
  - Compute `result = constraint_matrix @ event_vector`
  - Check for NEG results (violations)
  - Accumulate POS confirmations (supporting evidence)

### 4. Victorian Canon Adapter
- Pre-encoded Victorian era rules (1837-1901):
  - Technology constraints (no electricity, no phones)
  - Social constraints (class, gender, etiquette)
  - Geographic constraints (London fog, gaslight districts)
  - Supernatural constraints (BATVERSE mythology)

## PRIMUS Integration

```python
from src.primus.core import (
    TernaryMatrix, WaveArray, Trit,
    TernaryGates, ternary_hash_to_intent_hash
)

# Lore rule: "No electric light in 1880s London"
# Encodes as: slot_47 (electricity) = NEG when period=VICTORIAN
victorian_rules = [
    (47, Trit.NEG),  # No electricity
    (12, Trit.NEG),  # No telephone
    (33, Trit.POS),  # Gaslight required
    (58, Trit.POS),  # Horse carriage transport
]

# Build constraint matrix
constraint_matrix = TernaryMatrix.zeros()
for slot, value in victorian_rules:
    constraint_matrix.set(slot, slot, value)

# Validate event
event = WaveArray.from_trits(event_trits)  # 81 trits
violations = constraint_matrix.matvec(event)
# Check for NEG in violations -> lore violation
```

## Validation Pipeline

```
Narrative Event (81 trits)
        │
        ▼
Constraint Matrix (81×81)
        │
        ▼
Matrix-Vector Product (SparseRolling)
        │
        ▼
Violation Check: any(trit == NEG)
        │
        ├── YES → LoreViolation(details, intent_hash)
        │
        └── NO  → Valid + SupportingEvidence(count_POS)
```

## IntentHash Locking

Every validation produces an IntentHash:
```python
validation_hash = ternary_hash_to_intent_hash(
    f"lore_validation:{event_hash}:{constraint_set_hash}"
)
```
This locks the validation result to the specific lore version.

## Build Requirements
- Python 3.10+
- PRIMUS core (`src/primus/core/`)
- Lore corpus (JSON/YAML) for rule extraction

## Validation

```python
# Test Victorian constraint
from src.primus.core import TernaryMatrix, WaveArray, Trit
matrix = TernaryMatrix.zeros()
matrix.set(47, 47, Trit.NEG)  # No electricity
event = WaveArray.zeros()
event.waves[47] = Wave(band=FrequencyBand.ALPHA, trit=Trit.POS)
result = matrix.matvec(event)
assert result.waves[47].trit == Trit.NEG  # Violation detected
```

## Anti-patterns
- Boolean validation (loses "unknown/uncertain" = ZERO)
- Hardcoding rules in code (use external lore corpus)
- Not hashing validation results (no audit trail)
- Ignoring FrequencyBand context (rules may be band-specific)

## References
- PRD-MOC-INVENTORY-SYNTHESIS.md (SKL002)
- PRIMUS core: types, matrix, ternary_ops (TernaryGates), hash
- Victorian canon (ADMG/TALEX lore bible)
- BATVERSE mythology constraints
- IntentHash specification