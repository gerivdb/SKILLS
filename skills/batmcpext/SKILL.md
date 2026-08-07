---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xBATMCPEXT_20260801
status: active
---

# Skill: batmcpext

## Purpose
Extend BatMCP with custom tools for gerivdb ecosystem.

## Action
1. Read atmcp/tools/*.py (existing tools)
2. Generate new tool: atmcp/tools/<name>.py per spec
3. Register in atmcp/config/tools.yaml
4. Test: atmcp call <name> --dry-run

## Verify
New tool appears in atmcp list → PASS

## Ref
S-012: matrix-runner (tool pattern)
