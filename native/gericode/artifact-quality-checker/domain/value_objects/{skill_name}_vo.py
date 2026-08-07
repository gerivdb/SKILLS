"""Value objects for artifact-quality-checker."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArtifactQualityCheckerId:
    """Value object for artifact-quality-checker identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
