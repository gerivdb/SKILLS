"""Domain events for mox-validator."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class MoxValidatorEvent:
    """Base domain event for mox-validator."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> MoxValidatorEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
