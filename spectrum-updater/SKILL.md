---
type: SKILL
version: "1.0.0"
status: proposed
date: "2026-08-08"
intent_hash: 0xSKILL_SPECTRUM_UPDATER_20260808
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/spectrum-updater/SKILL.md
---

# Skill — Spectrum Updater

## Description

Met à jour `rlm_243_spectrum.json` de manière incrémentale depuis les
mesures terrain. Alimente la META-LOOP KEEL avec un spectre actualisé.

## Prérequis

- Probe P-810 validée
- `rlm_243_spectrum.json` initial présent
- Mesures terrain disponibles (KRONOS/PLIX)

## Workflow

1. Charger `rlm_243_spectrum.json` initial
2. Charger mesures terrain depuis KRONOS/PLIX
3. Pour chaque nouveau point de mesure :
   a. Comparer prédiction vs réel
   b. Si écart > τ : mettre à jour le pôle correspondant
   c. Si écart > 2τ : signaler ARGUS (anomalie)
4. Sauvegarder `spectrum_live.json` (spectre actualisé)
5. Logger chaque mise à jour dans WAL (NEXUS)
6. Notifier `keel-meta-loop` pour réoptimisation si nécessaire

## Sorties

- `spectrum_live.json` : spectre actualisé
- Log WAL : `[SPECTRUM_UPDATE] pole_id=<i>, old=<v>, new=<v>, gap=<v>`

## Intégration

- **Slice S4** : étape 2 de Phase 4
- **Skills consommés** : aucun (feeder pour `keel-meta-loop`)
- **Citizens** : SPECTRUM-ANALYST exécute, NEXUS log, ARGUS surveille anomalies

## Anti-patterns

- ❌ Mettre à jour sans valider écart → spectre corrompu
- ❌ Ignorer écart > 2τ → anomalie masquée
- ❌ Pas de sauvegarde initiale → perte de référence

## Référence

- Probe : P-810
- Intent : INTENT-RLM243-DEPLOYMENT
- ADR : ADR-2026-08-08-RLM243-LAPLACE-OPTIMIZATION
