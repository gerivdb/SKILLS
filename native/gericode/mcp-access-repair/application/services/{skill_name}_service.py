"""Application service for mcp-access-repair."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.mcp-access-repair_ports import McpAccessRepairPort
from application.ports.out.mcp-access-repair_ports import McpAccessRepairRepositoryPort

logger = logging.getLogger(__name__)


class McpAccessRepairService:
    """Application service for mcp-access-repair."""

    def __init__(
        self,
        in_port: McpAccessRepairPort,
        repo_port: McpAccessRepairRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
