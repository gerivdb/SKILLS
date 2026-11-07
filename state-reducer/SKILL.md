---
type: SKILL
version: "1.0.0"
status: proposed
date: "2026-08-08"
intent_hash: 0xSKILL_STATE_REDUCER_20260808
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/state-reducer/SKILL.md
---

# Skill — State Reducer

## Description

Identifie les trits dominants via analyse spectrale, réduit l'état de 81
à N_opt trits, génère le mapping et valide la perte de précision < 5%.

## Prérequis

- Probe P-805 validée
- `rlm_243_spectrum.json` présent
- `config_opt.yaml` avec Δ_opt défini

## Workflow

1. Charger PoleSpectrum et matrices depuis `rlm_243_matrices.json`
2. Calculer contribution de chaque trit : `||C_i||₂`
3. Sélectionner trits dominants : `||C_i||₂ > τ · max_j ||C_j||₂`
4. Déterminer N_opt = nombre de trits dominants
5. Valider 54 ≤ N_opt ≤ 72 et ε_max < 5%
6. Générer `trit_mapping.json` (ancien → nouvel index)
7. Mettre à jour `config_opt.yaml` avec `state_size: <N_opt>`
8. Logger dans WAL (NEXUS)

## Sorties

- `trit_mapping.json` : mapping trits ancien → nouveau
- `config_opt.yaml` : section `state_size` mise à jour
- Log WAL : `[STATE_REDUCE] n_opt=<v>, n_reduced=<v>, epsilon_max=<v>`

## Intégration

- **Slice S2** : étape 2 d'optimisation structurelle
- **Skills suivants** : `certified-code-generator`
- **Citizens** : RLM243-OPTIMIZER exécute, ARGUS vérifie

## Anti-patterns

- ❌ Réduire sans valider ε_max → perte de précision
- ❌ N_opt < 54 → over-reduction
- ❌ Mapping incomplet → crash exécution

## Référence

- Probe : P-805
- Intent : INTENT-RLM243-OPTIMIZATION
- ADR : ADR-2026-08-08-RLM243-LAPLACE-OPTIMIZATION
