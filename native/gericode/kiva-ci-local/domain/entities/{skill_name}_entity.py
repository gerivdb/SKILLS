"""Domain entity for kiva-ci-local."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class KivaCiLocalEntity:
    """Domain entity for kiva-ci-local."""

    id: str
    data: dict

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {"id": self.id, "data": self.data}

    @classmethod
    def from_dict(cls, data: dict) -> KivaCiLocalEntity:
        """Create entity from dictionary."""
        return cls(id=data["id"], data=data["data"])
