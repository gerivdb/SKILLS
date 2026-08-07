"""Inbound ports for ontology-guardian."""

from __future__ import annotations

from abc import ABC, abstractmethod


class OntologyGuardianPort(ABC):
    """Inbound port for ontology-guardian."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
