---
id: PRD-004
title: VERSEContext — branchement natif du verse_detector
repo: gerivdb/SKILLS
status: READY
priority: P2
created: 2026-06-10
author: gerivdb
depends_on:
  - VERSES/verse_detector.py
  - SKILLS/verse_context.py (implémenté 2026-06-10)
consumers:
  - WorkflowVerse/workflow_executor.py
  - VERSES/bon_sens_python_verse et tous les verses existants
---

# PRD-004 — VERSEContext — branchement natif verse_detector

## Contexte

`verse_context.py` a été implémenté (2026-06-10) avec `from_verse_detector()` comme constructeur factory. `workflow_executor.py` accepte un `verse_context` optionnel. Cependant `verse_detector.py` dans VERSES ne produit pas nativement un `VERSEContext` — il retourne un dict ou objet propriétaire non branché sur ce pattern.

Par ailleurs, les 15+ Verses existants dans VERSES (bon_sens_python_verse, urban_ontology_verse, etc.) n'ont aucun `verse_context.py` local et n'utilisent pas `VERSEContext`.

## Problème

1. `verse_detector.py` retourne un format non interopérable avec `VERSEContext.from_verse_detector()`.
2. Les verses existants sont des modules isolés sans contexte injecté dans `WorkflowExecutor`.
3. `VERSEContext.requires_tool()` stocke une string mais rien ne la résout avant l'exécution.

## Objectif

1. **Adapter `from_verse_detector()`** pour accepter le format réel de `verse_detector.py`.
2. **Auto-résolution des tools** : quand `VERSEContext.tools` est non vide, appeler `CTULUResolver.resolve_many()` automatiquement dans `to_dict()`.
3. **Template de migration** : documenter comment convertir un verse existant pour produire un `VERSEContext`.

## Critères d'acceptation

- [ ] `from_verse_detector()` compatible avec l'output réel de `VERSES/verse_detector.py`
- [ ] `VERSEContext.to_dict()` inclut `__ctulu_tools` avec les `ToolEntry` résolus
- [ ] Au moins 1 verse existant migré vers `VERSEContext` (bon_sens_python_verse en priorité)
- [ ] Tests mis à jour dans `tests/test_verse_context.py`

## Effort estimé

~30 min
