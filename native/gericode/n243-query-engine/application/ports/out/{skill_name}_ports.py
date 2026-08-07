"""Outbound ports for n243-query-engine."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class N243QueryEngineRepositoryPort(ABC):
    """Outbound repository port for n243-query-engine."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
