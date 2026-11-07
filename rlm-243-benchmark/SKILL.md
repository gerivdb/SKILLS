---
type: SKILL
version: "1.0.0"
status: proposed
date: "2026-08-08"
intent_hash: 0xSKILL_RLM_243_BENCHMARK_20260808
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/rlm-243-benchmark/SKILL.md
---

# Skill — RLM-243 Benchmark

## Description

Exécute les benchmarks comparatifs avant/après, mesure le gain de performance,
valide le critère ≥ 35%.

## Prérequis

- Probe P-807 validée
- `rlm_243_optimized.c` compilé et fonctionnel
- Baseline `benchmark_before.txt` existante (177.45 tok/s)

## Workflow

1. Vérifier présence `benchmark_before.txt`
2. Compiler RLM-243 optimisé avec `zig build -Dcpu=westmere`
3. Exécuter 5 runs benchmark sur ENV2
4. Calculer moyenne et écart-type de tok/s
5. Calculer gain = (after - before) / before
6. Vérifier gain ≥ 0.35 et latence ≤ 1.7 ms
7. Générer `benchmark_after.txt` et `validation_report.pdf`
8. Logger dans WAL (NEXUS)

## Sorties

- `benchmark_after.txt` : résultats détaillés
- `validation_report.pdf` : rapport de validation
- Log WAL : `[BENCHMARK] before=<v>, after=<v>, gain=<v>, temp_max=<v>`

## Intégration

- **Slice S3** : étape centrale
- **Skills suivants** : `conditional-validation`
- **Citizens** : SPECTRUM-ANALYST exécute, ARGUS vérifie

## Anti-patterns

- ❌ Benchmark sans baseline → pas de mesure de gain
- ❌ Un seul run → statistiquement invalide
- ❌ Ignorer température → risque rollback pendant benchmark

## Référence

- Probe : P-807
- Intent : INTENT-RLM243-VALIDATION
- ADR : ADR-2026-08-08-RLM243-LAPLACE-OPTIMIZATION
