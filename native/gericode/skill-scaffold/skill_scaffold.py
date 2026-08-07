"""Skill — skill-scaffold

Générateur de skill respectant le design skill-creation-tdd.
Crée la structure complète : SKILL.md, module.py, tests/conftest.py, tests/test_<module>.py
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)


class SkillScaffoldError(Exception):
    """Erreur lors du scaffolding de skill."""


def scaffold_skill(
    skill_name: str,
    description: str,
    citizen: str = "L2-PLATFORM",
    layer: str = "L4",
    target_dir: Path | None = None,
) -> Path:
    """Crée la structure complète d'un skill respectant TDD.

    Args:
        skill_name: Nom du skill (ex: my-skill).
        description: Description courte du skill.
        citizen: Citizen responsable.
        layer: Couche logique.
        target_dir: Répertoire parent (.kilo/skills/ par défaut).

    Returns:
        Chemin du répertoire du skill créé.

    Raises:
        SkillScaffoldError: Si le répertoire existe déjà ou si la création échoue.
    """
    if target_dir is None:
        target_dir = Path(".kilo/skills")

    skill_dir = target_dir / skill_name
    if skill_dir.exists():
        raise SkillScaffoldError(f"Le skill {skill_name} existe déjà: {skill_dir}")

    skill_dir.mkdir(parents=True, exist_ok=True)
    tests_dir = skill_dir / "tests"
    tests_dir.mkdir(exist_ok=True)

    module_name = skill_name.replace("-", "_")

    # SKILL.md
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(
        f"""---
name: {skill_name}
description: >
  {description}
version: "1.0.0"
status: active
intent_hash: 0xSKILL_{skill_name.upper().replace('-', '_')}_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/{skill_name}/SKILL.md
triggers:
  - "{skill_name}"
tools:
  - bash
  - read
  - write
citizen: "{citizen}"
layer: "{layer}"
---

# Skill — {skill_name}

> **Verdict** : **SKILL D'EXÉCUTION** — {description}

---

## Objectif

À définir.

---

## Déclencheur

À définir.

---

## Entrées

| Entrée | Type | Description |
|--------|------|-------------|
| À définir | | |

---

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| À définir | | |

---

## Règles

À définir.

---

## Exemple d'usage

À définir.

---

## Tests

| Test | Description | Attend |
|------|-------------|--------|
| `test_placeholder` | Placeholder | True |

---

## Référence ADR

- **ADR** : ADR-2026-08-07-001-{skill_name.upper().replace('-', '_')}
- **IntentHash** : 0xADR_{skill_name.upper().replace('-', '_')}_20260807
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| À définir | |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-701    SKILL.md contient la table Tests                                    |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| [OK]    SKILL.md avec frontmatter étendu                                    |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Supprimer le répertoire du skill.
2. Logger dans WAL.
""",
        encoding="utf-8",
    )

    # Module Python
    module_py = skill_dir / f"{module_name}.py"
    module_py.write_text(
        f"""\"\"\"Module — {skill_name}\"\"\"

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def run() -> None:
    \"\"\"Point d'entrée du skill.\"\"\"
    logger.info("{skill_name} skill running")
""",
        encoding="utf-8",
    )

    # tests/conftest.py
    conftest_py = tests_dir / "conftest.py"
    conftest_py.write_text(
        f"""\"\"\"conftest.py pour {skill_name}.\"\"\"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
""",
        encoding="utf-8",
    )

    # tests/test_<module>.py
    test_py = tests_dir / f"test_{module_name}.py"
    test_py.write_text(
        f"""\"\"\"Tests pour {skill_name}.\"\"\"

from __future__ import annotations

import pytest

from {module_name} import run


def test_placeholder() -> None:
    \"\"\"Placeholder test.\"\"\"
    assert True
""",
        encoding="utf-8",
    )

    logger.info("Skill créé: %s", skill_dir)
    return skill_dir
