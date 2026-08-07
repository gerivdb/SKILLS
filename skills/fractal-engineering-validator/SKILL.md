---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xFRACTAL_VALIDATOR_20260801
status: active
---

# Skill: fractal-engineering-validator

## Purpose
Validate the fractal self-similarity invariant across L0-L4 strata per DAG-3 design (ATOM-042, ATOM-045). Ensures recursive 3^n pattern holds at every layer.

## Context
The ecosystem follows fractal engineering: each stratum L0-L4 mirrors the same triadic structure (Primitive / Structural / Anamorphic). This skill validates compliance.

## Rules

### 1. Stratum presence check
- L0-CANON: Must contain primitive definitions (DAG-3 root)
- L1-INFRA: Must contain structural relations (6 kinds)
- L2-PLATFORM: Must contain orchestration relations (3 kinds)
- L3-CITIZENS: Must contain anamorphic citizens
- L4-TOOLS: Must contain tooling primitives
- L5-ARCHIVE: Read-only, no validation required

### 2. Self-similarity verification
For each stratum, verify:
- Triad exists: primitives/, structural/, namorphic/ (or equivalent)
- DAG-3 hierarchy depth <= 3
- Cross-stratum references resolve correctly

### 3. Recursion depth check
- Maximum recursion: 3^n where n = stratum index
- L0: 3^0 = 1 root
- L1: 3^1 = 3 branches
- L2: 3^2 = 9 branches
- L3: 3^3 = 27 branches
- L4: 3^4 = 81 branches

## Validation Command
`powershell
python -m tools.fractal_validator --strata L0-L4 --output .kilo/fractal-report.yaml
`

## Output Format
`yaml
stratum: L2-PLATFORM
triad_present: true
dag3_depth: 2
branches: 9
cross_refs: 47
status: PASS
`

## Anti-patterns
- Missing triad folder in any active stratum
- DAG-3 depth > 3 (breaks self-similarity)
- Cross-stratum references that don't resolve
- Stratum with > expected branches (bloat)

## References
- D-001: fractal-engineering-strata (design)
- ATOM-042: REPOSITORY-CENSUS
- ATOM-045: structural-relations
