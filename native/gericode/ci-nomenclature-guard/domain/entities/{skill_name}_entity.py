"""Domain entity for ci-nomenclature-guard."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CiNomenclatureGuardEntity:
    """Domain entity for ci-nomenclature-guard."""

    id: str
    data: dict

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {"id": self.id, "data": self.data}

    @classmethod
    def from_dict(cls, data: dict) -> CiNomenclatureGuardEntity:
        """Create entity from dictionary."""
        return cls(id=data["id"], data=data["data"])
