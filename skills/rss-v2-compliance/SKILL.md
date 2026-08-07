---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xRSS_V2_COMPLIANCE_20260801
status: active
---

# Skill: rss-v2-compliance

## Purpose
Validate RSS-v2 feed compliance across all citizen repos.

## Action
1. For each repo in L3-CITIZENS: check eeds/*.xml exists
2. Validate against schemas/rss-v2.xsd
3. Check <atom:link rel="self"> present
4. Report: .kilo/rss-compliance.yaml

## Verify
All 17 citizen feeds validate -> PASS

## Ref
D-008: verses-architecture.design.yaml
