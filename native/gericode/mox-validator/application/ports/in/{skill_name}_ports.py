"""Inbound ports for mox-validator."""

from __future__ import annotations

from abc import ABC, abstractmethod


class MoxValidatorPort(ABC):
    """Inbound port for mox-validator."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
