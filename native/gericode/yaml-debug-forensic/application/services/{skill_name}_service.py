"""Application service for yaml-debug-forensic."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.yaml-debug-forensic_ports import YamlDebugForensicPort
from application.ports.out.yaml-debug-forensic_ports import YamlDebugForensicRepositoryPort

logger = logging.getLogger(__name__)


class YamlDebugForensicService:
    """Application service for yaml-debug-forensic."""

    def __init__(
        self,
        in_port: YamlDebugForensicPort,
        repo_port: YamlDebugForensicRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
