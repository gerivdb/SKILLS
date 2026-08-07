"""Value objects for verify-terms."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VerifyTermsId:
    """Value object for verify-terms identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
