"""Domain events for ontology-guardian."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OntologyGuardianEvent:
    """Base domain event for ontology-guardian."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> OntologyGuardianEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
