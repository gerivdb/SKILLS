"""
Citizenship Auditor
Valide citizens.yaml ↔ known_repositories.yaml ↔ VERSES.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import yaml

logger = logging.getLogger(__name__)


class CitizenshipAuditorError(Exception):
    """Erreur d'audit de citoyenneté."""


class CitizenshipAuditor:
    def __init__(
        self,
        known_repositories_path: Path,
        citizens_yaml_path: Path,
        verses_dir: Path,
        skills_dir: Path,
        registry_yaml_path: Path,
    ) -> None:
        self.known_repositories_path = known_repositories_path
        self.citizens_yaml_path = citizens_yaml_path
        self.verses_dir = verses_dir
        self.skills_dir = skills_dir
        self.registry_yaml_path = registry_yaml_path

    def audit(self) -> dict:
        """Audit complet de la citoyenneté."""
        report = {
            "p801_repos_are_citizens": self._check_p801(),
            "p802_citizens_have_verses": self._check_p802(),
            "p806_skills_in_registry": self._check_p806(),
            "p807_registry_has_source_repo": self._check_p807(),
            "errors": [],
            "warnings": [],
        }
        return report

    def _load_known_repos(self) -> set[str]:
        data = yaml.safe_load(self.known_repositories_path.read_text(encoding="utf-8")) or {}
        repos = set()
        for key, value in data.items():
            if isinstance(key, str) and key.endswith("_REPOS") and isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and "name" in item:
                        repos.add(item["name"])
        return repos

    def _load_citizens(self) -> set[str]:
        data = yaml.safe_load(self.citizens_yaml_path.read_text(encoding="utf-8")) or {}
        return {c["id"] for c in data.get("citizens", []) if "id" in c}

    def _load_verses(self) -> set[str]:
        if not self.verses_dir.exists():
            return set()
        return {p.stem.replace("-verse", "") for p in self.verses_dir.glob("*-verse.md")}

    def _load_registry_skills(self) -> set[str]:
        data = yaml.safe_load(self.registry_yaml_path.read_text(encoding="utf-8")) or {}
        return {s["name"] for s in (data.get("skills") or []) if "name" in s}

    def _load_local_skills(self) -> set[str]:
        if not self.skills_dir.exists():
            return set()
        return {d.name for d in self.skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()}

    def _check_p801(self) -> dict:
        known_repos = self._load_known_repos()
        citizens = self._load_citizens()
        missing = known_repos - citizens
        return {"passed": len(missing) == 0, "missing": sorted(missing)}

    def _check_p802(self) -> dict:
        citizens = self._load_citizens()
        verses = self._load_verses()
        # Match citizen ID to verse stem
        missing = [c for c in citizens if c.lower() not in verses]
        return {"passed": len(missing) == 0, "missing": missing}

    def _check_p806(self) -> dict:
        local_skills = self._load_local_skills()
        registry_skills = self._load_registry_skills()
        missing = local_skills - registry_skills
        return {"passed": len(missing) == 0, "missing": sorted(missing)}

    def _check_p807(self) -> dict:
        data = yaml.safe_load(self.registry_yaml_path.read_text(encoding="utf-8")) or {}
        missing_source_repo = []
        for skill in (data.get("skills") or []):
            if not skill.get("source_repo"):
                missing_source_repo.append(skill.get("name", "unknown"))
        return {"passed": len(missing_source_repo) == 0, "missing": missing_source_repo}
