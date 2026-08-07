"""Value objects for ci-nomenclature-guard."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CiNomenclatureGuardId:
    """Value object for ci-nomenclature-guard identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
