"""Repository contract for actprotocol-fractal-nomenclature."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class ActprotocolFractalNomenclatureRepositoryContract(ABC):
    """Repository contract for actprotocol-fractal-nomenclature."""

    @abstractmethod
    def get(self, id: str) -> Optional[dict]:
        """Get entity by ID."""
        pass

    @abstractmethod
    def save(self, entity: dict) -> None:
        """Save entity."""
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete entity by ID."""
        pass
