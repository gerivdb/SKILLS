---
id: PRD-000
title: Index des PRD SKILLS
repo: gerivdb/SKILLS
created: 2026-06-10
author: gerivdb
---

# PRD SKILLS — Index

> Audit écosystème 2026-06-10.

| PRD | Titre | Priorité | Statut |
|---|---|---|---|
| [PRD_SKILLS_AGENTIC_RAG](PRD_SKILLS_AGENTIC_RAG.md) | Agentic RAG (existant) | — | actif |
| [PRD_SKILLS_UAE_KEEL_METAMORPHIC_V1](PRD_SKILLS_UAE_KEEL_METAMORPHIC_V1.md) | UAE/KEEL Metamorphic (existant) | — | actif |
| [PRD_CONSOLIDATION_PERP_TO_PERPLEXITY](PRD_CONSOLIDATION_PERP_TO_PERPLEXITY.md) | Consolidation Perplexity (existant) | — | actif |
| [PRD-004-verse-context](PRD-004-verse-context.md) | VERSEContext + verse_detector wiring | P2 | READY |
| [PRD-005-skill-loader-ctulu-wiring](PRD-005-skill-loader-ctulu-wiring.md) | skill_loader → CTULUResolver | P1 | READY |
| [PRD-006-bypasses-migration](PRD-006-bypasses-migration.md) | Migration bypasses vers pattern VERSES→SKILLS | P2 | DRAFT |

## Dépendances

```
PRD-005 (skill_loader wiring) → peut être fait immédiatement
PRD-004 (verse_detector)      → dépend de VERSES/verse_detector.py
PRD-006 (bypasses)            → dépend de VERSES coord
```

## Liens écosystème

- [VERSES/WorkflowVerse](https://github.com/gerivdb/VERSES/tree/main/WorkflowVerse)
- [CTULU/REGISTRY.yaml](https://github.com/gerivdb/CTULU/blob/main/REGISTRY.yaml)
- [PRIMUS/PRD](https://github.com/gerivdb/PRIMUS/tree/main/PRD)
