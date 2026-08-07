"""CLI adapter for yaml-debug-forensic."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.yaml-debug-forensic_ports import YamlDebugForensicPort

logger = logging.getLogger(__name__)


class YamlDebugForensicCLIAdapter:
    """CLI adapter for yaml-debug-forensic."""

    def __init__(self, port: YamlDebugForensicPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
