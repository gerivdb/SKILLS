---
type: skill
version: "1.0.0"
date: "2026-08-02"
intent_hash: 0xSKL003_GENERATION_ENGINE_20260802
status: active
---

# Skill: SKL003 - Generation Engine (ADMG/TALEX)

## Purpose
Generates narrative content (events, dialogue, descriptions) from ternary state using causal chains and lore constraints. Operates as a ternary-state-driven generator that produces coherent narrative sequences locked by IntentHash.

## Context
TALEX needs to generate narrative from causal hypotheses. The Generation Engine takes a validated causal chain and lore-compliant state, then produces natural language output while maintaining ternary coherence.

## Kernel Components

### 1. Ternary State -> Text Decoder
- Input: `TernaryState` (vector + memory + program, 3x81 trits)
- Process: Each WaveArray slot -> token via frequency-band vocabulary
- Output: Token sequence with ternary metadata

### 2. Causal Chain Narrativizer
- Input: Validated hypothesis chain (Event -> Cause -> Effect)
- Process: Map ternary causal links to narrative beats
- Output: Structured narrative beats with ternary anchors

### 3. Lore-Compliant Generator
- Constrained by Lore Validator (SKL002) rules
- Uses `TernaryGates.mux()` for conditional generation
- Rejects generations that produce lore violations

### 4. IntentHash Anchor
- Every generated segment gets IntentHash
- Enables verification: `regenerate(state) == original_hash`
- Supports deterministic regeneration for testing

## PRIMUS Integration

```python
from src.primus.core import (
    TernaryState, WaveArray, FrequencyBand, Trit,
    TernaryGates, ternary_hash_to_intent_hash, validate_intent_hash
)

# Generation from ternary state
def generate_from_state(state: TernaryState, max_tokens: int = 256) -> str:
    tokens = []
    for i, wave in enumerate(state.vector.waves):
        if wave.trit == Trit.ZERO:
            continue
        # Decode slot via frequency band vocabulary
        token = decode_slot(i, wave.band, wave.trit)
        tokens.append(token)
        
        # Conditional generation via mux
        if wave.trit == Trit.NEG:
            token = TernaryGates.mux(wave.trit, negation_token, token)
    
    text = " ".join(tokens[:max_tokens])
    intent_hash = ternary_hash_to_intent_hash(f"generation:{text}:{state.hash_state().hex()}")
    return text, intent_hash

def decode_slot(slot: int, band: FrequencyBand, trit: Trit) -> str:
    # Vocabulary mapping (slot x band x trit -> token)
    vocab = {
        (0, FrequencyBand.ALPHA, Trit.POS): "The detective",
        (1, FrequencyBand.BETA, Trit.POS): "observed",
        (2, FrequencyBand.THETA, Trit.POS): "a clue",
        # ... full vocabulary 81x5x3
    }
    return vocab.get((slot, band, trit), f"[slot{slot}]")
```

## Generation Pipeline

```
TernaryState (3x81 trits)
        |
        |----> Vector (current focus) --> Token decoder -->
        |----> Memory (context) ----------> Context injector --> Combined tokens
        `----> Program (generation rules) --> Rule applier -->
                        |
                        v
            Lore Validator (SKL002) check
                        |
                        |---- VIOLATION -> Regenerate with constraints
                        |
                        `---- PASS --> Final text + IntentHash
```

## Narrative Modes

| Mode | Vector Source | Memory Depth | Program Type |
|------|---------------|--------------|--------------|
| **Scene** | Current event | 3 beats | Descriptive |
| **Dialogue** | Character state | 5 exchanges | Conversational |
| **Exposition** | World state | Full history | Explanatory |
| **Action** | Causal chain | Immediate | Imperative |

## Deterministic Regeneration

```python
# Same state + same generator version = identical output
state = TernaryState.from_intent(b"scene:detective_office:rain")
text1, hash1 = generate_from_state(state)
text2, hash2 = generate_from_state(state)
assert text1 == text2
assert hash1 == hash2
assert validate_intent_hash(hash1)
```

## Build Requirements
- Python 3.10+
- PRIMUS core
- Vocabulary database (slot x band x trit -> token)
- Lore Validator (SKL002) for constraint checking

## Validation

```python
# Test deterministic generation
from src.primus.core import TernaryState, WaveArray, FrequencyBand, Trit
state = TernaryState.from_intent(b"test_generation")
state = state.with_vector(WaveArray.from_trits([
    Trit.POS if i == 0 else Trit.ZERO for i in range(81)
]))
text, intent_hash = generate_from_state(state)
assert "The detective" in text
assert validate_intent_hash(intent_hash)
```

## Anti-patterns
- Non-deterministic generation (breaks IntentHash verification)
- Skipping lore validation (produces invalid narrative)
- Ignoring memory/context (incoherent output)
- Hardcoding templates (use ternary-driven generation)

## References
- PRD-MOC-INVENTORY-SYNTHESIS.md (SKL003)
- PRIMUS core: types, state, hash, ternary_ops (TernaryGates)
- SKL002 (Lore Validator) for constraints
- TALEX narrative architecture
- IntentHash specification