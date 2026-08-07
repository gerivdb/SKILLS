"""Value objects for repo-citizen-manager."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RepoCitizenManagerId:
    """Value object for repo-citizen-manager identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
