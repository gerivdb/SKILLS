---
type: SKILL
version: "1.0.0"
status: proposed
date: "2026-08-08"
intent_hash: 0xSKILL_SSM_MATRIX_EXTRACTOR_20260808
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/ssm-matrix-extractor/SKILL.md
---

# Skill — SSM Matrix Extractor

## Description

Extrait les matrices W, U, b, V depuis le binaire RLM-243 et produit
`rlm_243_matrices.json`. BLOCKING pour Phase 1 (Analyse Laplacienne).

## Prérequis

- Probe P-801 validée
- RLM-243 compilé et accessible sur ENV2
- Python 3.10+ avec `numpy`, `scipy`

## Workflow

1. Localiser le binaire RLM-243 via `known_repositories.yaml`
2. Charger le binaire en mémoire (mapping mémoire si nécessaire)
3. Extraire W (81×81), U (81×M), b (81), V (81×P)
4. Valider dimensions et plages de valeurs
5. Sérialiser en JSON avec SHA256 checksum
6. Logger extraction dans WAL (NEXUS)

## Sorties

- `rlm_243_matrices.json` : matrices extraites
- `rlm_243_matrices.sha256` : checksum
- Log WAL : `[SSM_EXTRACT] matrices extracted, sha256=<hash>`

## Intégration

- **Slice S1** : première étape avant analyse spectrale
- **Skills suivants** : `laplace-spectrum-analyzer` consomme la sortie
- **Citizens** : LAPLACE-VERIFIER valide, NEXUS log

## Anti-patterns

- ❌ Extraire sans valider dimensions → corruption downstream
- ❌ Ignorer SHA256 → risque de matrice corrompue
- ❌ Modifier les matrices après extraction → invalide P-801

## Référence

- Probe : P-801
- Intent : INTENT-RLM243-LAPLACE-ANALYSIS
- ADR : ADR-2026-08-08-RLM243-LAPLACE-OPTIMIZATION
