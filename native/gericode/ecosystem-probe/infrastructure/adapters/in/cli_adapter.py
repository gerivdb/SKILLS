"""CLI adapter for ecosystem-probe."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.ecosystem-probe_ports import EcosystemProbePort

logger = logging.getLogger(__name__)


class EcosystemProbeCLIAdapter:
    """CLI adapter for ecosystem-probe."""

    def __init__(self, port: EcosystemProbePort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
