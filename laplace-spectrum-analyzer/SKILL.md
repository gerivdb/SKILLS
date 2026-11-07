---
type: SKILL
version: "1.0.0"
status: proposed
date: "2026-08-08"
intent_hash: 0xSKILL_LAPLACE_SPECTRUM_ANALYZER_20260808
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/laplace-spectrum-analyzer/SKILL.md
---

# Skill — Laplace Spectrum Analyzer

## Description

Construit H(z) depuis les matrices SSM, applique Tustin inverse pour obtenir
H(s), calcule les pôles, analyse le spectre. Cœur mathématique du projet.

## Prérequis

- Probe P-802 validée
- `rlm_243_matrices.json` présent (sortie de `ssm-matrix-extractor`)
- Python 3.10+ avec `numpy`, `scipy`, `control`

## Workflow

1. Charger matrices depuis `rlm_243_matrices.json`
2. Construire H(z) = C·(zI - A)⁻¹·B + D
3. Appliquer Tustin inverse : A_c = (2/Δ)·(A + I)·(A - I)⁻¹
4. Calculer pôles : valeurs propres de A_c
5. Analyser spectre : stabilité, Δ_critique, trits dominants
6. Générer `rlm_243_spectrum.json`
7. Générer `laplace_proof.tex` (preuve formelle)
8. Logger dans WAL (NEXUS)

## Sorties

- `rlm_243_spectrum.json` : pôles, Δ_crit, trits dominants
- `laplace_proof.tex` : preuve mathématique H(z) ↔ H(s)
- Log WAL : `[LAPLACE_ANALYSIS] poles=<n>, delta_crit=<v>, stable=<bool>`

## Intégration

- **Slice S1** : étape centrale
- **Skills suivants** : `thermal-predictor`, `delta-optimizer`, `state-reducer`
- **Citizens** : LAPLACE-VERIFIER certifie, ARGUS vérifie plausibilité

## Anti-patterns

- ❌ Calculer pôles sans valider H(z) d'abord → résultats invalides
- ❌ ignorer singularité Tustin (A-I non-inversible) → crash
- ❌ Générer proof.tex sans valider cohérence numérique → preuve fausse

## Référence

- Probe : P-802, P-803
- Intent : INTENT-RLM243-LAPLACE-ANALYSIS
- ADR : ADR-2026-08-08-RLM243-LAPLACE-OPTIMIZATION
