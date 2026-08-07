"""Domain entity for actprotocol-fractal-nomenclature."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ActprotocolFractalNomenclatureEntity:
    """Domain entity for actprotocol-fractal-nomenclature."""

    id: str
    data: dict

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {"id": self.id, "data": self.data}

    @classmethod
    def from_dict(cls, data: dict) -> ActprotocolFractalNomenclatureEntity:
        """Create entity from dictionary."""
        return cls(id=data["id"], data=data["data"])
