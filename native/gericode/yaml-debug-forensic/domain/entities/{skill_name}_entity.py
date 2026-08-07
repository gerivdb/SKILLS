"""Domain entity for yaml-debug-forensic."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class YamlDebugForensicEntity:
    """Domain entity for yaml-debug-forensic."""

    id: str
    data: dict

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {"id": self.id, "data": self.data}

    @classmethod
    def from_dict(cls, data: dict) -> YamlDebugForensicEntity:
        """Create entity from dictionary."""
        return cls(id=data["id"], data=data["data"])
