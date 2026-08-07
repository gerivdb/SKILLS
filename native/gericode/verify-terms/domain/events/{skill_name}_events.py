"""Domain events for verify-terms."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class VerifyTermsEvent:
    """Base domain event for verify-terms."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> VerifyTermsEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
