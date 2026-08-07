"""Outbound ports for ontology-guardian."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class OntologyGuardianRepositoryPort(ABC):
    """Outbound repository port for ontology-guardian."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
