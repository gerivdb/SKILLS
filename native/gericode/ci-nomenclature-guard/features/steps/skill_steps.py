"""BDD steps for ci-nomenclature-guard."""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SkillSteps:
    """BDD steps for ci-nomenclature-guard skill."""

    def __init__(self, skill_dir: Path) -> None:
        self.skill_dir = skill_dir

    def validate_skill_structure(self) -> bool:
        """Validate skill has required structure."""
        required = ["SKILL.md", "features", "application", "domain", "infrastructure"]
        return all((self.skill_dir / r).exists() for r in required)

    def check_contracts(self) -> bool:
        """Check contracts are present."""
        return (self.skill_dir / "acceptance" / "contract.yaml").exists()
