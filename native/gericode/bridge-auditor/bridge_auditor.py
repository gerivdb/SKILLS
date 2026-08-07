"""
Bridge Auditor
Valide BRIDGES.yaml et détecte les orphelins et cycles.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import yaml

logger = logging.getLogger(__name__)


class BridgeAuditorError(Exception):
    """Erreur d'audit de bridges."""


class BridgeAuditor:
    def __init__(self, bridges_path: Path, known_repositories_path: Path) -> None:
        self.bridges_path = bridges_path
        self.known_repositories_path = known_repositories_path

    def audit(self) -> dict:
        """Audit complet des bridges."""
        report = {
            "orphaned_bridges": self._find_orphaned_bridges(),
            "missing_bridges": self._find_missing_bridges(),
            "cycles": self._find_cycles(),
            "errors": [],
            "warnings": [],
        }
        return report

    def _load_bridges(self) -> dict:
        data = yaml.safe_load(self.bridges_path.read_text(encoding="utf-8")) or {}
        return data.get("repos", {})

    def _load_known_repos(self) -> set[str]:
        data = yaml.safe_load(self.known_repositories_path.read_text(encoding="utf-8")) or {}
        repos = set()
        for key, value in data.items():
            if isinstance(key, str) and key.endswith("_REPOS") and isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and "name" in item:
                        repos.add(item["name"].upper())
        return repos

    def _find_orphaned_bridges(self) -> list[str]:
        """Trouve les bridges vers des repos inexistants."""
        bridges = self._load_bridges()
        known_repos = self._load_known_repos()
        orphaned = []
        for repo_id, bridge_data in bridges.items():
            full_name = bridge_data.get("full_name", "")
            if full_name:
                repo_name = full_name.replace("gerivdb/", "").upper()
                if repo_name not in known_repos:
                    orphaned.append(repo_id)
        return orphaned

    def _find_missing_bridges(self) -> list[str]:
        """Trouve les repos actifs sans bridge."""
        bridges = self._load_bridges()
        known_repos = self._load_known_repos()
        missing = []
        for repo in known_repos:
            if repo not in bridges:
                missing.append(repo)
        return missing

    def _find_cycles(self) -> list[list[str]]:
        """Détecte les cycles dans les bridges."""
        bridges = self._load_bridges()
        graph = {}
        for repo_id, bridge_data in bridges.items():
            graph[repo_id] = bridge_data.get("bridges", [])

        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node: str, path: list[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path)
                elif neighbor in rec_stack:
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])

            path.pop()
            rec_stack.remove(node)

        for node in graph:
            if node not in visited:
                dfs(node, [])

        return cycles
