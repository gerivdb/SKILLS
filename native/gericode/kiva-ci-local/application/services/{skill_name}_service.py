"""Application service for kiva-ci-local."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.kiva-ci-local_ports import KivaCiLocalPort
from application.ports.out.kiva-ci-local_ports import KivaCiLocalRepositoryPort

logger = logging.getLogger(__name__)


class KivaCiLocalService:
    """Application service for kiva-ci-local."""

    def __init__(
        self,
        in_port: KivaCiLocalPort,
        repo_port: KivaCiLocalRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
