"""Value objects for actprotocol-fractal-nomenclature."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ActprotocolFractalNomenclatureId:
    """Value object for actprotocol-fractal-nomenclature identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
