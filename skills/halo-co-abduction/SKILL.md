---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xHALO_CO_ABDUCTION_20260801
status: active
---

# Skill: halo-co-abduction

## Purpose
Co-abductive reasoning halo: infer missing context from partial observations.

## Action
1. Input: partial observation (anomaly, gap, error)
2. Query ATOMs + designs for related patterns
3. Generate hypotheses ranked by coherence
4. Output: .kilo/halo/hypotheses.yaml

## Verify
Top hypothesis validated by cfmi-scanner -> PASS

## Ref
ATOM-065: co-abductive-halo
