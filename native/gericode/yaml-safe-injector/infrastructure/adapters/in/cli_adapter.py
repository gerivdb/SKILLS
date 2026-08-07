"""
Hexagonal Infrastructure Adapters — yaml-safe-injector
"""

from pathlib import Path
from typing import Protocol


class IYamlInjectionAdapter(Protocol):
    """Inbound adapter: exposes injection to CLI/MCP."""

    def execute(self, target_path: str, updates: dict, repo_name: str) -> dict:
        ...


class CLIYamlInjectionAdapter:
    """CLI adapter for yaml-safe-injector."""

    def execute(self, target_path: str, updates: dict, repo_name: str) -> dict:
        from yaml_safe_injector import inject_yaml
        result_path, diff = inject_yaml(Path(target_path), updates, repo_name=repo_name)
        return {"path": str(result_path), "diff": diff}
