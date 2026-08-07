"""Repository contract for yaml-debug-forensic."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class YamlDebugForensicRepositoryContract(ABC):
    """Repository contract for yaml-debug-forensic."""

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
