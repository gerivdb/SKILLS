---
name: skill-scaffold
description: "Générateur de skill respectant le design skill-creation-tdd. Crée la structure complète : SKILL.md, module.py, tests/conftest.py, tests/test_<module>.py"
version: "1.0.0"
status: active
intent_hash: 0xSKILL_SKILL_SCAFFOLD_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/skill-scaffold/SKILL.md
triggers:
  - "créer skill"
  - "nouveau skill"
  - "scaffold skill"
tools:
  - bash
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill — skill-scaffold

> **Verdict** : **SKILL D'EXÉCUTION** — Générateur de skill respectant TDD.

---

## Objectif

Créer la structure complète d'un skill en respectant le design `skill-creation-tdd`.

---

## Déclencheur

- Création d'un nouveau skill
- Génération de squelette de skill

---

## Entrées

| Entrée | Type | Description |
|--------|------|-------------|
| `skill_name` | str | Nom du skill (ex: my-skill) |
| `description` | str | Description courte |
| `citizen` | str | Citizen responsable |
| `layer` | str | Couche logique |

---

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `skill_dir` | Path | Répertoire du skill créé |

---

## Règles

1. Frontmatter étendu obligatoire
2. Sections obligatoires pré-remplies
3. Tests de base générés
4. Registration automatique dans `registry.yaml`

---

## Exemple d'usage

```python
from pathlib import Path
from skill_scaffold import scaffold_skill

scaffold_skill(
    skill_name="my-skill",
    description="Mon skill",
    citizen="DEV-EXPERIENCE",
    layer="L4",
)
```

---

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_scaffold_creates_directory` | Crée le répertoire du skill | Répertoire existe |
| `test_scaffold_creates_files` | Crée SKILL.md, module.py, tests | Tous les fichiers existent |
| `test_scaffold_raises_if_exists` | Lève erreur si skill existe | SkillScaffoldError |

---

## Référence ADR

- **ADR** : ADR-2026-08-07-005-SKILL_SCAFFOLD
- **IntentHash** : 0xADR_SKILL_SCAFFOLD_20260807
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `DEV-EXPERIENCE` | Garant des conventions TDD |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-710    scaffold_skill crée un répertoire valide                           |
| P-711    SKILL.md avec frontmatter étendu généré                            |
| P-712    tests/conftest.py généré                                          |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          Répertoire skill créé                                            |
| ✓          SKILL.md avec frontmatter étendu                                 |
| ✓          tests/conftest.py présent                                        |
| ✓          pytest vert                                                      |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Supprimer le répertoire du skill.
2. Logger dans WAL.

---

## Références

- `skill-creation-tdd.yaml`
- `mcp-access-repair/SKILL.md`
