"""Inbound ports for yaml-debug-forensic."""

from __future__ import annotations

from abc import ABC, abstractmethod


class YamlDebugForensicPort(ABC):
    """Inbound port for yaml-debug-forensic."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
