"""Inbound ports for verify-terms."""

from __future__ import annotations

from abc import ABC, abstractmethod


class VerifyTermsPort(ABC):
    """Inbound port for verify-terms."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
