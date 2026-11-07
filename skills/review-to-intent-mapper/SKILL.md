---
type: skill
version: "1.0.0"
date: "2026-08-19"
intent_hash: 0xSKILL_REVIEW_TO_INTENT_MAPPER_20260819
status: active
---

# Skill: review-to-intent-mapper

## Purpose
Map V10.0 review feedback (M1-M5, missing items, recommendations) to concrete INTENT patches.

## Input
- Review document (V10.0 format)
- Current INTENT file path

## Action
1. Parse review for:
   - Missing items (contracts_kg_l, metrics_kg_l, schema_kg_l, replay_trajectory, relation_speaks)
   - M1-M5 verdicts and recommendations
   - New slices to add
2. For each missing item, determine target section:
   - contracts_kg_l -> Section 5 (ownership contracts)
   - metrics_kg_l -> Section 10 (KPIs)
   - schema_kg_l -> Section 3.6 (KG-L schema)
   - replay_trajectory -> new S14 slice
   - relation_speaks -> Section 2 (graph edge types)
3. Generate patch commands:
   - Section insertions
   - Table row additions
   - New slice creation
4. Output: ordered list of patches to apply

## Verify
All missing items from review mapped to sections -> COUNT == 0
Patch list is executable sequentially -> DRY_RUN PASS

## Ref
- governance-architect skill (M1-M4 mapping)
- ctulu-artifact-builder skill (report generation pattern)
