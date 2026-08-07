"""CLI adapter for mcp-access-repair."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.mcp-access-repair_ports import McpAccessRepairPort

logger = logging.getLogger(__name__)


class McpAccessRepairCLIAdapter:
    """CLI adapter for mcp-access-repair."""

    def __init__(self, port: McpAccessRepairPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
