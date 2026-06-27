# EPIC — Lazy Loading Skill Menu

**ID**: EPIC-MANIFEST-LAZY-001  
**IntentHash**: 0xSKILLS_MANIFEST_LAZY_LOAD_20260627  
**PRD**: PRD/PRD-MANIFEST-LAZY-001.md  
**Status**: draft  
**Owner**: gerivdb  
**Date**: 2026-06-27  
**Taille estimée**: <5 Ko (conforme règle EPIC ≤ 10 Ko)

---

## Objectif

Réduire de 78% les tokens consommés au boot d'une session LLM sur gerivdb/SKILLS
en remplaçant l'injection massive de `MANIFEST.json` par un menu compact + lazy load.

## Stories

### S-01 — Générer `menu.yaml`

**Effort**: 30 min  
**Critère**: `menu.yaml` à la racine, 1 ligne par skill, total <200 tokens

```
Input  : REGISTRY.yaml (63 skills)
Output : menu.yaml (63 entrées name+desc 5 mots max)
Script : scripts/generate_menu.py
```

### S-02 — Étendre `ctulu_resolver.py`

**Effort**: 1h  
**Critère**: `get_menu()` et `load_skill(name)` testables unitairement

```python
# Fonctions à ajouter :
def get_menu() -> str:          # lit menu.yaml → str <200 tokens
def load_skill(name: str) -> dict:  # lit REGISTRY.yaml → {doc, schema}
```

### S-03 — Mettre à jour la règle d'injection

**Effort**: 15 min  
**Critère**: Documentation dans `SKILLS.md` + `LLM_BOOT_PROTOCOL.md` de LLM-REPO

### S-04 — Tests de non-régression

**Effort**: 30 min  
**Critère**: `tests/test_lazy_load.py` — 63 skills loadables, aucune erreur

## Séquence

```
S-01 → S-02 → S-04 → S-03
```

## Blockers connus

- `ctulu_resolver.py` doit être relu avant extension (vérifier interface actuelle)
- `LLM_BOOT_PROTOCOL.md` dans LLM-REPO doit être mis à jour en S-03

## Métriques de succès

| Métrique | Avant | Après |
|---|---|---|
| Tokens boot | ~10 000 | <200 |
| Skills loadables | 63 (toutes en mémoire) | 63 (à la demande) |
| Régression | — | 0 |
