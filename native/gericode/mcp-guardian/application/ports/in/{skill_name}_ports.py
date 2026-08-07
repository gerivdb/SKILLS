"""Inbound ports for mcp-guardian."""

from __future__ import annotations

from abc import ABC, abstractmethod


class McpGuardianPort(ABC):
    """Inbound port for mcp-guardian."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
