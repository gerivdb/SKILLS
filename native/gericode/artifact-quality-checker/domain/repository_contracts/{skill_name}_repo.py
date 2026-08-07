"""Repository contract for artifact-quality-checker."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class ArtifactQualityCheckerRepositoryContract(ABC):
    """Repository contract for artifact-quality-checker."""

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
