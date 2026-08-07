"""Inbound ports for actprotocol-fractal-nomenclature."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ActprotocolFractalNomenclaturePort(ABC):
    """Inbound port for actprotocol-fractal-nomenclature."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
