"""Domain events for mcp-access-repair."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class McpAccessRepairEvent:
    """Base domain event for mcp-access-repair."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> McpAccessRepairEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
