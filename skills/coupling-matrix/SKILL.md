---
type: skill
version: "1.0.0"
date: "2026-08-02"
intent_hash: 0xSKL005_COUPLING_MATRIX_20260802
status: active
---

# Skill: SKL005 — Coupling Matrix 16×16 (ADMG/TALEX)

## Purpose
Manages the 16×16 narrative domain coupling matrix, expanded to 81×81 for PRIMUS matrix runner. Represents causal coupling strengths between 16 narrative domains (characters, locations, themes, factions, etc.).

## Context
TALEX narratives operate across 16 semantic domains. The coupling matrix encodes how strongly each domain influences others, used by Causal Engine (SKL001) for hypothesis generation and by Generation Engine (SKL003) for coherent narrative flow.

## 16 Narrative Domains

| Index | Domain | Description |
|-------|--------|-------------|
| 0 | **Protagonist** | Main character agency |
| 1 | **Antagonist** | Opposition force |
| 2 | **Ally** | Supporting characters |
| 3 | **Neutral** | Bystanders, civilians |
| 4 | **Location: Home** | Safe/known spaces |
| 5 | **Location: Away** | Unknown/dangerous spaces |
| 6 | **Location: Threshold** | Transitional spaces |
| 7 | **Theme: Truth** | Revelation, investigation |
| 8 | **Theme: Deception** | Lies, secrets, masks |
| 9 | **Theme: Power** | Control, authority |
| 10 | **Theme: Loss** | Grief, sacrifice |
| 11 | **Faction: Law** | Official authority |
| 12 | **Faction: Crime** | Underground, illicit |
| 13 | **Faction: Secret** | Hidden societies |
| 14 | **Time: Past** | Backstory, memory |
| 15 | **Time: Future** | Prophecy, consequence |

## Matrix Structure

### 16×16 Base Matrix (Float [-1, 1])
```
coupling[i][j] = influence of domain i on domain j
-1.0 = strong negative coupling (suppresses)
 0.0 = no coupling
+1.0 = strong positive coupling (amplifies)
```

### 81×81 Expanded Matrix (Ternary)
Via `create_coupling_matrix()`:
- Each 16×16 cell → 5×5 block in 81×81
- Float → Trit: POS (>0.33), ZERO (-0.33 to 0.33), NEG (<-0.33)
- Used directly by `SparseRolling` for O(nnz) matrix-vector product

## PRIMUS Integration

```python
from src.primus.core import (
    TernaryMatrix, SparseRolling, WaveArray,
    create_coupling_matrix, Trit
)

# Example: Victorian detective coupling matrix
base_16x16 = [
    # Proto  Antag  Ally  Neut  Home  Away  Thresh Truth Decep Power Loss Law  Crime Secret Past  Fut
    [ 0.0, -0.8,  0.6,  0.1,  0.3, -0.2,  0.4,  0.7, -0.5,  0.2, -0.3,  0.4, -0.6,  0.1,  0.5,  0.2],  # Protagonist
    [-0.7,  0.0, -0.5, -0.1, -0.3,  0.4, -0.2, -0.6,  0.8, -0.4,  0.5, -0.5,  0.7, -0.3, -0.4, -0.2],  # Antagonist
    [ 0.5, -0.4,  0.0,  0.2,  0.4, -0.1,  0.3,  0.5, -0.3,  0.1, -0.2,  0.3, -0.4,  0.2,  0.3,  0.1],  # Ally
    [ 0.1, -0.1,  0.2,  0.0,  0.1,  0.0,  0.1,  0.1, -0.1,  0.0,  0.0,  0.1, -0.1,  0.0,  0.1,  0.0],  # Neutral
    [ 0.3, -0.3,  0.4,  0.1,  0.0, -0.5,  0.6,  0.2, -0.2,  0.1, -0.4,  0.2, -0.3,  0.1,  0.4,  0.1],  # Home
    [-0.2,  0.4, -0.1,  0.0, -0.5,  0.0,  0.5, -0.3,  0.4, -0.2,  0.3, -0.3,  0.5, -0.2, -0.1, -0.2],  # Away
    [ 0.4, -0.2,  0.3,  0.1,  0.6,  0.5,  0.0,  0.4, -0.3,  0.2, -0.1,  0.3, -0.4,  0.3,  0.3,  0.4],  # Threshold
    [ 0.7, -0.6,  0.5,  0.1,  0.2, -0.3,  0.4,  0.0, -0.7,  0.5, -0.4,  0.5, -0.6,  0.3,  0.6,  0.4],  # Truth
    [-0.5,  0.8, -0.3, -0.1, -0.2,  0.4, -0.3, -0.7,  0.0, -0.5,  0.6, -0.4,  0.7, -0.5, -0.4, -0.3],  # Deception
    [ 0.2, -0.4,  0.1,  0.0,  0.1, -0.2,  0.2,  0.5, -0.5,  0.0, -0.6,  0.3, -0.4,  0.2,  0.3,  0.5],  # Power
    [-0.3,  0.5, -0.2,  0.0, -0.4,  0.3, -0.1, -0.4,  0.6, -0.6,  0.0, -0.5,  0.4, -0.3, -0.5,  0.7],  # Loss
    [ 0.4, -0.5,  0.3,  0.1,  0.2, -0.3,  0.3,  0.5, -0.4,  0.3, -0.5,  0.0, -0.6,  0.2,  0.4,  0.2],  # Law
    [-0.6,  0.7, -0.4, -0.1, -0.3,  0.5, -0.4, -0.6,  0.7, -0.4,  0.4, -0.6,  0.0, -0.4, -0.5, -0.3],  # Crime
    [ 0.1, -0.3,  0.2,  0.0,  0.1, -0.2,  0.3,  0.3, -0.5,  0.2, -0.3,  0.2, -0.4,  0.0,  0.3,  0.4],  # Secret
    [ 0.5, -0.4,  0.3,  0.1,  0.4, -0.1,  0.3,  0.6, -0.4,  0.3, -0.5,  0.4, -0.5,  0.3,  0.0,  0.6],  # Past
    [ 0.2, -0.2,  0.1,  0.0,  0.1, -0.2,  0.4,  0.4, -0.3,  0.5,  0.7,  0.2, -0.3,  0.4,  0.6,  0.0],  # Future
]

# Expand to 81×81 ternary matrix
ternary_matrix = create_coupling_matrix(base_16x16)

# Create sparse version for fast computation
sparse = SparseRolling.from_matrix(ternary_matrix)

# Apply to narrative state vector
state_vector = WaveArray.from_trits(narrative_trits)  # 81 trits
influenced = sparse.matvec(state_vector)
```

## Domain Queries

```python
def get_domain_influence(matrix: TernaryMatrix, domain: int) -> list[Trit]:
    """Get row: how domain influences others."""
    return matrix.row(domain)

def get_domain_susceptibility(matrix: TernaryMatrix, domain: int) -> list[Trit]:
    """Get column: how others influence domain."""
    return matrix.col(domain)

def get_mutual_coupling(matrix: TernaryMatrix, d1: int, d2: int) -> tuple[Trit, Trit]:
    """Get bidirectional coupling between two domains."""
    return (matrix.get(d1, d2), matrix.get(d2, d1))
```

## Dynamic Coupling Updates

```python
def update_coupling(matrix: TernaryMatrix, d1: int, d2: int, value: float):
    """Update coupling from narrative events."""
    trit = Trit.from_int(int(value * 2))  # [-1,1] -> {-1,0,1}
    if trit != Trit.ZERO:
        # Update 5×5 block
        block = 5
        for i in range(block):
            for j in range(block):
                r, c = d1*block + i, d2*block + j
                if r < 81 and c < 81:
                    matrix.set(r, c, trit)
```

## Build Requirements
- Python 3.10+
- PRIMUS core: matrix, types, ternary_ops
- Base 16×16 matrix (JSON/config)

## Validation

```python
from src.primus.core import TernaryMatrix, SparseRolling, create_coupling_matrix, WaveArray, Trit

base = [[0.0]*16 for _ in range(16)]
base[0][1] = -0.8  # Protagonist suppresses Antagonist
base[1][0] = -0.7  # Antagonist suppresses Protagonist

m = create_coupling_matrix(base)
assert m.get(0, 5) == Trit.NEG    # Block (0,1) -> NEG
assert m.get(5, 0) == Trit.NEG    # Block (1,0) -> NEG

sparse = SparseRolling.from_matrix(m)
v = WaveArray.zeros()
v.waves[0] = Wave(band=FrequencyBand.ALPHA, trit=Trit.POS)
result = sparse.matvec(v)
# Result should have NEG in antagonist block
```

## Anti-patterns
- Using raw 16×16 without expansion (dimension mismatch)
- Ignoring block structure (5×5 blocks must align)
- Hardcoding values (load from narrative analysis)
- Not using sparse version (81×81 dense is slow)

## References
- PRD-MOC-INVENTORY-SYNTHESIS.md (SKL005)
- PRIMUS core: matrix, types, sparse_rolling
- SKL001 (Causal Engine) consumer
- SKL003 (Generation Engine) consumer
- TALEX 16-domain taxonomy