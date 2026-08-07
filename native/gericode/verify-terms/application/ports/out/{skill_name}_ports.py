"""Outbound ports for verify-terms."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class VerifyTermsRepositoryPort(ABC):
    """Outbound repository port for verify-terms."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
