"""Outbound ports for actprotocol-fractal-nomenclature."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class ActprotocolFractalNomenclatureRepositoryPort(ABC):
    """Outbound repository port for actprotocol-fractal-nomenclature."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
