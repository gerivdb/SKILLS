"""Domain events for repo-citizen-manager."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class RepoCitizenManagerEvent:
    """Base domain event for repo-citizen-manager."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> RepoCitizenManagerEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
