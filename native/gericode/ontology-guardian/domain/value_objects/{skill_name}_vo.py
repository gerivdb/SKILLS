"""Value objects for ontology-guardian."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OntologyGuardianId:
    """Value object for ontology-guardian identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
