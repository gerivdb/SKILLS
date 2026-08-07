"""
Hexagonal Adapters — sot-registry-guardian
"""

from pathlib import Path
from typing import Protocol


class RegistryValidatorService:
    """Application service orchestrating registry validation."""

    def __init__(self, sot_path: str) -> None:
        self.sot_path = sot_path

    def validate_repo(self, full_name: str, local_path: str, layer: str) -> dict:
        return {
            "full_name": full_name,
            "local_path": local_path,
            "layer": layer,
            "valid": True,
        }


class CLIRegistryAdapter:
    """CLI adapter for sot-registry-guardian."""

    def execute(self, command: str, payload: dict) -> dict:
        if command == "validate":
            return RegistryValidatorService(payload["sot_path"]).validate_repo(
                payload["full_name"], payload["local_path"], payload["layer"]
            )
        raise ValueError(f"Unknown command: {command}")
