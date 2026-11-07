---
type: SKILL
version: "1.0.0"
status: proposed
date: "2026-08-08"
intent_hash: 0xSKILL_LAPLACE_PROOF_WRITER_20260808
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/laplace-proof-writer/SKILL.md
---

# Skill — Laplace Proof Writer

## Description

Génère `laplace_proof.tex` formalisant la preuve du lien H(z) ↔ H(s)
pour RLM-243. Document vérifiable par MOX (P-106/P-107).

## Prérequis

- Probe P-802 validée
- `rlm_243_spectrum.json` présent avec pôles validés

## Workflow

1. Charger PoleSpectrum et matrices depuis `rlm_243_matrices.json`
2. Rédiger preuve Tustin inverse en LaTeX :
   - Énoncé : H(z) = C·(zI-A)⁻¹·B+D
   - Transformation : z = e^{sΔ} → H(s) = C·(sI-A_c)⁻¹·B_c+D_c
   - Vérification : pôles de H(s) correspondent aux valeurs propres de A_c
3. Inclure vérifications numériques (comparaison H(z=1) vs H(s=0))
4. Générer PDF via `pdflatex`
5. Soumettre à MOX pour validation P-106/P-107
6. Logger dans WAL (NEXUS)

## Sorties

- `laplace_proof.tex` : preuve formelle
- `laplace_proof.pdf` : PDF compilé
- Log WAL : `[LAPLACE_PROOF] generated, pages=<n>, validated=<ok|fail>`

## Intégration

- **Slice S1** : livrable final de Phase 1
- **Slice S3** : audit MOX
- **Citizens** : LAPLACE-VERIFIER rédige, MOX valide

## Anti-patterns

- ❌ Preuve sans vérification numérique → risque erreur mathématique
- ❌ PDF non compilé → document invalide
- ❌ Passer à Phase 2 sans preuve validée → rupture R14

## Référence

- Probe : P-802
- Intent : INTENT-RLM243-LAPLACE-ANALYSIS
- ADR : ADR-2026-08-08-RLM243-LAPLACE-OPTIMIZATION
