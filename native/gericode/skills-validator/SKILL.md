---
name: skills-validator
description: "Valide tous les skills de l'écosystème contre la taxonomie SKILLS/TAXONOMY.md et détecte les anomalies de frontmatter, chemins et doublons."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_SKILLS_VALIDATOR_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/skills-validator/SKILL.md
triggers:
  - "validate skills"
  - "skills lint"
  - "taxonomy check"
tools:
  - bash
  - read
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill — skills-validator

> **Verdict** : **SKILL D'EXÉCUTION** — Valide la conformité des skills à la taxonomie.

---

## Objectif

Valider tous les skills contre `SKILLS/TAXONOMY.md` : frontmatter, champs obligatoires, triggers, type, status, doublons, chemins.

---

## Déclencheur

- CI/CD : validation avant commit
- ARGUS : détection d'anomalies
- MOX : vérification avant merge

---

## Entrées

 | Entrée | Type | Description |
 |--------|------|-------------|
 | `skills_dir` | Path | Répertoire `.kilo/skills/` |
 | `taxonomy_path` | Path | Chemin vers `SKILLS/TAXONOMY.md` |
 | `registry_path` | Path | Chemin vers `SKILLS/REGISTRY.yaml` |

---

## Sorties

 | Sortie | Type | Description |
 |--------|------|-------------|
 | `validation_report` | dict | Rapport de validation |
 | `errors` | list | Erreurs critiques |
 | `warnings` | list | Avertissements |

---

## Règles

1. Frontmatter YAML valide
2. Champs obligatoires présents : `name`, `description`, `triggers`, `domain`, `version`, `author`, `license`, `status`
3. `triggers` non vide
4. `type` ∈ {foundational, domain, external}
5. `status` ∈ {active, draft, deprecated}
6. Pas de doublons de `name`
7. `path` existe dans le filesystem

---

## Exemple d'usage

```python
from pathlib import Path
from skills_validator import SkillsValidator

validator = SkillsValidator(
    skills_dir=Path(".kilo/skills"),
    taxonomy_path=Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/TAXONOMY.md"),
    registry_path=Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/REGISTRY.yaml"),
)

report = validator.validate_all()
print(report)
```

---

## Tests

 | Test | Description | Attend |
 |------|-------------|--------|
 | `test_validate_valid_skill` | Skill valide | 0 erreur |
 | `test_validate_missing_field` | Champ manquant | Erreur détectée |
 | `test_detect_duplicate_names` | Doublon de nom | Erreur détectée |
 | `test_validate_all_skills` | Tous les skills | Rapport complet |

---

## Probes

 ```ascii
 +-----------------------------------------------------------------------------+
 | PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
 +-----------------------------------------------------------------------------+
 | P-903    100% des skills ont un frontmatter valide                          |
 | P-904    0 doublon de nom                                                  |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Critères

 ```ascii
 +-----------------------------------------------------------------------------+
 | CRITÈRE    DESCRIPTION                                                      |
 +-----------------------------------------------------------------------------+
 | ✓          skills-validator fonctionne                                      |
 | ✓          P-903 passe                                                      |
 | ✓          P-904 passe                                                      |
 +-----------------------------------------------------------------------------+
 ```

 ---

 ## Références

 - `PRD-MOC-AUTOMATED-DEVELOPMENT-FRAMEWORK-2026-08-07.md`
 - `SKILLS/TAXONOMY.md`
 - `SKILLS/REGISTRY.yaml`
