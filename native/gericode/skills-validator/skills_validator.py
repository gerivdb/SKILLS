"""
Skills Validator
Valide tous les skills contre la taxonomie SKILLS/TAXONOMY.md.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import yaml

logger = logging.getLogger(__name__)


class SkillsValidatorError(Exception):
    """Erreur de validation de skill."""


class SkillValidationError:
    def __init__(self, skill_name: str, message: str, severity: Literal["error", "warning"] = "error") -> None:
        self.skill_name = skill_name
        self.message = message
        self.severity = severity

    def __repr__(self) -> str:
        return f"SkillValidationError({self.skill_name}: {self.message})"


class SkillsValidator:
    REQUIRED_FIELDS = {"name", "description", "triggers", "domain", "version", "author", "license", "status"}
    VALID_TYPES = {"foundational", "domain", "external"}
    VALID_STATUSES = {"active", "draft", "deprecated"}

    def __init__(self, skills_dir: Path, taxonomy_path: Path, registry_path: Path) -> None:
        self.skills_dir = skills_dir
        self.taxonomy_path = taxonomy_path
        self.registry_path = registry_path

    def validate_all(self) -> dict:
        """Valide tous les skills."""
        errors: list[SkillValidationError] = []
        warnings: list[SkillValidationError] = []
        skill_names: list[str] = []

        for skill_md in self.skills_dir.rglob("SKILL.md"):
            skill_errors, skill_warnings = self._validate_skill(skill_md)
            errors.extend(skill_errors)
            warnings.extend(skill_warnings)
            # Extract name from frontmatter for duplicate detection
            try:
                content = skill_md.read_text(encoding="utf-8")
                if content.startswith("---"):
                    end = content.find("---", 3)
                    if end != -1:
                        frontmatter = yaml.safe_load(content[3:end]) or {}
                        if "name" in frontmatter:
                            skill_names.append(frontmatter["name"])
            except Exception:
                pass

        # Check duplicates based on frontmatter name
        seen = set()
        duplicates = []
        for name in skill_names:
            if name in seen:
                duplicates.append(name)
            seen.add(name)

        for dup in duplicates:
            errors.append(SkillValidationError(dup, "Duplicate skill name", severity="error"))

        return {
            "total_skills": len(skill_names),
            "errors": [{"skill": e.skill_name, "message": e.message} for e in errors],
            "warnings": [{"skill": w.skill_name, "message": w.message} for w in warnings],
            "duplicates": duplicates,
        }

    def _validate_skill(self, skill_md: Path) -> tuple[list[SkillValidationError], list[SkillValidationError]]:
        """Valide un SKILL.md."""
        errors: list[SkillValidationError] = []
        warnings: list[SkillValidationError] = []
        skill_name = skill_md.parent.name

        try:
            content = skill_md.read_text(encoding="utf-8")
        except Exception as exc:
            errors.append(SkillValidationError(skill_name, f"Cannot read file: {exc}"))
            return errors, warnings

        # Extract frontmatter
        if not content.startswith("---"):
            errors.append(SkillValidationError(skill_name, "Missing YAML frontmatter"))
            return errors, warnings

        end = content.find("---", 3)
        if end == -1:
            errors.append(SkillValidationError(skill_name, "Unclosed YAML frontmatter"))
            return errors, warnings

        frontmatter_text = content[3:end]
        try:
            frontmatter = yaml.safe_load(frontmatter_text) or {}
        except Exception as exc:
            errors.append(SkillValidationError(skill_name, f"Invalid YAML frontmatter: {exc}"))
            return errors, warnings

        # Check required fields
        missing = self.REQUIRED_FIELDS - set(frontmatter.keys())
        if missing:
            errors.append(SkillValidationError(skill_name, f"Missing fields: {sorted(missing)}"))

        # Check type
        skill_type = frontmatter.get("type")
        if skill_type and skill_type not in self.VALID_TYPES:
            errors.append(SkillValidationError(skill_name, f"Invalid type: {skill_type}"))

        # Check status
        status = frontmatter.get("status")
        if status and status not in self.VALID_STATUSES:
            errors.append(SkillValidationError(skill_name, f"Invalid status: {status}"))

        # Check triggers
        triggers = frontmatter.get("triggers", [])
        if not triggers:
            errors.append(SkillValidationError(skill_name, "Empty triggers"))

        # Check path exists
        path = frontmatter.get("path")
        if path:
            # Path is relative to SKILLS repo
            full_path = self.skills_dir.parent / path
            if not full_path.exists():
                warnings.append(SkillValidationError(skill_name, f"Path does not exist: {path}", severity="warning"))

        return errors, warnings
