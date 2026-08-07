"""Application service for repo-citizen-manager."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.repo-citizen-manager_ports import RepoCitizenManagerPort
from application.ports.out.repo-citizen-manager_ports import RepoCitizenManagerRepositoryPort

logger = logging.getLogger(__name__)


class RepoCitizenManagerService:
    """Application service for repo-citizen-manager."""

    def __init__(
        self,
        in_port: RepoCitizenManagerPort,
        repo_port: RepoCitizenManagerRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
