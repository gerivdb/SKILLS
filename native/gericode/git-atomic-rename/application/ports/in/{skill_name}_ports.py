"""Inbound ports for git-atomic-rename."""

from __future__ import annotations

from abc import ABC, abstractmethod


class GitAtomicRenamePort(ABC):
    """Inbound port for git-atomic-rename."""

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute the skill with given input."""
        pass
