"""Domain events for git-atomic-rename."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class GitAtomicRenameEvent:
    """Base domain event for git-atomic-rename."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> GitAtomicRenameEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
