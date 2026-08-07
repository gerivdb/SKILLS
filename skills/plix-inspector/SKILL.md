---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xPLIX_INSPECT_20260801
status: active
---

# Skill: plix-inspector

## Purpose
Analyze design relations for impact analysis, diff detection, and conflict resolution. Used by plix inspect command.

## Context
PLIX designs form a graph. This skill provides query operations on that graph.

## Inspection Modes

### 1. Relations
`powershell
plix inspect relations --node <design_id> --depth 2
`
- Shows incoming/outgoing relations by kind
- Depth-limited traversal
- Output: YAML or ASCII tree

### 2. Impact
`powershell
plix inspect impact --changed <design_id> --radius 3
`
- Computes transitive closure of equires + inherits
- Returns affected designs with distance
- Used for change impact assessment

### 3. Diff
`powershell
plix inspect diff --base main --head feature/xyz
`
- Compares design graphs between git refs
- Detects: added/removed nodes, changed relations
- Output: structured diff YAML

### 4. Conflicts
`powershell
plix inspect conflicts --strict
`
- Detects: opposes violations, equires cycles, cardinality breaches
- --strict: fail on any conflict
- Output: conflict list with severity

## Data Source
- designs/*.yaml and toms/*.yaml with elations field
- Git history for diff mode

## Output Format (Impact)
`yaml
changed: ATOM-063
affected:
  - design: D-005
    distance: 1
    via: requires
  - design: S-010
    distance: 2
    via: requires->orchestrates
total_affected: 47
max_radius: 3
`

## Anti-patterns
- Running impact without --radius (full graph traversal)
- Ignoring conflicts in CI
- Not using diff before merge
- Querying without specifying --node

## References
- S-005: plix-graph-generator (skill)
- S-002: structural-relations-validator (skill)
- D-003: structural-relations (design)
- ATOM-045: structural-relations
- ATOM-060: orchestration-relations
