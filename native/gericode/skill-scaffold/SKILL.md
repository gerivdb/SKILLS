---
name: skill-scaffold
description: "Generateur de skill respectant le design skill-creation-tdd. Cree la structure complete : SKILL.md, module.py, tests/conftest.py, tests/test_<module>.py"
version: "1.0.0"
status: active
intent_hash: 0xSKILL_SKILL_SCAFFOLD_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/skill-scaffold/SKILL.md
triggers:
  - "creer skill"
  - "nouveau skill"
  - "scaffold skill"
tools:
  - bash
  - write
citizen: "DEV-EXPERIENCE"
layer: "L4"
---

# Skill - skill-scaffold

> **Verdict** : **SKILL D'EXECUTION** - Generateur de skill respectant TDD.

---

## Objectif

Creer la structure complete d'un skill en respectant le design `skill-creation-tdd`.

---

## Declencheur

- Creation d'un nouveau skill
- Generation de squelette de skill

---

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `skill_name` | str | Nom du skill (ex: my-skill) |
| `description` | str | Description courte |
| `citizen` | str | Citizen responsable |
| `layer` | str | Couche logique |

---

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `skill_dir` | Path | Repertoire du skill cree |

---

## Regles

1. Frontmatter etendu obligatoire
2. Sections obligatoires pre-remplies
3. Tests de base generes
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
| `test_scaffold_creates_directory` | Cree le repertoire du skill | Repertoire existe |
| `test_scaffold_creates_files` | Cree SKILL.md, module.py, tests | Tous les fichiers existent |
| `test_scaffold_raises_if_exists` | Leve erreur si skill existe | SkillScaffoldError |

---

## Reference ADR

- **ADR** : ADR-2026-08-07-005-SKILL_SCAFFOLD
- **IntentHash** : 0xADR_SKILL_SCAFFOLD_20260807
- **Depot** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed

---

## Roles

| Role | Responsabilite |
|------|----------------|
| `DEV-EXPERIENCE` | Garant des conventions TDD |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-710    scaffold_skill cree un repertoire valide                           |
| P-711    SKILL.md avec frontmatter etendu genere                            |
| P-712    tests/conftest.py genere                                          |
+-----------------------------------------------------------------------------+
```

---

## Criteres

```ascii
+-----------------------------------------------------------------------------+
| CRITERE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| [OK]          Repertoire skill cree                                            |
| [OK]          SKILL.md avec frontmatter etendu                                 |
| [OK]          tests/conftest.py present                                        |
| [OK]          pytest vert                                                      |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Supprimer le repertoire du skill.
2. Logger dans WAL.

---

## References

- `skill-creation-tdd.yaml`
- `mcp-access-repair/SKILL.md`
