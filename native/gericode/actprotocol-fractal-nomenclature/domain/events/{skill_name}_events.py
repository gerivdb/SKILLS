"""Domain events for actprotocol-fractal-nomenclature."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ActprotocolFractalNomenclatureEvent:
    """Base domain event for actprotocol-fractal-nomenclature."""

    occurred_at: datetime

    @classmethod
    def now(cls, **kwargs) -> ActprotocolFractalNomenclatureEvent:
        """Create event with current timestamp."""
        return cls(occurred_at=datetime.now(), **kwargs)
