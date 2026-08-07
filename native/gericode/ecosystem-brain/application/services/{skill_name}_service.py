"""Application service for ecosystem-brain."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.ecosystem-brain_ports import EcosystemBrainPort
from application.ports.out.ecosystem-brain_ports import EcosystemBrainRepositoryPort

logger = logging.getLogger(__name__)


class EcosystemBrainService:
    """Application service for ecosystem-brain."""

    def __init__(
        self,
        in_port: EcosystemBrainPort,
        repo_port: EcosystemBrainRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
