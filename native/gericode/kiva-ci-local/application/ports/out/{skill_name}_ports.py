"""Outbound ports for kiva-ci-local."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class KivaCiLocalRepositoryPort(ABC):
    """Outbound repository port for kiva-ci-local."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
