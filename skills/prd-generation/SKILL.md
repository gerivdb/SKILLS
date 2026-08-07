---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xPRD_GENERATION_20260801
status: active
---

# Skill: prd-generation

## Purpose
Generate PRD from EPIC + INTENT + gap report using governance-doc-writer.

## Input
- EPIC file
- INTENT file(s)
- Gap report (from ARGUS)

## Action
1. Merge EPIC scope + INTENT hashes + gap priorities
2. Apply PRD template: .kilo/templates/PRD.md
3. Frontmatter: type=PRD, status=proposed, intent_hash=0x<SLUG>
4. Write to PRD/<slug>.md

## Verify
rontmatter-guardian validate PRD/<slug>.md → PASS

## Ref
governance-doc-writer skill
