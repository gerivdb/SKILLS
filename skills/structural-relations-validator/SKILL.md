---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xSTRUCTURAL_VALIDATOR_20260801
status: active
---

# Skill: structural-relations-validator

## Purpose
Validate the 6 structural relation kinds (opposes, complements, inherits, requires, blocks, stabilizes) with symmetry and acyclicity constraints per ATOM-045.

## Context
Structural relations form the backbone of the meta-design triad. Every design must declare its relations explicitly. This skill enforces validity.

## Relation Kinds

| Kind | Symmetric | Transitive | Description |
|------|-----------|------------|-------------|
| opposes | Yes | No | Mutually exclusive alternatives |
| complements | Yes | No | Work together, enhance each other |
| inherits | No | Yes | Hierarchical specialization |
| equires | No | Yes | Hard dependency |
| locks | No | No | Prevents coexistence |
| stabilizes | No | No | Provides stability/grounding |

## Rules

### 1. Symmetry enforcement
- opposes and complements MUST be bidirectional
- If A opposes B u2192 B must oppose A
- If A complements B u2192 B must complement A

### 2. Acyclicity for transitive relations
- inherits and equires must form DAGs
- No cycles: Au2192Bu2192Cu2192A forbidden
- Use topological sort to verify

### 3. Cardinality constraints
- equires: max 3 outgoing per node (prevents over-coupling)
- inherits: single parent (tree structure)
- locks: max 5 per node

### 4. Coverage
- Every design in designs/ and toms/ must declare at least 1 relation
- Orphan designs (0 relations) flagged as WARNING

## Validation Command
`powershell
python -m tools.structural_validator --source atoms --source designs --output .kilo/structural-report.yaml
`

## Output Format
`yaml
relations_checked: 142
symmetry_violations: 0
cycles_detected: 0
cardinality_violations: 0
orphan_designs: 3
status: PASS
`

## Anti-patterns
- Declaring opposes without bidirectional link
- Creating equires cycles
- Exceeding cardinality limits
- Designs with zero declared relations

## References
- D-003: structural-relations (design)
- ATOM-045: structural-relations
- ATOM-050: meta-design-triad
