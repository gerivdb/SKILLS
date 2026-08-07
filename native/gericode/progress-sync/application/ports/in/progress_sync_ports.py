"""Inbound ports for progress-sync."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ProgressSyncPort(ABC):
    """Inbound port for progress-sync."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
