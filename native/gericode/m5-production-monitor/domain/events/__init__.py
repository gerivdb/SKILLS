"""Domain events for m5-production-monitor."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class M5ConceptEvent:
    """Base domain event for m5-production-monitor."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> M5ConceptEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
