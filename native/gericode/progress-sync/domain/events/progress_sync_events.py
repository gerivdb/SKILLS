"""Domain events for progress-sync."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProgressSyncEvent:
    """Base domain event for progress-sync."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> ProgressSyncEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
