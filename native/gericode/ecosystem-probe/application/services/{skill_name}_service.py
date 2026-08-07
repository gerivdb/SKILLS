"""Application service for ecosystem-probe."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.ecosystem-probe_ports import EcosystemProbePort
from application.ports.out.ecosystem-probe_ports import EcosystemProbeRepositoryPort

logger = logging.getLogger(__name__)


class EcosystemProbeService:
    """Application service for ecosystem-probe."""

    def __init__(
        self,
        in_port: EcosystemProbePort,
        repo_port: EcosystemProbeRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
