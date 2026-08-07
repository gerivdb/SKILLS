"""Value objects for mcp-access-repair."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class McpAccessRepairId:
    """Value object for mcp-access-repair identifier."""

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("ID cannot be empty")
