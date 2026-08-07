"""Domain events for artifact-quality-checker."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ArtifactQualityCheckerEvent:
    """Base domain event for artifact-quality-checker."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> ArtifactQualityCheckerEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
