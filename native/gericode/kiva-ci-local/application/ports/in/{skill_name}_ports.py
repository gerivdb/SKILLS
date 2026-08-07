"""Inbound ports for kiva-ci-local."""

from __future__ import annotations

from abc import ABC, abstractmethod


class KivaCiLocalPort(ABC):
    """Inbound port for kiva-ci-local."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
