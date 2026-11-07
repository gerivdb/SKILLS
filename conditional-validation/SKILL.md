---
type: SKILL
version: "1.0.0"
status: proposed
date: "2026-08-08"
intent_hash: 0xSKILL_CONDITIONAL_VALIDATION_20260808
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/conditional-validation/SKILL.md
---

# Skill — Conditional Validation

## Description

Configure les règles de skip des validations : si le PoleSpectrum prouve
la stabilité d'un chemin d'exécution, les validations redondantes sont
sautées. Réduit l'overhead de 40%.

## Prérequis

- Probe P-809 validée
- `rlm_243_spectrum.json` présent
- `skip_rules.yaml` généré

## Workflow

1. Charger PoleSpectrum depuis `rlm_243_spectrum.json`
2. Pour chaque chemin d'exécution :
   a. Calculer les pôles associés au chemin
   b. Si `Re(pᵢ) < -0.5` pour tous les pôles du chemin → marquer SKIP
   c. Sinon → marquer VALIDATE
3. Générer `skip_rules.yaml` avec les chemins skippables
4. Instrumenter le code pour respecter les règles
5. Mesurer overhead avant/après
6. Logger dans WAL (NEXUS)

## Sorties

- `skip_rules.yaml` : règles de skip par chemin
- Log WAL : `[COND_VALID] skipped=<n>, validated=<n>, overhead_reduction=<v>`

## Intégration

- **Slice S3** : activation après benchmark validé
- **Slice S4** : monitoring continu
- **Citizens** : RLM243-OPTIMIZER configure, ARGUS vérifie sécurité

## Anti-patterns

- ❌ Skipper un chemin instable → risque crash
- ❌ Seuil trop agressif (< -0.5) → skip excessif
- ❌ Pas de instrumentation → règles non appliquées

## Référence

- Probe : P-809
- Intent : INTENT-RLM243-VALIDATION
- ADR : ADR-2026-08-08-RLM243-LAPLACE-OPTIMIZATION
