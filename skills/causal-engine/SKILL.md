---
type: skill
version: "1.0.0"
date: "2026-08-02"
intent_hash: 0xSKL001_CAUSAL_ENGINE_20260802
status: active
---

# Skill: SKL001 — Causal Engine (ADMG/TALEX)

## Purpose
Implements the core causal inference engine for TALEX narratives. Operates on base-243 ternary logic (3^5) to compute causal relationships between narrative events, generate hypothesis chains, and validate causal coherence across 16×16 coupling matrix.

## Context
TALEX (Ternary Adaptive Logic Engine) requires a causal engine that can:
- Encode narrative events as ternary vectors (243 trits)
- Compute causal adjacency via ternary matrix operations
- Generate and validate hypothesis chains (Clue → Hypothesis → Validation)
- Interface with PRIMUS core (TernaryMatrix, SparseRolling, TernaryState)

## Kernel Components

### 1. Causal Event Encoder
- Input: Natural language event description
- Process: Hash → 243 trits via `ternary_hash_to_intent_hash`
- Output: `WaveArray` (81 slots) for matrix runner

### 2. Causal Adjacency Matrix
- 16×16 coupling matrix expanded to 81×81 via `create_coupling_matrix`
- Represents causal strength between narrative domains
- Operates via `SparseRolling` for O(nnz) performance

### 3. Hypothesis Chain Generator
- Forward chaining: Event → possible causes → hypotheses
- Backward chaining: Hypothesis → required evidence → validation
- Uses ternary logic gates (Kleene K3) for uncertainty propagation

### 4. Coherence Validator
- Computes ternary hash of full narrative state
- Validates against IntentHash (locks artifact)
- Detects causal cycles and contradictions

## PRIMUS Integration

```python
from src.primus.core import (
    TernaryMatrix, SparseRolling, WaveArray,
    ternary_hash_to_intent_hash, validate_intent_hash,
    TernaryState, TernaryStateMachine,
    create_matrix_step, create_verify_hash, create_commit,
    StatePhase
)

# Build causal adjacency from coupling data
coupling = [[0.0]*16 for _ in range(16)]
# ... populate from narrative analysis ...
adjacency = create_coupling_matrix(coupling)
sparse = SparseRolling.from_matrix(adjacency)

# State machine for causal inference
state = TernaryState.zero(b"causal_inference")
sm = TernaryStateMachine(state)
```

## TALEX NarrativeEvent Mapping

| Narrative Concept | Ternary Representation |
|-------------------|------------------------|
| Event (Clue) | WaveArray (81 trits) |
| Hypothesis | WaveArray + confidence trit |
| Causal Link | Matrix entry (POS/NEG/ZERO) |
| Narrative State | TernaryState (3×81 + phase) |
| Validation | IntentHash (243 trits) |

## BATVERSE Operators Used

From `TernaryGates` (Kleene K3 logic):
- `implies(a, b)` — Causal implication
- `equiv(a, b)` — Bidirectional causality
- `mux(cond, a, b)` — Conditional branching
- `and_k3 / or_k3` — Conjunction/disjunction with uncertainty

## Build Requirements
- Python 3.10+ (for PRIMUS core)
- PRIMUS core installed (`src/primus/core/`)
- No Zig compilation needed (pure Python)

## Validation

```python
# Test causal encoding
from src.primus.core import ternary_hash_to_intent_hash
event = "The artifact was stolen at midnight"
hash_val = ternary_hash_to_intent_hash(event)
assert validate_intent_hash(hash_val)

# Test causal step
from src.primus.core import TernaryMatrix, SparseRolling, WaveArray
matrix = TernaryMatrix.identity()
vector = WaveArray.zeros()
result = matrix.matvec(vector)
assert result.to_trits().count(Trit.ZERO) == 81
```

## Anti-patterns
- Using boolean logic instead of Kleene K3 (loses uncertainty)
- Skipping IntentHash validation (narrative can drift)
- Hardcoding coupling matrix (must be learned/derived)
- Ignoring phase transitions in TernaryStateMachine

## References
- PRD-MOC-INVENTORY-SYNTHESIS.md (SKL001)
- PRIMUS core: types, matrix, ternary_ops, hash, state
- TALEX architecture (ADMG v19.2)
- BATVERSE 7 operators
- IntentHash specification (base 243 = 3^5)