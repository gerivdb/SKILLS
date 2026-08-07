"""Domain events for n243-query-engine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class N243QueryEngineEvent:
    """Base domain event for n243-query-engine."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> N243QueryEngineEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
