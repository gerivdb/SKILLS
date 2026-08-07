---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xBUZZ_PARASITAGE_20260801
status: active
---

# Skill: buzz-parasitage

## Purpose
Detect and remediate parasitic @block patterns in BUZZ runtime that hijack control flow.

## Trigger
BUZZ execution shows unexpected blocks, latency spikes, or state corruption.

## Action
1. Scan .kilo/buzz/blocks/ for @block with parasite: true
2. Check caller chain for unauthorized injections
3. Emit .kilo/buzz/parasite-report.yaml
4. Auto-fix: strip parasite flag, restore original block

## Verify
uzz validate --no-parasites -> PASS

## Ref
ATOM-065: co-abductive-halo
