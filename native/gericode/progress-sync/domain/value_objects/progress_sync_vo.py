"""Value objects for progress-sync."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProgressSyncId:
    """Value object for progress-sync identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
