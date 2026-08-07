"""Inbound ports for ci-nomenclature-guard."""

from __future__ import annotations

from abc import ABC, abstractmethod


class CiNomenclatureGuardPort(ABC):
    """Inbound port for ci-nomenclature-guard."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
