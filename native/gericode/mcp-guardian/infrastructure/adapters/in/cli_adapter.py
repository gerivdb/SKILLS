"""CLI adapter for mcp-guardian."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.mcp-guardian_ports import McpGuardianPort

logger = logging.getLogger(__name__)


class McpGuardianCLIAdapter:
    """CLI adapter for mcp-guardian."""

    def __init__(self, port: McpGuardianPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
