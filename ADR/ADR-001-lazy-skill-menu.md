# ADR-001 — Lazy Loading du Skill Menu via menu.yaml

**Date**: 2026-06-27  
**Status**: proposed  
**IntentHash**: 0xSKILLS_MANIFEST_LAZY_LOAD_20260627  
**φ-CPS**: 4.7 (≥ 4.559 requis pour ADR constitutionnelle)  
**Auteur**: gerivdb

---

## Contexte

Le `MANIFEST.json` de gerivdb/SKILLS fait 40 Ko (~10 000 tokens). Il est injecté
entièrement à chaque session LLM, consommant ~8% du budget de contexte disponible
avant toute interaction utile. Le [Harness Engineering Guide](https://github.com/nexu-io/harness-engineering-guide/blob/main/guide/skill-system.md)
nomme explicitement ce pattern l'**anti-pattern #1** du Skill System.

## Décision

Introduire un `menu.yaml` compact (<200 tokens) comme seul point d'entrée au boot,
et ajouter `get_menu()` / `load_skill(name)` à `ctulu_resolver.py` pour le chargement
à la demande. `MANIFEST.json` reste la source de vérité — il n'est ni supprimé ni modifié.

## Alternatives considérées

| Option | Avantage | Rejet |
|---|---|---|
| Conserver MANIFEST.json entier | Zéro dev | Coût token inacceptable (10K/session) |
| Réécrire REGISTRY.yaml | Plus propre | Trop invasif, dev solo sans ressources |
| Vector store (RAG) | Optimal à long terme | Nécessite infra, hors contrainte actuelle |
| **menu.yaml + lazy load** | Chirurgical, réversible | **Choisi** |

## Conséquences

**Positives**:
- ~9 800 tokens économisés par session (~78%)
- Conforme Priority System du Context Engineering Guide
- Réversible : supprimer menu.yaml restaure l'état initial
- Aucune breaking change sur les 63 skills

**Négatives / Risques**:
- `load_skill()` ajoute 1 appel LLM pour charger une skill non connue
- Si `menu.yaml` n'est pas maintenu en sync avec REGISTRY.yaml → désync
- Risque de désync mitigé par `scripts/generate_menu.py` auto-généré

## Plan de mitigation désync

```yaml
# .pre-commit-config.yaml — hook à ajouter :
- repo: local
  hooks:
    - id: sync-skill-menu
      name: Sync menu.yaml with REGISTRY.yaml
      entry: python scripts/generate_menu.py
      language: python
      files: REGISTRY.yaml
```

## Références

- [Skill System Guide](https://github.com/nexu-io/harness-engineering-guide/blob/main/guide/skill-system.md)
- [Context Engineering Guide](https://github.com/nexu-io/harness-engineering-guide/blob/main/guide/context-engineering.md)
- INTENT: `INTENTS/INT-MANIFEST-LAZY-001.yaml`
- PRD: `PRD/PRD-MANIFEST-LAZY-001.md`
- EPIC: `EPICS/EPIC-MANIFEST-LAZY-001.md`
