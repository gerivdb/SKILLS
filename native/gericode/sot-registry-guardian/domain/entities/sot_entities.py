"""
DDD Entities — sot-registry-guardian
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RepositoryEntry:
    full_name: str
    local_path: str
    layer: str
    status: str = "active"

    def validate_layer(self) -> bool:
        return self.layer.startswith("L") and self.layer[1:].split("-")[0].isdigit()


@dataclass
class DriftReport:
    repo_name: str
    mismatches: list[str]
    valid: bool

    def add_mismatch(self, message: str) -> None:
        self.mismatches.append(message)
        self.valid = False
