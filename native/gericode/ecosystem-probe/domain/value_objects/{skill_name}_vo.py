"""Value objects for ecosystem-probe."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EcosystemProbeId:
    """Value object for ecosystem-probe identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
