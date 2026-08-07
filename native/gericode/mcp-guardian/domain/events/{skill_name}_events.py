"""Domain events for mcp-guardian."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class McpGuardianEvent:
    """Base domain event for mcp-guardian."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> McpGuardianEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
