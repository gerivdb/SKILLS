"""Outbound ports for artifact-quality-checker."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class ArtifactQualityCheckerRepositoryPort(ABC):
    """Outbound repository port for artifact-quality-checker."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
