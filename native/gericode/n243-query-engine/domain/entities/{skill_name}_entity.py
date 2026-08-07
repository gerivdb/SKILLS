"""Domain entity for n243-query-engine."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class N243QueryEngineEntity:
    """Domain entity for n243-query-engine."""

    id: str
    data: dict

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {"id": self.id, "data": self.data}

    @classmethod
    def from_dict(cls, data: dict) -> N243QueryEngineEntity:
        """Create entity from dictionary."""
        return cls(id=data["id"], data=data["data"])
