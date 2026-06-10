---
id: PRD-006
title: Migration des bypasses vers le pattern VERSES→SKILLS
repo: gerivdb/SKILLS
status: DRAFT
priority: P2
created: 2026-06-10
author: gerivdb
depends_on:
  - PRD-004 (VERSEContext)
  - VERSES/PRD-005 (verse_detector wiring)
consumers:
  - VERSES/brain_bypass_verse.py
  - VERSES/fluence_bypass_verse.py
  - VERSES/wazaa_bypass_verse.js
---

# PRD-006 — Migration bypasses VERSES vers pattern standard

## Contexte

Trois fichiers dans VERSES contournent la chaîne VERSES → SKILLS :
- `brain_bypass_verse.py` — bypass direct sans VERSEContext
- `fluence_bypass_verse.py` — bypass direct sans VERSEContext
- `wazaa_bypass_verse.js` — bypass en JS (hors pipeline Python)

Ces fichiers résolvent des besoins réels mais cassent la traçabilité du pipeline et ne bénéficient pas des mécanismes de rollback/compensation de `WorkflowExecutor`.

## Objectif

Pour chaque bypass :
1. Analyser ce qu'il fait (inputs, outputs, dépendances).
2. Le convertir en `VERSEContext` + workflow VERSES standard.
3. Archiver le bypass original dans `VERSES/archive/`.

## Critères d'acceptation

- [ ] `brain_bypass_verse.py` migré en workflow VERSES ou documenté comme étant hors-scope
- [ ] `fluence_bypass_verse.py` migré ou documenté
- [ ] `wazaa_bypass_verse.js` évalué (JS — peut rester hors pipeline Python si frontend only)
- [ ] Aucun nouveau fichier `*_bypass_*.py` ajouté sans PRD associé

## Note

Ce PRD est DRAFT — activer après PRD-004 et VERSES/PRD-005.

## Effort estimé

~1h
