"""Application service for mox-validator."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.mox-validator_ports import MoxValidatorPort
from application.ports.out.mox-validator_ports import MoxValidatorRepositoryPort

logger = logging.getLogger(__name__)


class MoxValidatorService:
    """Application service for mox-validator."""

    def __init__(
        self,
        in_port: MoxValidatorPort,
        repo_port: MoxValidatorRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
