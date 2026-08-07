"""Skill — ecosystem-probe

Découverte automatique de l'écosystème avant toute session.
Scanne skills, workflows, citizens, designs et produit un index JSON.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class EcosystemItem:
    type: str
    name: str
    path: str
    intent_hash: str = ""


@dataclass
class EcosystemIndex:
    skills: list[EcosystemItem] = field(default_factory=list)
    workflows: list[EcosystemItem] = field(default_factory=list)
    citizens: list[EcosystemItem] = field(default_factory=list)
    designs: list[EcosystemItem] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "skills": [item.__dict__ for item in self.skills],
            "workflows": [item.__dict__ for item in self.workflows],
            "citizens": [item.__dict__ for item in self.citizens],
            "designs": [item.__dict__ for item in self.designs],
        }


class EcosystemProbe:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.index = EcosystemIndex()

    def scan_all(self) -> EcosystemIndex:
        """Scanne l'écosystème complet."""
        self._scan_skills()
        self._scan_workflows()
        self._scan_citizens()
        self._scan_designs()
        return self.index

    def _scan_skills(self) -> None:
        skills_dir = self.repo_root / ".kilo" / "skills"
        if not skills_dir.exists():
            return
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                self.index.skills.append(
                    EcosystemItem(
                        type="skill",
                        name=skill_dir.name,
                        path=str(skill_dir),
                    )
                )

    def _scan_workflows(self) -> None:
        workflows_dir = self.repo_root / ".kilo" / "workflows"
        if not workflows_dir.exists():
            return
        for workflow_file in workflows_dir.glob("*.py"):
            self.index.workflows.append(
                EcosystemItem(
                    type="workflow",
                    name=workflow_file.stem,
                    path=str(workflow_file),
                )
            )

    def _scan_citizens(self) -> None:
        citizens_file = self.repo_root / "act-protocol" / "citizens.yaml"
        if not citizens_file.exists():
            return
        self.index.citizens.append(
            EcosystemItem(
                type="citizens",
                name="citizens",
                path=str(citizens_file),
            )
        )

    def _scan_designs(self) -> None:
        designs_dir = self.repo_root / "unified-design" / "designs"
        if not designs_dir.exists():
            return
        for design_file in designs_dir.glob("*.yaml"):
            self.index.designs.append(
                EcosystemItem(
                    type="design",
                    name=design_file.stem,
                    path=str(design_file),
                )
            )

    def save(self, output_path: Path) -> None:
        """Sauvegarde l'index en JSON."""
        output_path.write_text(
            json.dumps(self.index.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
