---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-07"
intent_hash: 0xSKILL_ECOSYSTEM_BRAIN_20260807
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/ecosystem-brain/SKILL.md
---

# Skill — ecosystem-brain

Orchestrateur de découverte de l'écosystème. Utilise `ecosystem-probe` pour scanner et indexer.

## Objectifs
- Scanner l'écosystème avant toute session.
- Vérifier si le besoin est déjà couvert par un skill/citizen/workflow existant.
- Proposer la création via `skill-scaffold` si le besoin n'est pas couvert.

## Entrées
- `force_rescan`: booléen, forcer le re-scan même si l'index est récent.
- `need`: description du besoin à couvrir.

## Sorties
- `dict`: résultat de la découverte avec recommandation.

## Règles
- Toujours scanner avant d'implémenter un nouveau skill/workflow/citizen.
- Si le besoin est déjà couvert → réutiliser, pas de duplication.
- Si le besoin n'est pas couvert → proposer création via `skill-scaffold`.

## Tests
- `tests/test_ecosystem_brain.py`: 100% passants requis.

## Probes
- P-601: scan complet en < 30s
- P-602: 0 skill manquant dans l'index
- P-603: 0 duplication détectée
