"""Domain events for ecosystem-probe."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class EcosystemProbeEvent:
    """Base domain event for ecosystem-probe."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> EcosystemProbeEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
