"""Inbound ports for repo-citizen-manager."""

from __future__ import annotations

from abc import ABC, abstractmethod


class RepoCitizenManagerPort(ABC):
    """Inbound port for repo-citizen-manager."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
