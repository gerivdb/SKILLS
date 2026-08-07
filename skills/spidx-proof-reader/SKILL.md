---
type: skill
version: "1.0.0"
date: "2026-08-02"
intent_hash: 0xSKL006_SPIDX_PROOF_READER_20260802
status: active
---

# Skill: SKL006 — SPIDX Proof Reader (ADMG/TALEX)

## Purpose
Validates SPIDX (Structured Proof Index) causal rewrites for narrative coherence. Reads SPIDX documents, verifies causal chain integrity, checks IntentHash locks, and produces validation reports with ternary diagnostics.

## Context
TALEX uses SPIDX (causal proof index) to track narrative reasoning chains. Each SPIDX entry is a causal rewrite step with IntentHash anchoring. The Proof Reader ensures no logical gaps, circular dependencies, or hash mismatches exist in the proof chain.

## SPIDX Structure

```yaml
spidx_version: "1.0"
intent_hash: "0x..."           # Root intent hash
entries:
  - index: 0
    type: "clue"              # clue | hypothesis | validation | rewrite
    premise: "The letter was sealed with red wax"
    conclusion: "The sender is nobility"
    operator: "implies"       # BATVERSE operator
    confidence: 0.87          # [0,1]
    ternary_state: "..."      # 243-trit hash of state
    intent_hash: "0x..."      # Step intent hash
    dependencies: [0]         # Previous entry indices
  - index: 1
    type: "hypothesis"
    premise: "Nobility uses red wax seals"
    conclusion: "Sender is Lord Blackwood"
    operator: "equiv"
    confidence: 0.72
    ternary_state: "..."
    intent_hash: "0x..."
    dependencies: [0]
```

## Validation Checks

### 1. Causal Chain Integrity
- Every entry's dependencies must exist
- No circular dependencies (DAG check)
- Operator application valid: `premise --operator--> conclusion`

### 2. IntentHash Verification
- Each entry's `intent_hash` = `ternary_hash_to_intent_hash(premise + conclusion + operator)`
- Root `intent_hash` = hash of all entry hashes combined
- `validate_intent_hash()` must pass for all

### 3. Ternary State Consistency
- `ternary_state` must be valid 243-trit hash
- Sequential entries: `state_{n+1}` = transition(`state_n`, `entry_n`)
- Final state must match expected narrative state

### 4. Confidence Propagation
- Confidence flows through operators per K3 logic
- `implies`: min(premise_conf, conclusion_conf)
- `equiv`: min(premise_conf, conclusion_conf)
- `and_k3`: min(all_confidences)
- `or_k3`: max(all_confidences)
- Chain confidence = propagated confidence to final conclusion

### 5. Lore Compliance (SKL002 Integration)
- All conclusions checked against Lore Validator
- Violations flagged with domain and severity

## PRIMUS Integration

```python
from src.primus.core import (
    ternary_hash_to_intent_hash, validate_intent_hash,
    parse_intent_hash, TernaryGates, Trit
)

def validate_spidx_entry(entry: dict, prev_states: dict) -> tuple[bool, list[str]]:
    errors = []
    
    # 1. Check IntentHash
    content = f"{entry['premise']}|{entry['conclusion']}|{entry['operator']}"
    expected_hash = ternary_hash_to_intent_hash(content)
    if entry['intent_hash'] != expected_hash:
        errors.append(f"IntentHash mismatch: expected {expected_hash}, got {entry['intent_hash']}")
    
    # 2. Validate operator application
    op_func = getattr(TernaryGates, entry['operator'] + '_k3', None)
    if not op_func:
        errors.append(f"Unknown operator: {entry['operator']}")
    
    # 3. Check ternary state format
    try:
        trits = parse_intent_hash(entry['ternary_state'])
        if len(trits) != 243:
            errors.append(f"Invalid ternary_state length: {len(trits)} != 243")
    except Exception as e:
        errors.append(f"Invalid ternary_state: {e}")
    
    # 4. Dependency check
    for dep in entry.get('dependencies', []):
        if dep not in prev_states:
            errors.append(f"Missing dependency: {dep}")
    
    return len(errors) == 0, errors

def validate_spidx_document(spidx: dict) -> tuple[bool, dict]:
    """Full document validation."""
    report = {
        'valid': True,
        'entry_count': len(spidx.get('entries', [])),
        'errors': [],
        'warnings': [],
        'chain_confidence': 1.0,
        'lore_violations': []
    }
    
    prev_states = {}
    for entry in spidx['entries']:
        valid, errors = validate_spidx_entry(entry, prev_states)
        if not valid:
            report['valid'] = False
            report['errors'].extend(errors)
        prev_states[entry['index']] = entry
    
    # Root hash verification
    all_hashes = b''.join(bytes.fromhex(e['intent_hash'][2:]) for e in spidx['entries'])
    root_expected = ternary_hash_to_intent_hash(all_hashes)
    if spidx['intent_hash'] != root_expected:
        report['valid'] = False
        report['errors'].append(f"Root IntentHash mismatch")
    
    return report['valid'], report
```

## Validation Pipeline

```
SPIDX Document (YAML/JSON)
        │
        ▼
Parse & Structure Check
        │
        ├──► IntentHash Verification (per entry + root)
        ├──► Causal DAG Check (no cycles, deps exist)
        ├──► Operator Validity (BATVERSE 7)
        ├──► Ternary State Format (243 trits each)
        ├──► Confidence Propagation (K3 logic)
        └──► Lore Compliance (SKL002)
                    │
                    ▼
Validation Report + IntentHash Lock
```

## Output Report Format

```json
{
  "valid": true,
  "spidx_hash": "0x...",
  "entries_validated": 47,
  "chain_confidence": 0.847,
  "max_depth": 12,
  "lore_violations": [],
  "warnings": ["Low confidence at entry 23: 0.45"],
  "ternary_diagnostics": {
    "pos_ratio": 0.34,
    "neg_ratio": 0.12,
    "zero_ratio": 0.54
  }
}
```

## Build Requirements
- Python 3.10+
- PRIMUS core: hash, ternary_ops (TernaryGates), types
- PyYAML for SPIDX parsing
- SKL002 (Lore Validator) for compliance check

## Validation

```python
# Test SPIDX entry validation
entry = {
    'premise': 'A implies B',
    'conclusion': 'B',
    'operator': 'implies',
    'confidence': 0.9,
    'ternary_state': ternary_hash_to_intent_hash('test_state'),
    'intent_hash': ternary_hash_to_intent_hash('A implies B|B|implies'),
    'dependencies': []
}

valid, errors = validate_spidx_entry(entry, {})
assert valid, f"Errors: {errors}"

# Test invalid operator
entry['operator'] = 'invalid_op'
valid, errors = validate_spidx_entry(entry, {})
assert not valid
assert "Unknown operator" in errors[0]
```

## Anti-patterns
- Skipping root IntentHash verification (chain can be spliced)
- Not checking ternary state format (243 trits exactly)
- Ignoring confidence propagation (overconfident conclusions)
- Circular dependencies (breaks DAG assumption)
- Not integrating Lore Validator (generates invalid narrative)

## References
- PRD-MOC-INVENTORY-SYNTHESIS.md (SKL006)
- PRIMUS core: hash, ternary_ops, types
- SKL002 (Lore Validator)
- SKL004 (BATVERSE Operators)
- SPIDX specification (ADMG/TALEX)
- IntentHash specification