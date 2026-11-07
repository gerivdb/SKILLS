---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-07"
intent_hash: 0xSKILL_ECOSYSTEM_PROBE_20260807
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/ecosystem-probe/SKILL.md
---

# Skill — ecosystem-probe

Scanner l'écosystème et produire un index des skills, workflows, citizens et designs.

## Objectifs
- Scanner `.kilo/skills/`, `.kilo/workflows/`, `citizens/`, `designs/`.
- Produire `ecosystem-index.json` à la racine du repo.
- Vérifier la découvrabilité des skills (présence dans `registry.yaml`).

## Entrées
- `scan_all`: booléen, scanner tous les répertoires.
- `output_path`: chemin de sortie pour `ecosystem-index.json`.

## Sorties
- `dict`: index de l'écosystème.

## Règles
- Toute erreur de scan est loggée mais n'arrête pas le processus.
- Les skills sans `SKILL.md` sont signalés mais inclus dans l'index.
- Le fichier de sortie est écrasé à chaque scan.

## Tests
- `tests/test_ecosystem_probe.py`: 100% passants requis.

## Probes
- P-601: scan complet en < 30s
- P-602: 0 skill manquant dans l'index
- P-603: 0 workflow manquant dans l'index
