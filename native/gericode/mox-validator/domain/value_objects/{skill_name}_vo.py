"""Value objects for mox-validator."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MoxValidatorId:
    """Value object for mox-validator identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
