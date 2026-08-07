"""Domain entity for artifact-quality-checker."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ArtifactQualityCheckerEntity:
    """Domain entity for artifact-quality-checker."""

    id: str
    data: dict

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {"id": self.id, "data": self.data}

    @classmethod
    def from_dict(cls, data: dict) -> ArtifactQualityCheckerEntity:
        """Create entity from dictionary."""
        return cls(id=data["id"], data=data["data"])
