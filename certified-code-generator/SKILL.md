---
type: SKILL
version: "1.0.0"
status: proposed
date: "2026-08-08"
intent_hash: 0xSKILL_CERTIFIED_CODE_GENERATOR_20260808
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/certified-code-generator/SKILL.md
---

# Skill — Certified Code Generator

## Description

Génère `rlm_243_optimized.c` et `rlm_243_optimized.h` à partir de
`config_opt.yaml` et `trit_mapping.json`. Code C SSE4.2 inline dans
`dispatch.zig` (Zig 0.15 compat).

## Prérequis

- Probe P-806 validée
- `config_opt.yaml` complet (Δ_opt, N_opt)
- `trit_mapping.json` complet
- Zig 0.15 installé sur ENV2

## Workflow

1. Charger `config_opt.yaml` et `trit_mapping.json`
2. Charger template C SSE4.2 depuis `unified-design/designs/`
3. Substituer paramètres : N_opt, Δ_opt, mapping
4. Générer `rlm_243_optimized.c` avec instructions SSE4.2 (`_mm_*`)
5. Générer `rlm_243_optimized.h` avec types inline
6. Valider pas d'`ArrayList.init()`, pas de types Win32 externes
7. Inliner le code dans `src/dispatch.zig` (avant bloc `// Tests`)
8. Compiler avec `zig build -Dcpu=westmere`
9. Logger dans WAL (NEXUS)

## Sorties

- `rlm_243_optimized.c` : code C optimisé
- `rlm_243_optimized.h` : headers
- `src/dispatch.zig` : code inliné
- Log WAL : `[CODE_GEN] n_opt=<v>, delta_opt=<v>, compile=<ok|fail>`

## Intégration

- **Slice S2** : dernière étape
- **Skills suivants** : `rlm-243-benchmark`
- **Citizens** : RLM243-OPTIMIZER génère, TRIX compile

## Anti-patterns

- ❌ Générer code hors `dispatch.zig` → violation ADR-101
- ❌ Utiliser AVX2 → ENV2 ne supporte pas
- ❌ Oublier inline → erreur résolution modules Zig 0.15

## Référence

- Probe : P-806
- Intent : INTENT-RLM243-OPTIMIZATION
- ADR : ADR-093-zig-015-api-compatibility, ADR-101-triade-runtime
