"""Domain entity for mcp-guardian."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class McpGuardianEntity:
    """Domain entity for mcp-guardian."""

    id: str
    data: dict

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {"id": self.id, "data": self.data}

    @classmethod
    def from_dict(cls, data: dict) -> McpGuardianEntity:
        """Create entity from dictionary."""
        return cls(id=data["id"], data=data["data"])
