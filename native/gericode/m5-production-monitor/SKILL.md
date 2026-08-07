---
name: m5-production-monitor
description: "Surveille le cycle de vie M5 des concepts conversationnels : detecte les embryons, mesure la maturite, et declenche les transitions detectBirth -> develop -> stabilize -> integrate -> lifecycle."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_M5_PRODUCTION_MONITOR_20260807
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: native/gericode/m5-production-monitor/SKILL.md
triggers:
  - "surveiller le cycle de vie M5"
  - "detecter les embryons de concept"
  - "mesurer la maturite des concepts"
  - "BOOT-0.5"
  - "m5-production-monitor"
tools:
  - read
  - write
  - bash
citizen: "ECOSYSTEM-BRAIN"
layer: "L4"
---

# Skill - M5 Production Monitor

> **Verdict** : **SKILL D'EXECUTION** - Surveillance du cycle de vie M5 des concepts conversationnels.

## Objectif

Surveiller le cycle de vie M5 des concepts conversationnels, detecter les embryons,
mesurer la maturite, et declencher les transitions : detectBirth -> develop -> stabilize -> integrate -> lifecycle.

## Declencheur

- Boot de session (`BOOT-0.5`)
- Post-commit sur un concept conversationnel
- Demande utilisateur "verifier la maturite des concepts"
- Execution de probe P-9xx

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `concept_registry_path` | Path | Chemin vers le registre des concepts |
| `m5_threshold` | float | Seuil de maturite pour integration (defaut: 0.7) |
| `probe_runner` | string | `pytest` / `behave` / `custom` |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `embryos` | list | Concepts en etat detectBirth |
| `developing` | list | Concepts en etat develop |
| `stable` | list | Concepts en etat stabilize |
| `integrated` | list | Concepts en etat integrate |
| `report` | object | Resume: total, embryos, mature, integrated |

## Cycle M5

```
detectBirth()
  -> Embryon detecte (maturity_score < 0.3)
  -> conversational_birth_detector probe

develop()
  -> Concept en developpement (0.3 <= maturity_score < 0.6)
  -> Clarifications et tests requis

stabilize()
  -> Concept stable (0.6 <= maturity_score < 0.8)
  -> Integration recommandee

integrate()
  -> Concept mature (maturity_score >= 0.8)
  -> Integration dans schemas, validators, pipelines

lifecycle()
  -> Concept archive (maturity_score = 1.0)
  -> archived, immuable
```

## Regles

1. Un concept embryon ne doit pas etre integre dans la production
2. Un concept mature (> 0.7) doit etre propose pour integration
3. La transition integrate -> lifecycle necessite une validation NEXUS
4. Toute transition est tracee dans le registre M5
5. BOOT-0.5 est obligatoire pour les sessions multi-repo
