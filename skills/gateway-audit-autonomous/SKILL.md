---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xGATEWAY_AUDIT_AUTO_20260801
status: active
---

# Skill: gateway-audit-autonomous

## Purpose
Autonomous audit of GATEWAY-MANAGER clapet state (BDCP/FREE).

## Action
1. Query http://localhost:18000/clapet/status
2. Verify BDCP mode (default, invariant)
3. Check watchdog: auto-close ≤ 300s
4. Log: .kilo/wal/gateway.wal

## Verify
BDCP=true, watchdog=active → PASS

## Ref
ADR: BDCP_INVIOLABLE_20260416
