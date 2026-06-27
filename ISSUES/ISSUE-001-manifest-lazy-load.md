# ISSUE-001 — MANIFEST.json injecté entier = 10K tokens brûlés/session

**Type**: performance / token-cost  
**Priorité**: P0  
**Status**: open  
**Date**: 2026-06-27  
**Epic**: EPICS/EPIC-MANIFEST-LAZY-001.md  
**Assigné**: gerivdb

---

## Symptôme

Chaque session LLM sur gerivdb/SKILLS injecte `MANIFEST.json` (40 Ko, ~10 000 tokens)
au démarrage. Cela représente ~8% du budget de contexte utilisé avant la première
interaction utile.

## Impact

- Context anxiety augmentée dès le début de session
- Velocity effective réduite (mass=0.71 confirmé par CTULU vector.yaml)
- ~49 000 tokens/jour gaspillés (5 sessions × 9 800 tokens)

## Reproduction

1. Ouvrir une session LLM sur gerivdb/SKILLS
2. Observer l'injection de MANIFEST.json dans le contexte système
3. Compter les tokens : ~10 000 pour du catalogue non demandé

## Fix attendu

Voir ADR-001 + EPIC-MANIFEST-LAZY-001.
Action immédiate : créer `menu.yaml` (S-01 de l'EPIC).

## Critère de clôture

- [ ] `menu.yaml` généré et validé <200 tokens
- [ ] `ctulu_resolver.py` expose `get_menu()` et `load_skill(name)`
- [ ] Session test confirme réduction tokens boot
