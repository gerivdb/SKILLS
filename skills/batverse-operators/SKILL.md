---
type: skill
version: "1.0.0"
date: "2026-08-02"
intent_hash: 0xSKL004_BATVERSE_OPERATORS_20260802
status: active
---

# Skill: SKL004 — BATVERSE 7 Operators (ADMG/TALEX)

## Purpose
Implements the 7 fundamental BATVERSE narrative operators as ternary logic gates. These operators form the computational basis for TALEX narrative manipulation, operating on base-243 ternary states.

## Context
BATVERSE defines 7 primitive operators for narrative transformation. Each maps to a ternary gate in Kleene K3 logic, enabling composition of complex narrative operations from atomic ternary transformations.

## The 7 BATVERSE Operators

| # | Operator | Symbol | Ternary Gate | Description |
|---|----------|--------|--------------|-------------|
| 1 | **INVERT** | ¬ | `not_k3` | Polarity inversion (truth ↔ falsehood) |
| 2 | **CONJOIN** | ∧ | `and_k3` | Causal conjunction (both must hold) |
| 3 | **DISJOIN** | ∨ | `or_k3` | Alternative causality (either holds) |
| 4 | **IMPLY** | → | `implies` | Causal implication (if A then B) |
| 5 | **EQUIV** | ↔ | `equiv` | Bidirectional causality (A iff B) |
| 6 | **SELECT** | ? : | `mux` | Conditional narrative branching |
| 7 | **SPLIT** | ⇢ | `demux` | Narrative fork (one input → two paths) |

## PRIMUS Integration

```python
from src.primus.core import Trit, TernaryGates, WaveArray, TernaryOps

# All operators available via TernaryGates (Kleene K3)
# Boolean variants also available for definite logic

# Operator 1: INVERT
def op_invert(a: Trit) -> Trit:
    return TernaryGates.not_k3(a)

# Operator 2: CONJOIN
def op_conjoin(a: Trit, b: Trit) -> Trit:
    return TernaryGates.and_k3(a, b)

# Operator 3: DISJOIN
def op_disjoin(a: Trit, b: Trit) -> Trit:
    return TernaryGates.or_k3(a, b)

# Operator 4: IMPLY
def op_imply(a: Trit, b: Trit) -> Trit:
    return TernaryGates.implies(a, b)

# Operator 5: EQUIV
def op_equiv(a: Trit, b: Trit) -> Trit:
    return TernaryGates.equiv(a, b)

# Operator 6: SELECT (Multiplexer)
def op_select(cond: Trit, a: Trit, b: Trit) -> Trit:
    return TernaryGates.mux(cond, a, b)

# Operator 7: SPLIT (Demultiplexer)
def op_split(val: Trit, sel: Trit) -> tuple[Trit, Trit]:
    return TernaryGates.demux(val, sel)

# Vectorized versions via TernaryOps
def op_vector_invert(arr: WaveArray) -> WaveArray:
    return TernaryOps.not_op(arr)

def op_vector_conjoin(a: WaveArray, b: WaveArray) -> WaveArray:
    return TernaryOps.and_op(a, b)

def op_vector_imply(a: WaveArray, b: WaveArray) -> WaveArray:
    # implies(a,b) = (NOT a) OR b
    return TernaryOps.or_op(TernaryOps.not_op(a), b)
```

## Composition Examples

### Causal Chain Construction
```python
# Event A implies Event B, which implies Event C
# Chain: A → B → C
chain = op_imply(event_a, op_imply(event_b, event_c))
# Equivalent: (¬A ∨ (¬B ∨ C))
```

### Narrative Branching
```python
# If clue_found then investigation_path else dead_end
path = op_select(clue_found, investigation_path, dead_end)
```

### Contradiction Detection
```python
# A and ¬A cannot both be true
contradiction = op_conjoin(proposition, op_invert(proposition))
# Result: ZERO (unknown) in K3, not NEG (false)
```

## Truth Tables (Kleene K3)

| A | B | ¬A | A∧B | A∨B | A→B | A↔B |
|---|---|----|-----|-----|-----|-----|
| T | T | F  | T   | T   | T   | T   |
| T | U | F  | U   | T   | U   | U   |
| T | F | F  | F   | T   | F   | F   |
| U | T | U  | U   | T   | T   | U   |
| U | U | U  | U   | U   | U   | U   |
| U | F | U  | F   | U   | T   | F   |
| F | T | T  | F   | T   | T   | F   |
| F | U | T  | F   | U   | T   | U   |
| F | F | T  | F   | F   | T   | T   |

T=POS, F=NEG, U=ZERO

## Build Requirements
- Python 3.10+
- PRIMUS core: `ternary_ops.TernaryGates`
- No external dependencies

## Validation

```python
from src.primus.core import Trit, TernaryGates

# Test all 7 operators
a, b = Trit.POS, Trit.NEG

assert TernaryGates.not_k3(a) == Trit.NEG          # INVERT
assert TernaryGates.and_k3(a, b) == Trit.NEG       # CONJOIN
assert TernaryGates.or_k3(a, b) == Trit.POS        # DISJOIN
assert TernaryGates.implies(a, b) == Trit.NEG      # IMPLY
assert TernaryGates.equiv(a, b) == Trit.NEG        # EQUIV
assert TernaryGates.mux(Trit.POS, a, b) == a       # SELECT (cond=POS)
assert TernaryGates.demux(a, Trit.POS) == (a, Trit.ZERO)  # SPLIT

print("All 7 BATVERSE operators verified!")
```

## Anti-patterns
- Using boolean logic (loses ZERO/uncertainty)
- Composing without parentheses (ternary ops not fully associative)
- Ignoring K3 semantics (ZERO propagates differently than FALSE)
- Hardcoding truth tables (use TernaryGates)

## References
- PRD-MOC-INVENTORY-SYNTHESIS.md (SKL004)
- PRIMUS core: ternary_ops.TernaryGates
- BATVERSE operator specification
- Kleene K3 logic
- TALEX narrative algebra