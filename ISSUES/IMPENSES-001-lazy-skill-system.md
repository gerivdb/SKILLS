# IMPENSÉS — Lazy Skill System

**Lié à**: EPIC-MANIFEST-LAZY-001, ADR-001  
**Date**: 2026-06-27  
**Auteur**: gerivdb  

---

Ce document capture les angles morts identifiés lors de l'analyse du MANIFEST.json
par croisement avec le Harness Engineering Guide.

---

## Impensé 1 — L'unload n'existe pas

**Observation**: `skill_loader.py` charge des skills mais n'expose pas de `unload_skill()`.
**Risque**: Si 5 skills sont chargées successivement sans déchargement, le contexte
accumule 5 × ~1 000 tokens = 5 000 tokens de schemas actifs inutiles.
**Référence**: Le guide dit explicitement : *"Always provide unload_skill alongside load_skill"*.
**Action suggérée**: Ajouter `unload_skill(name)` dans ctulu_resolver.py (phase 2, après S-01→S-04).

---

## Impensé 2 — Le REGISTRY.yaml est la source de vérité mais n'a pas de hash d'intégrité

**Observation**: REGISTRY.yaml v1.0.8, 63 skills, mais aucun mécanisme ne détecte
si menu.yaml dérive du REGISTRY après un ajout de skill.
**Risque**: LLM charge menu.yaml périmé → propose des skills qui n'existent plus ou
manque les nouvelles.
**Action suggérée**: Ajouter `registry_hash` dans menu.yaml + vérification au load.

---

## Impensé 3 — `citizens.yaml` et `CITIZENS.md` ne sont pas bridgés au Skill Menu

**Observation**: Les citizens (agents) sont définis séparément des skills.
Un citizen a besoin de savoir quelles skills il peut invoquer — mais ce lien
n'est pas formalisé dans le mécanisme de lazy load.
**Risque**: Un citizen charge toutes ses skills au boot → recrée l'anti-pattern MANIFEST.
**Action suggérée**: Ajouter un champ `default_skills: []` dans citizens.yaml,
chargé via load_skill() au moment où le citizen est instancié, pas au boot global.

---

## Impensé 4 — `verse_context.py` et le lazy load ne sont pas coordonnés

**Observation**: `verse_context.py` gère la compaction de contexte (VERSES).
Mais si load_skill() ajoute des tokens en cours de session, verse_context.py
ne sait pas distinguer les tokens de skill (Priority 1) des tokens de conversation (Priority 5).
**Risque**: La compaction écrase des schemas de skills actives.
**Action suggérée**: Tagger les blocs de contexte par priorité dans verse_context.py
(conforme au Priority System du Context Engineering Guide — Priority 0→6).

---

## Impensé 5 — Le `skill_health_monitor.py` n'a pas de rubric d'évaluation

**Observation**: `skill_health_monitor.py` existe mais évalue la santé des skills
sans critères formels → self-evaluation bias (cf. Long-Running Harness Guide).
**Risque**: Monitor dit "tout va bien" même si 20% des skills ont des SKILL.md manquants.
**Action suggérée**: Ajouter une rubric explicite :
```
1. SKILL.md présent ? PASS/FAIL
2. path valide dans REGISTRY.yaml ? PASS/FAIL
3. Consommée par ≥ 1 repo ? PASS/FAIL
4. phi_weight > 0 ? PASS/FAIL
```
