---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xWAZAA_BUZZ_BRIDGE_20260801
status: active
---

# Skill: wazaa-buzz-bridge

## Purpose
Bridge WAZAA event stream to BUZZ runtime for reactive execution.

## Context
WAZAA emits events; BUZZ executes blocks. Bridge maps events→blocks.

## Action
1. Read wazaa/events/*.json stream
2. Map vent.type → uzz.block_id via config/bridge-map.yaml
3. Inject into BUZZ queue: uzz enqueue <block_id> --payload <event>
4. Log to .kilo/wal/bridge.wal

## Verify
uzz status --queue shows enqueued blocks

## Ref
S-003: cfmi-scanner (pipeline bridge pattern)
