"""
Registry Prune
Nettoie les entrées orphelines dans tous les registres.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import yaml

logger = logging.getLogger(__name__)


class RegistryPruneError(Exception):
    """Erreur de prune des registres."""


class RegistryPrune:
    def __init__(
        self,
        registry_yaml_path: Path,
        registry_json_path: Path,
        citizens_yaml_path: Path,
        bridges_path: Path,
        known_repositories_path: Path,
    ) -> None:
        self.registry_yaml_path = registry_yaml_path
        self.registry_json_path = registry_json_path
        self.citizens_yaml_path = citizens_yaml_path
        self.bridges_path = bridges_path
        self.known_repositories_path = known_repositories_path

    def prune(self, dry_run: bool = False) -> dict:
        """Nettoie tous les registres."""
        report: dict = {
            "dry_run": dry_run,
            "registry_yaml_pruned": 0,
            "registry_json_pruned": 0,
            "citizens_yaml_pruned": 0,
            "bridges_yaml_pruned": 0,
            "errors": [],
            "warnings": [],
        }

        try:
            # Load all registries
            known_repos = self._load_known_repositories()
            registry_yaml = self._load_registry_yaml()
            citizens = self._load_citizens()
            bridges = self._load_bridges()

            # Prune REGISTRY.yaml
            pruned_yaml = self._prune_registry_yaml(registry_yaml, known_repos, dry_run=dry_run)
            report["registry_yaml_pruned"] = pruned_yaml

            # Prune registry.json
            pruned_json = self._prune_registry_json(known_repos, dry_run=dry_run)
            report["registry_json_pruned"] = pruned_json

            # Prune citizens.yaml
            pruned_citizens = self._prune_citizens(citizens, known_repos, dry_run=dry_run)
            report["citizens_yaml_pruned"] = pruned_citizens

            # Prune BRIDGES.yaml
            pruned_bridges = self._prune_bridges(bridges, known_repos, dry_run=dry_run)
            report["bridges_yaml_pruned"] = pruned_bridges

            report["status"] = "OK"
        except Exception as exc:
            report["errors"].append(str(exc))
            report["status"] = "FAILED"

        return report

    def _load_known_repositories(self) -> set[str]:
        data = yaml.safe_load(self.known_repositories_path.read_text(encoding="utf-8")) or {}
        repos = set()
        for key, value in data.items():
            if isinstance(key, str) and key.endswith("_REPOS") and isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and "name" in item:
                        repos.add(item["name"].upper())
        return repos

    def _load_registry_yaml(self) -> dict:
        data = yaml.safe_load(self.registry_yaml_path.read_text(encoding="utf-8")) or {}
        return data

    def _load_citizens(self) -> dict:
        data = yaml.safe_load(self.citizens_yaml_path.read_text(encoding="utf-8")) or {}
        return data

    def _load_bridges(self) -> dict:
        data = yaml.safe_load(self.bridges_path.read_text(encoding="utf-8")) or {}
        return data

    def _prune_registry_yaml(self, data: dict, known_repos: set[str], dry_run: bool = False) -> int:
        """Supprime les skills dont le source_repo n'existe plus."""
        if "skills" not in data or data["skills"] is None:
            return 0

        original_count = len(data["skills"])
        pruned = []
        for skill in data["skills"]:
            source_repo = skill.get("source_repo", "")
            if source_repo:
                repo_name = source_repo.replace("gerivdb/", "").upper()
                if repo_name not in known_repos:
                    if not dry_run:
                        pruned.append(skill)
                    continue
            data["skills"].append(skill)

        if not dry_run:
            data["skills"] = [s for s in data["skills"] if s not in pruned]

        return len(pruned)

    def _prune_registry_json(self, known_repos: set[str], dry_run: bool = False) -> int:
        """Placeholder: prune registry.json."""
        return 0

    def _prune_citizens(self, data: dict, known_repos: set[str], dry_run: bool = False) -> int:
        """Supprime les citizens dont le repo n'existe plus."""
        if "citizens" not in data or data["citizens"] is None:
            return 0

        original_count = len(data["citizens"])
        if not dry_run:
            data["citizens"] = [c for c in data["citizens"] if c.get("id", "").upper() in known_repos]
        return max(0, original_count - len(data["citizens"]))

    def _prune_bridges(self, data: dict, known_repos: set[str], dry_run: bool = False) -> int:
        """Supprime les bridges dont le repo n'existe plus."""
        if "repos" not in data or data["repos"] is None:
            return 0

        original_count = len(data["repos"])
        if not dry_run:
            data["repos"] = {k: v for k, v in data["repos"].items() if k.upper() in known_repos}
        return max(0, original_count - len(data["repos"]))
