---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xINSIGHT_CAPTURE_20260801
status: active
---

# Skill: insight-capture

## Purpose
Capture, structure, and index insights from sessions into MDU.

## Action
1. Input: session transcript or manual note
2. Extract: pattern, decision, anti-pattern, metric
3. Map to: design, skill, ATOM, or ADR
4. Write: .kilo/insights/<timestamp>_<hash>.yaml

## Verify
Insight linked to ≥1 existing artifact → PASS

## Ref
S-011: atomic-task-planner (pattern extraction)
