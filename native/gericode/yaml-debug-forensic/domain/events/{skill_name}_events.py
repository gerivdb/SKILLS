"""Domain events for yaml-debug-forensic."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class YamlDebugForensicEvent:
    """Base domain event for yaml-debug-forensic."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> YamlDebugForensicEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
