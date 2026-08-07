"""Domain events for ecosystem-brain."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class EcosystemBrainEvent:
    """Base domain event for ecosystem-brain."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> EcosystemBrainEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
