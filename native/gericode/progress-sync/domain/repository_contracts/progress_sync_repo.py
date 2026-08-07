"""Repository contract for progress-sync."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class ProgressSyncRepositoryContract(ABC):
    """Repository contract for progress-sync."""

    @abstractmethod
    def get(self, id: str) -> Optional[dict]:
        """Get entity by ID."""
        pass

    @abstractmethod
    def save(self, entity: dict) -> None:
        """Save entity."""
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete entity by ID."""
        pass
