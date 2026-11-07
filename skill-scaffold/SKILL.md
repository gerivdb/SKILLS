---
type: SKILL
version: "1.0.0"
status: active
date: "2026-08-07"
intent_hash: 0xSKILL_SKILL_SCAFFOLD_20260807
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/skill-scaffold/SKILL.md
---

# Skill — skill-scaffold

Générateur de skill respectant le design `skill-creation-tdd`.

## Objectifs
- Générer la structure complète d'un skill : `SKILL.md`, `<module>.py`, `tests/conftest.py`, `tests/test_<module>.py`.
- Auto-générer le frontmatter étendu.
- Pré-remplir les sections obligatoires.
- Générer des tests de base.
- Enregistrer automatiquement dans `registry.yaml`.

## Entrées
- `name`: nom du skill (kebab-case).
- `description`: description courte du skill.
- `citizen`: citoyen responsable.
- `layer`: couche logique (L4 par défaut).

## Sorties
- `Path`: chemin du répertoire du skill créé.

## Règles
- Le nom du skill doit être en kebab-case.
- Le frontmatter étendu est obligatoire.
- Les sections `## Tests`, `## Rôles`, `## Probes`, `## Critères`, `## Rollback` sont obligatoires.
- Les tests de dry-run et rollback sont obligatoires pour les skills d'écriture/modification.

## Tests
- `tests/test_skill_scaffold.py`: 100% passants requis.

## Probes
- P-301: 100% tests passants
- P-302: 0 corruption sur jeu de tests représentatif
- P-303: dry-run ne modifie pas le fichier
- P-304: rollback en < 30s
