"""Outbound ports for ecosystem-probe."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class EcosystemProbeRepositoryPort(ABC):
    """Outbound repository port for ecosystem-probe."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
