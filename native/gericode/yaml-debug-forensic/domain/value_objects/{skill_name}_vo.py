"""Value objects for yaml-debug-forensic."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class YamlDebugForensicId:
    """Value object for yaml-debug-forensic identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
