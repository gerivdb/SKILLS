"""
Filesystem Adapter for Meta Coherence Validator.

Implements reference checking by reading actual files from the filesystem.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Set, Optional
from ...domain.value_objects.reference_vo import Reference


class FilesystemPrdMocReader:
    """Read PRD MOC documents from the filesystem."""

    def __init__(self, base_path: Path):
        self.base_path = base_path

    def read_prd_mocs(self, paths: List[Path]) -> List[Dict]:
        """Read PRD MOC documents from given paths."""
        prd_mocs = []
        for path in paths:
            if path.exists() and path.is_file():
                try:
                    content = path.read_text(encoding="utf-8")
                    title = self._extract_title(content)
                    prd_mocs.append({
                        "path": str(path),
                        "title": title,
                        "content": content,
                    })
                except Exception as e:
                    prd_mocs.append({
                        "path": str(path),
                        "title": path.name,
                        "content": "",
                        "error": str(e),
                    })
        return prd_mocs

    def _extract_title(self, content: str) -> str:
        """Extract title from PRD MOC markdown."""
        match = re.search(r"^# (.+)$", content, re.MULTILINE)
        return match.group(1) if match else "Unknown"


class FilesystemReferenceChecker:
    """Check reference existence using the filesystem."""

    def __init__(
        self,
        unified_design_path: Path,
        ontology_path: Path,
        skills_base_path: Path,
        boot_sequence_path: Path,
        governance_hub_path: Path,
    ):
        self.unified_design_path = unified_design_path
        self.ontology_path = ontology_path
        self.skills_base_path = skills_base_path
        self.boot_sequence_path = boot_sequence_path
        self.governance_hub_path = governance_hub_path

        # Cache for existence checks
        self._design_cache: Set[str] = set()
        self._skill_cache: Set[str] = set()
        self._boot_steps: Set[str] = set()
        self._ontology_concepts: Set[str] = set()
        self._ontology_citizens: Set[str] = set()

        self._load_caches()

    def _load_caches(self) -> None:
        """Load caches for faster existence checks."""
        # Cache designs
        if self.unified_design_path.exists():
            for f in self.unified_design_path.rglob("*.yaml"):
                rel = f.relative_to(self.unified_design_path)
                self._design_cache.add(str(rel))

        # Cache skills
        if self.skills_base_path.exists():
            for d in self.skills_base_path.rglob("SKILL.md"):
                rel = d.parent.relative_to(self.skills_base_path)
                self._skill_cache.add(str(rel))

        # Cache boot steps
        if self.boot_sequence_path.exists():
            content = self.boot_sequence_path.read_text(encoding="utf-8")
            steps = re.findall(r"^### (BOOT-[^\s]+)", content, re.MULTILINE)
            self._boot_steps.update(steps)

        # Cache ontology concepts and citizens
        self._load_ontology_caches()

    def _load_ontology_caches(self) -> None:
        """Load ontology concept and citizen caches."""
        ontology_yaml = self.ontology_path / "ONTOLOGY.yaml"
        if not ontology_yaml.exists():
            return

        try:
            import yaml
            with open(ontology_yaml, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if data and "concepts" in data:
                for concept in data["concepts"]:
                    if isinstance(concept, dict):
                        self._ontology_concepts.add(concept.get("id", ""))
                    elif isinstance(concept, str):
                        self._ontology_concepts.add(concept)

            if data and "citizens" in data:
                for citizen in data["citizens"]:
                    if isinstance(citizen, dict):
                        self._ontology_citizens.add(citizen.get("id", ""))
                    elif isinstance(citizen, str):
                        self._ontology_citizens.add(citizen)
        except Exception:
            pass

    def check_design_exists(self, design_path: str) -> bool:
        """Check if a design file exists."""
        normalized = design_path.replace("unified-design/designs/", "")
        return normalized in self._design_cache or design_path in self._design_cache

    def check_concept_exists(self, concept_id: str) -> bool:
        """Check if a concept exists in ONTOLOGY."""
        return concept_id in self._ontology_concepts

    def check_skill_exists(self, skill_path: str) -> bool:
        """Check if a skill directory exists."""
        # Normalize path
        normalized = skill_path.replace("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/native/gericode/", "")
        normalized = normalized.replace("D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS\\native\\gericode\\", "")
        return normalized in self._skill_cache

    def check_citizen_exists(self, citizen_id: str) -> bool:
        """Check if a citizen exists in ONTOLOGY."""
        return citizen_id in self._ontology_citizens

    def check_boot_step_exists(self, step_name: str) -> bool:
        """Check if a boot step exists in session-boot-sequence.md."""
        return step_name in self._boot_steps

    def check_prd_moc_exists(self, prd_moc_path: str) -> bool:
        """Check if a PRD MOC file exists."""
        # Remove leading act-protocol/ if present
        path = prd_moc_path
        if path.startswith("act-protocol/"):
            path = path[len("act-protocol/"):]
        full_path = self.base_path / "act-protocol" / "PRD" / path
        return full_path.exists()

    def check_adr_exists(self, adr_id: str) -> bool:
        """Check if an ADR exists."""
        adr_path = self.governance_hub_path / "ADR" / f"{adr_id}.md"
        return adr_path.exists()

    def check_ontology_file_exists(self, ontology_path: str) -> bool:
        """Check if an ontology YAML file exists."""
        full_path = self.ontology_path / ontology_path
        return full_path.exists()
