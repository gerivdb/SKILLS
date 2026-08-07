"""Outbound ports for git-atomic-rename."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class GitAtomicRenameRepositoryPort(ABC):
    """Outbound repository port for git-atomic-rename."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
