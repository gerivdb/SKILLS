"""Outbound ports for m5-production-monitor."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class M5MonitorRepositoryPort(ABC):
    """Outbound repository port for m5-production-monitor."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
