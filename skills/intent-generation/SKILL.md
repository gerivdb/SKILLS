---
type: skill
version: "1.0.0"
date: "2026-08-19"
intent_hash: 0xSKILL_INTENT_GENERATION_20260819
status: active
---

# Skill: intent-generation

## Purpose
Generate a full INTENT document from review output, framework alignment notes, and existing INTENT base.

## Input
- Base INTENT file path
- Review output (V10.0-style: mathèmes M1-M5, missing items, recommendations)
- Framework alignment notes (DeepSeek Harness, TrueForge, Frontier, OpenBot, etc.)
- Target version (ex: v1.0)

## Action
1. Read base INTENT and extract existing sections
2. Map review feedback to missing sections/slices using governance-architect M1-M4
3. Apply INTENT template structure:
   - Section 1: executive summary with framework alignment
   - Section 2: 3-layer nervous system metaphor + graph with edge types
   - Section 3: KG-L as common language + schema
   - Section 4: Architecture by strata with KG-L expression
   - Section 5: Ownership contracts for all MCPs + KG-L/KG-WAZAA
   - Section 6: Phi-CPS concrete loop
   - Section 7: Operationalized slices S1-S8 with R16 proofs
   - Section 8: ENV2 adaptation constraints
   - Section 9: Immediate action plan (next 2 weeks)
   - Section 10: Success metrics with thresholds
   - Section 11: Risks and mitigations
   - Section 12: References & traceability
   - Section 13: Chain of thought
   - Section 14+: new slices from review (S14-S18 pattern)
   - Alignment section: DSH + TrueForge + Frontier + Speedrun + OpenBot
   - Synthesis: complete nervous system diagram
   - Conclusion: final statement
4. Generate IntentHash: `0xINTENT_<SLUG_MAJUSCULES>_v<version>`
5. Write to INTENTS/<slug>.md

## Verify
frontmatter-guardian validate INTENTS/<slug>.md -> PASS
grep "^## " INTENTS/<slug>.md | wc -l >= 20

## Ref
- governance-architect skill (M1-M4)
- governance-doc-writer skill (frontmatter)
- prd-generation skill (template pattern)
- INTENT-MCP-SYNAPTIC-ECOSYSTEM-VISION-2026-08-19.md (template reference)
