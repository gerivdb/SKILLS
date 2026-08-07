"""Value objects for ecosystem-brain."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EcosystemBrainId:
    """Value object for ecosystem-brain identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
