"""Domain events for kiva-ci-local."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class KivaCiLocalEvent:
    """Base domain event for kiva-ci-local."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> KivaCiLocalEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
