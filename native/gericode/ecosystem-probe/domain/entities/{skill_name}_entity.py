"""Domain entity for ecosystem-probe."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EcosystemProbeEntity:
    """Domain entity for ecosystem-probe."""

    id: str
    data: dict

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {"id": self.id, "data": self.data}

    @classmethod
    def from_dict(cls, data: dict) -> EcosystemProbeEntity:
        """Create entity from dictionary."""
        return cls(id=data["id"], data=data["data"])
