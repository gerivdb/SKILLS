"""Outbound ports for progress-sync."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class ProgressSyncRepositoryPort(ABC):
    """Outbound repository port for progress-sync."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
