"""Inbound ports for n243-query-engine."""

from __future__ import annotations

from abc import ABC, abstractmethod


class N243QueryEnginePort(ABC):
    """Inbound port for n243-query-engine."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
