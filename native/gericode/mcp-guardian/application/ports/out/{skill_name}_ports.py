"""Outbound ports for mcp-guardian."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class McpGuardianRepositoryPort(ABC):
    """Outbound repository port for mcp-guardian."""

    @abstractmethod
    def save(self, data: dict) -> None:
        """Save data."""
        pass

    @abstractmethod
    def load(self, key: str) -> dict | None:
        """Load data by key."""
        pass
