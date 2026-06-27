# PRD — Lazy Loading du Skill Menu

**ID**: PRD-MANIFEST-LAZY-001  
**IntentHash**: 0xSKILLS_MANIFEST_LAZY_LOAD_20260627  
**Status**: proposed  
**Owner**: gerivdb  
**Date**: 2026-06-27  
**Strata**: L3

---

## Contexte

`MANIFEST.json` (40 Ko, ~10 000 tokens) est actuellement injecté intégralement à chaque boot de session LLM.
Selon le [Harness Engineering Guide](https://github.com/nexu-io/harness-engineering-guide/blob/main/guide/skill-system.md),
charger toutes les skills au démarrage est l'anti-pattern #1 du Skill System.
Avec 63 skills actives, chaque session brûle ~10K tokens avant la première ligne de travail réel.

## Problème

| Métrique | État actuel | Cible |
|---|---|---|
| Tokens injectés au boot | ~10 000 | <200 |
| Méthode | MANIFEST.json entier | menu.yaml + lazy load |
| Économie/session | — | ~9 800 tokens (−78%) |
| Sessions/jour | ~5 | ~5 |
| Économie/jour | — | ~49 000 tokens |

## Solution

### 1. `menu.yaml` — point d'entrée unique (<200 tokens)

```yaml
skills_menu:
  - name: causal-chain
    desc: "Engine causalité CTULU — DAGs, DoWhy Pearl L1-L3"
  - name: moe-router
    desc: "Routage intelligent MoE — GATE-0→4, dispatch engines"
  - name: safety-guard
    desc: "Validation sécurité φ-CPS ≥ 4.559 — instancié par tous citizens"
  # ... 1 ligne par skill, max 5 mots
```

### 2. `ctulu_resolver.py` — API lazy load

Exposer deux fonctions supplémentaires :
- `get_menu() → str` : retourne menu.yaml sérialisé (<200 tokens)
- `load_skill(name: str) → dict` : charge SKILL.md + schema depuis REGISTRY.yaml

### 3. Règle d'injection

Priorité contexte (conforme Context Engineering Guide) :
```
Priority 0 — System prompt      : 300–800 tokens
Priority 1 — menu.yaml          : <200 tokens  ← remplace MANIFEST entier
Priority 2 — Task instruction   : 200–1000 tokens
Priority 3 — load_skill(name)   : 500–1000 tokens (à la demande)
```

## Contraintes

- Dev solo : aucune refonte architecturale, modifications chirurgicales uniquement
- `ctulu_resolver.py` existe déjà — étendre, pas réécrire
- MANIFEST.json reste intact comme source de vérité
- Aucune breaking change sur les 63 skills

## Hors scope

- Réécriture de REGISTRY.yaml
- Nouveau repo ou nouveau système
- Unload automatique (phase 2)

## Références

- [Skill System](https://github.com/nexu-io/harness-engineering-guide/blob/main/guide/skill-system.md)
- [Context Engineering](https://github.com/nexu-io/harness-engineering-guide/blob/main/guide/context-engineering.md)
- INTENT: `INTENTS/INT-MANIFEST-LAZY-001.yaml`
- EPIC: `EPICS/EPIC-MANIFEST-LAZY-001.md`
