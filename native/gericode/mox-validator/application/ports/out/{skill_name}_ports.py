"""Outbound ports for mox-validator."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class MoxValidatorRepositoryPort(ABC):
    """Outbound repository port for mox-validator."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
