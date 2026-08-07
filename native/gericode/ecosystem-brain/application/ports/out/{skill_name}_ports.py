"""Outbound ports for ecosystem-brain."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class EcosystemBrainRepositoryPort(ABC):
    """Outbound repository port for ecosystem-brain."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
