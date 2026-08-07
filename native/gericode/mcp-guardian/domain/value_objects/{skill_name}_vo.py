"""Value objects for mcp-guardian."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class McpGuardianId:
    """Value object for mcp-guardian identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
