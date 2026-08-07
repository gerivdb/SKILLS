"""Outbound ports for ci-nomenclature-guard."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class CiNomenclatureGuardRepositoryPort(ABC):
    """Outbound repository port for ci-nomenclature-guard."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
