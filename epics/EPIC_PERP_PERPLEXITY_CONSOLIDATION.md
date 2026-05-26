---
type: EPIC
version: 1.1.0
date: 2026-05-26T03:24:32+02:00
intent_hash: 0xEPIC_PERP_PERPLEXITY_CONSOLIDATION_20260526
status: in_progress
author: owl/kilo
branch: skills/consolidate-perp-to-perplexity
repo_path: D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS
kiva_status: phi-CPS WAL unavailable (warning on push)
---

# EPIC — Consolidation /perp → /perplexity (KIVA-enabled)

## Résumé
Consolider le répertoire historique `perp/` dans `perplexity/` pour faire de `perplexity/` la source de vérité unique des skills Perplexity (ENV1). Intégrer l'exécution locale CI via KIVA CLI (lint, index, scripts dry-run, tests).

## Contexte et état courant
- Branche de travail : skills/consolidate-perp-to-perplexity
- Travail en cours depuis : 2026-05-26
- Actions déjà effectuées (atomiques, commit par commit) :
  - Création archive/perp-archive/
  - Rapatriement vers `perplexity/` des fichiers suivants : SKILL_FORMAT_CANONICAL.md, generate-skills.ps1 (→ perplexity/scripts/), examples/brain-cortex.md, examples/ecosystem-maestro.md, analyse-repo-deepwiki.md, deepwiki_repo_enricher.md, fermi-legacy.md, hitl-ops.md, media-culture.md, new-pillars.md, nexus-map.md, pulse-infra.md, swarm-cli.md
  - Réconciliation: la version `perplexity/` a été conservée pour `comet-browser.md` et `data-vector.md` (suppression des copies `perp/`)
  - Archivage du fichier orphelin: `Nouveau document texte (2).txt` → archive/perp-archive/
  - Suppression du répertoire `perp/` (commit)
  - Ajout du PRD et EPIC (PRD/PRD_CONSOLIDATION_PERP_TO_PERPLEXITY.md)
  - Linter REPO-STANDARDS exécuté et corrections appliquées (création config/README.md)
  - Branche poussée vers origin (push succeeded, KIVA warning: phi-CPS WAL unavailable)

## Objectifs de l'EPIC
- Faire passer le repo en conformité RSS-v2 (REPO-STANDARDS)
- Centraliser tous les contents Perplexity dans `perplexity/`
- Valider localement avec KIVA CLI : lint, indexation dry-run, scripts dry-run, tests
- Ouvrir PR documentée et merger sur main après revue

## Tâches (décomposées)
1. Analyse et décision (COMPLET) — diffs, décisions pour doublons
2. Rapatriement atomique (COMPLET) — 14 fichiers + scripts
3. Archivage (COMPLET)
4. Suppression /perp (COMPLET)
5. Linter REPO-STANDARDS (COMPLET) — rss_lint.py --fix, config/ ajouté
6. Push branche (COMPLET) — KIVA phi-CPS reported WAL unavailable (warning)
7. Exécuter pipeline KIVA local (EN COURS/À FAIRE) — voir détails ci-dessous
8. Ouvrir PR sur GitHub (À FAIRE)
9. Revue & Merge (À FAIRE)
10. Nettoyage post-merge (À FAIRE)

## Pipeline KIVA local (à exécuter avant ouverture PR)
Commandes à lancer localement (KIVA runner / shell) :

- python D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\REPO-STANDARDS\\rss_lint.py --repo . --strict
- python scripts/index_skills.py --dry-run
- cmd /c powershell -ExecutionPolicy ByPass -File "perplexity\\scripts\\organize_perplexity.ps1" -WhatIf
- python -m pytest tests -q

Critères de succès KIVA : toutes les étapes retournent exit code 0. Joindre les logs KIVA au PR.

## Risques et mitigations (réactualisés)
- Hooks locaux ECOS/KIVA peuvent bloquer commits (ex: ecos-nexus-sync). Mitigation : corriger le test fautif ou utiliser --no-verify pour commits de préparation mais documenter et réparer avant merge.
- phi-CPS WAL unavailable → init KIVA WAL ou ignorer avec caution. Mitigation : exécuter `kiva phi-cps status` et init si nécessaire.
- Perte de contenu lors de mv/rm : mitigation appliquée via bundle backup et commits atomiques.

## Artefacts produits
- PRD: PRD/PRD_CONSOLIDATION_PERP_TO_PERPLEXITY.md
- EPIC: epics/EPIC_PERP_PERPLEXITY_CONSOLIDATION.md (ce fichier)
- Branch: skills/consolidate-perp-to-perplexity
- Archive: archive/perp-archive/
- Logs & diffs: diffs/ (à créer si besoin)

## Critères d'acceptation
- `perp/` absent ou remplacé par archive/périmétré (main)
- `perplexity/` contient tous les fichiers nécessaires (inventaire matching)
- rss_lint.py --strict passe (0 violation)
- KIVA local pipeline passe (lint, index dry-run, scripts dry-run, tests)
- PR mergée et branche supprimée

## Prochaine action autorisée (plan exécutable maintenant)
1. Exécuter les commandes KIVA listées ci-dessus et collecter les logs.
2. Mettre à jour le PRD/EPIC avec les résultats et attacher les logs.
3. Ouvrir PR et notifier reviewers.

---

# Environment details (injected)
- Current time: 2026-05-26T03:24:32+02:00
- Working directory: D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS
- Workspace root folder: D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS

---

*IntentHash: 0xEPIC_PERP_PERPLEXITY_CONSOLIDATION_20260526 | Version: 1.1.0 | Status: in_progress*
