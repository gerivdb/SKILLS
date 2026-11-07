---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-07"
intent_hash: 0xSKILL_KIVA_CI_LOCAL_20260807
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/kiva-ci-local/SKILL.md
---

# Skill — kiva-ci-local

Template et validation de `.kiva/ci.yaml` pour pipelines CI locales KIVA-CLI.

## Objectifs
- Générer un template `.kiva/ci.yaml` pour un repo.
- Valider la conformité du pipeline.
- Intégrer avec KIVA-CLI.

## Entrées
- `repo_path`: chemin du repo cible.
- `stages`: liste des stages à inclure.

## Sorties
- `Path`: chemin du fichier `.kiva/ci.yaml` généré.

## Règles
- Le template doit inclure les stages obligatoires : lint, test, typecheck, validate.
- Les stages N243 sont ajoutés si le repo contient des skills N243.
- La validation vérifie que tous les chemins référencés existent.

## Tests
- `tests/test_kiva_ci_local.py`: 100% passants requis.

## Probes
- P-501: template valide en < 5s
- P-502: 0 erreur de chemin
- P-503: 0 stage manquant
