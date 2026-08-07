"""Value objects for n243-query-engine."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class N243QueryEngineId:
    """Value object for n243-query-engine identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
