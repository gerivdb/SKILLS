---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xADMG_IMPLEMENTATION_20260801
status: active
---

# Skill: admg-implementation

## Purpose
Implement ADMG (Architecture Decision Meta-Graph) from design.

## Action
1. Read designs/admg-state-model.yaml
2. Generate src/admg/graph.py (nodes, edges, DAG validation)
3. Generate src/admg/state.py (state machine per node)
4. Generate src/admg/query.py (path, impact, cycle)

## Verify
python -m pytest tests/admg/ → all pass

## Ref
D-002: admg-state-model.yaml
