---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xKORX_PATH_MANAGER_20260801
status: active
---

# Skill: korx-path-manager

## Purpose
Manage KORX semantic paths: resolve, validate, version.

## Action
1. Read korx/paths.yaml (semantic path registry)
2. Resolve korx://<domain>/<entity> → local path
3. Validate existence + version match
4. Cache: .kilo/cache/korx/

## Verify
All korx:// refs in codebase resolve → PASS

## Ref
D-010: vft-fractal-ternary.design.yaml
