"""Application service for artifact-quality-checker."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.artifact-quality-checker_ports import ArtifactQualityCheckerPort
from application.ports.out.artifact-quality-checker_ports import ArtifactQualityCheckerRepositoryPort

logger = logging.getLogger(__name__)


class ArtifactQualityCheckerService:
    """Application service for artifact-quality-checker."""

    def __init__(
        self,
        in_port: ArtifactQualityCheckerPort,
        repo_port: ArtifactQualityCheckerRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
