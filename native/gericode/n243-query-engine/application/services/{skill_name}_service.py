"""Application service for n243-query-engine."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.n243-query-engine_ports import N243QueryEnginePort
from application.ports.out.n243-query-engine_ports import N243QueryEngineRepositoryPort

logger = logging.getLogger(__name__)


class N243QueryEngineService:
    """Application service for n243-query-engine."""

    def __init__(
        self,
        in_port: N243QueryEnginePort,
        repo_port: N243QueryEngineRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
