---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xPATCH_MANAGEMENT_20260801
status: active
---

# Skill: patch-management

## Purpose
Apply, track, and rollback patches across 47 repos atomically.

## Action
1. Read .kilo/patches/<id>.patch (unified diff)
2. For each repo in ECOS_ROOT.json: git apply --check
3. If all pass: git apply per repo, record in .kilo/wal/patch.wal
4. Rollback: git apply -R per repo on failure

## Verify
git status --short clean in all 47 repos

## Ref
S-009: git-checkpoint
