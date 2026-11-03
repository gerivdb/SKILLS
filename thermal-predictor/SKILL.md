---
type: SKILL
version: "1.0.0"
status: proposed
date: "2026-08-08"
intent_hash: 0xSKILL_THERMAL_PREDICTOR_20260808
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/thermal-predictor/SKILL.md
---

# Skill - Thermal Predictor (M5 Predictif)

## Description

Utilise PoleSpectrum pour predire la charge thermique avant execution et
ajuster la charge pour garantir T_reelle < 70 degC. Remplace le M5 reactif
actuel par un M5 proactif.

## Prerequis

- Probe P-808 validee
- `rlm_243_spectrum.json` present
- Acces aux capteurs thermiques ENV2 (via `Get-CimInstance` PowerShell)

## Workflow

1. Charger PoleSpectrum depuis `rlm_243_spectrum.json`
2. Calculer T_predite = f(PoleSpectrum, charge_actuelle)
3. Comparer a T_seuil = 65 degC
4. Si T_predite > T_seuil : reduire charge ou augmenter delta
5. Si T_predite <= T_seuil : execution autorisee
6. Logger prediction et ajustement dans WAL (NEXUS)

## Sorties

- `thermal_prediction.json` : T_predite, T_seuil, ajustement
- Log WAL : `[M5_PREDICTIVE] temp_pred=<v>, action=<reduce|pass>`

## Integration

- **Slice S3** : M5 check avant benchmark
- **Slice S4** : monitoring continu
- **Citizens** : SPECTRUM-ANALYST supervise, NEXUS log

## Anti-patterns

- [KO] Executer sans prediction -> retour au M5 reactif
- [KO] Ignorer T_predite > T_seuil -> risque rollback
- [KO] Logger prediction dans WAL -> tracabilite perdue

## Reference

- Probe : P-808
- Intent : INTENT-RLM243-VALIDATION, INTENT-RLM243-DEPLOYMENT
- ADR : ADR-2026-08-08-RLM243-LAPLACE-OPTIMIZATION
