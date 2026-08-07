"""Inbound ports for m5-production-monitor."""

from __future__ import annotations

from abc import ABC, abstractmethod


class M5MonitorPort(ABC):
    """Inbound port for m5-production-monitor."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
