"""
Gitignore Harmonizer
Harmonise les .gitignore pour supporter Hexagonal/BDD/ATDD.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import yaml

logger = logging.getLogger(__name__)


class GitignoreHarmonizerError(Exception):
    """Erreur d'harmonisation de .gitignore."""


class GitignoreHarmonizer:
    BROAD_PATTERNS = [
        "out/",
        "infrastructure/adapters/",
        "__pycache__/",
        "*.pyc",
    ]

    REPLACEMENTS = {
        "out/": "infrastructure/adapters/out/\ninfrastructure/adapters/in/",
        "infrastructure/adapters/": "# infrastructure/adapters/ is allowed\n# infrastructure/adapters/out/\n# infrastructure/adapters/in/",
    }

    def __init__(self, repo_path: Path) -> None:
        self.repo_path = repo_path
        self.gitignore_path = repo_path / ".gitignore"

    def harmonize(self, dry_run: bool = False) -> dict:
        """Harmonise le .gitignore."""
        report: dict = {
            "repo_path": str(self.repo_path),
            "gitignore_path": str(self.gitignore_path),
            "dry_run": dry_run,
            "broad_patterns_found": [],
            "replacements_made": [],
            "errors": [],
        }

        if not self.gitignore_path.exists():
            report["errors"].append(".gitignore not found")
            return report

        try:
            content = self.gitignore_path.read_text(encoding="utf-8")
        except Exception as exc:
            report["errors"].append(f"Cannot read .gitignore: {exc}")
            return report

        lines = content.splitlines()
        new_lines = []
        modified = False

        for line in lines:
            stripped = line.strip()
            if stripped in self.BROAD_PATTERNS:
                report["broad_patterns_found"].append(stripped)
                if stripped in self.REPLACEMENTS and not dry_run:
                    replacement = self.REPLACEMENTS[stripped]
                    new_lines.append(f"# {stripped} replaced by gitignore-harmonizer")
                    for rl in replacement.splitlines():
                        new_lines.append(rl)
                    report["replacements_made"].append(stripped)
                    modified = True
                else:
                    new_lines.append(f"# {stripped} would be replaced")
                    modified = True
            else:
                new_lines.append(line)

        if modified and not dry_run:
            try:
                self.gitignore_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
                logger.info(".gitignore harmonized: %d replacements", len(report["replacements_made"]))
            except Exception as exc:
                report["errors"].append(f"Cannot write .gitignore: {exc}")

        return report

    def detect_broad_patterns(self) -> list[str]:
        """Détecte les patterns trop larges."""
        if not self.gitignore_path.exists():
            return []

        try:
            content = self.gitignore_path.read_text(encoding="utf-8")
        except Exception:
            return []

        found = []
        for line in content.splitlines():
            stripped = line.strip()
            if stripped in self.BROAD_PATTERNS:
                found.append(stripped)
        return found
