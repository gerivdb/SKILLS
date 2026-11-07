---
type: skill
version: "1.0.0"
date: "2026-08-19"
intent_hash: 0xSKILL_INTENT_VERSION_BUMPER_20260819
status: active
---

# Skill: intent-version-bumper

## Purpose
Bump an INTENT version (v0.9 -> v1.0) by updating metadata, renumbering sections, and patching references without rewriting the whole document.

## Input
- INTENT file path
- Target version (ex: v1.0)
- List of new sections to insert (optional)
- Framework alignments to add in summary (optional)

## Action
1. Read INTENT file
2. Update intent_hash in frontmatter: `0x..._v<target>`
3. Update title: `# INTENT v<target> -- ...`
4. Update executive summary IntentHash line
5. Renumber sections after insertion point if new sections are provided
6. Insert new sections at correct position
7. Update footer bullet list with new features
8. Update final IntentHash line
9. Validate with frontmatter-guardian

## Verify
grep "^intent_hash: 0x.*_v<target>" INTENT/<file>.md -> MATCH
grep "^# INTENT v<target>" INTENT/<file>.md -> MATCH
frontmatter-guardian validate INTENT/<file>.md -> PASS

## Ref
- doc-status-validator skill
- governance-doc-writer skill
