"""Inbound ports for ecosystem-probe."""

from __future__ import annotations

from abc import ABC, abstractmethod


class EcosystemProbePort(ABC):
    """Inbound port for ecosystem-probe."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
