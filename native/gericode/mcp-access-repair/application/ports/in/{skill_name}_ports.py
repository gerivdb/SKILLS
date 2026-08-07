"""Inbound ports for mcp-access-repair."""

from __future__ import annotations

from abc import ABC, abstractmethod


class McpAccessRepairPort(ABC):
    """Inbound port for mcp-access-repair."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
