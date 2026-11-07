---
type: SKILL
version: "1.0.0"
status: proposed
date: "2026-08-08"
intent_hash: 0xSKILL_KEEL_META_LOOP_20260808
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/keel-meta-loop/SKILL.md
---

# Skill — Keel Meta Loop

## Description

Orchestre la META-LOOP KEEL : mesure écart réel/prédit, analyse spectre,
réoptimise Δ_opt et N_opt, déploie, converge vers optimum global.

## Prérequis

- Probe P-810 validée
- `spectrum_live.json` présent (spectre actualisé)
- `convergence_report.yaml` générable

## Workflow

1. Charger `spectrum_live.json` et historique mesures
2. Calculer écart : `|gain_réel - gain_prédit| / gain_prédit`
3. Si écart > 5% : déclencher réoptimisation
4. Réoptimiser Δ_opt et N_opt via `delta-optimizer` + `state-reducer`
5. Régénérer code via `certified-code-generator`
6. Déployer et mesurer nouveau gain
7. Vérifier convergence monotone
8. Générer `convergence_report.yaml`
9. Logger chaque itération dans WAL (NEXUS)

## Sorties

- `convergence_report.yaml` : historique itérations, gains, écarts
- Log WAL : `[KEEL_META_LOOP] iteration=<n>, gain=<v>, gap=<v>, converged=<bool>`

## Intégration

- **Slice S4** : cœur de Phase 4
- **Skills consommés** : `delta-optimizer`, `state-reducer`, `certified-code-generator`, `spectrum-updater`
- **Citizens** : KEEL orchestre, NEXUS trace, ARGUS détecte régression

## Anti-patterns

- ❌ Itérer sans vérifier convergence → régression silencieuse
- ❌ Ignorer écart > 5% → optimum jamais atteint
- ❌ Pas de WAL → perte traçabilité META-LOOP

## Référence

- Probe : P-810
- Intent : INTENT-RLM243-DEPLOYMENT
- ADR : ADR-2026-08-08-RLM243-LAPLACE-OPTIMIZATION
