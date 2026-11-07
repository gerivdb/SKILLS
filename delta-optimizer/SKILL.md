---
type: SKILL
version: "1.0.0"
status: proposed
date: "2026-08-08"
intent_hash: 0xSKILL_DELTA_OPTIMIZER_20260808
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/delta-optimizer/SKILL.md
---

# Skill — Delta Optimizer

## Description

Calcule Δ_critique depuis PoleSpectrum, détermine Δ_opt ∈ {1,2,3} qui
maximise la rapidité sans dépasser Δ_critique.

## Prérequis

- Probe P-804 validée
- `rlm_243_spectrum.json` présent

## Workflow

1. Charger PoleSpectrum depuis `rlm_243_spectrum.json`
2. Calculer Δ_critique = π / max(|Im(pᵢ)|)
3. Énumérer Δ candidates = {1, 2, 3}
4. Sélectionner Δ_opt = max{Δ ∈ {1,2,3} | Δ < Δ_critique}
5. Si Δ_opt = Δ_actuel (3) : signaler ARGUS, pas d'optimisation possible
6. Générer `config_opt.yaml` avec `delta_optimal: <Δ_opt>`
7. Logger dans WAL (NEXUS)

## Sorties

- `config_opt.yaml` : section `delta_optimal`
- Log WAL : `[DELTA_OPT] delta_crit=<v>, delta_opt=<v>, gain_pct=<v>`

## Intégration

- **Slice S2** : première étape d'optimisation structurelle
- **Skills suivants** : `state-reducer`, `certified-code-generator`
- **Citizens** : RLM243-OPTIMIZER exécute, MOX valide

## Anti-patterns

- ❌ Choisir Δ < Δ_crit/2 → sous-échantillonnage
- ❌ Ignorer Δ_opt = Δ_actuel → perte de temps
- ❌ Modifier Δ sans mettre à jour config_opt.yaml → inconsistency

## Référence

- Probe : P-804
- Intent : INTENT-RLM243-OPTIMIZATION
- ADR : ADR-2026-08-08-RLM243-LAPLACE-OPTIMIZATION
