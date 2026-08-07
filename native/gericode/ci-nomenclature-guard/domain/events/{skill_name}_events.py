"""Domain events for ci-nomenclature-guard."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CiNomenclatureGuardEvent:
    """Base domain event for ci-nomenclature-guard."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> CiNomenclatureGuardEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
