"""Application service for mcp-guardian."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.mcp-guardian_ports import McpGuardianPort
from application.ports.out.mcp-guardian_ports import McpGuardianRepositoryPort

logger = logging.getLogger(__name__)


class McpGuardianService:
    """Application service for mcp-guardian."""

    def __init__(
        self,
        in_port: McpGuardianPort,
        repo_port: McpGuardianRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
