"""Domain entity for git-atomic-rename."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GitAtomicRenameEntity:
    """Domain entity for git-atomic-rename."""

    id: str
    data: dict

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {"id": self.id, "data": self.data}

    @classmethod
    def from_dict(cls, data: dict) -> GitAtomicRenameEntity:
        """Create entity from dictionary."""
        return cls(id=data["id"], data=data["data"])
