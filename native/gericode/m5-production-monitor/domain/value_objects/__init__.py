"""Value objects for m5-production-monitor."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class M5ConceptId:
    """Value object for m5-production-monitor identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
