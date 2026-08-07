"""
DDD Value Objects — yaml-safe-injector
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Layer:
    value: str

    def __post_init__(self):
        valid = {
            "L0-CANON",
            "L1-INFRA",
            "L2-PLATFORM",
            "L3-CITIZENS",
            "L4-TOOLS",
            "L5-ARCHIVE",
        }
        if self.value not in valid:
            raise ValueError(f"Invalid layer: {self.value}")


@dataclass(frozen=True)
class VerseMapping:
    value: str

    def __post_init__(self):
        if self.value not in {"verse", "none"}:
            raise ValueError("VerseMapping must be 'verse' or 'none'")
