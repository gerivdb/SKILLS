"""Domain entity for ontology-guardian."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class OntologyGuardianEntity:
    """Domain entity for ontology-guardian."""

    id: str
    data: dict

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {"id": self.id, "data": self.data}

    @classmethod
    def from_dict(cls, data: dict) -> OntologyGuardianEntity:
        """Create entity from dictionary."""
        return cls(id=data["id"], data=data["data"])
