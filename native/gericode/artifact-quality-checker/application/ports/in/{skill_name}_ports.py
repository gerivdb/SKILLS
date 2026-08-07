"""Inbound ports for artifact-quality-checker."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ArtifactQualityCheckerPort(ABC):
    """Inbound port for artifact-quality-checker."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
