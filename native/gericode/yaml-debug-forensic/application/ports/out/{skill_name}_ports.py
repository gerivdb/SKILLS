"""Outbound ports for yaml-debug-forensic."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class YamlDebugForensicRepositoryPort(ABC):
    """Outbound repository port for yaml-debug-forensic."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
