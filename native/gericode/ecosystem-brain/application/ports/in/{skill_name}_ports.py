"""Inbound ports for ecosystem-brain."""

from __future__ import annotations

from abc import ABC, abstractmethod


class EcosystemBrainPort(ABC):
    """Inbound port for ecosystem-brain."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
