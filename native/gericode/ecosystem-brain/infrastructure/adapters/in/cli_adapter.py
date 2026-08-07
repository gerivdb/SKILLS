"""CLI adapter for ecosystem-brain."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.ecosystem-brain_ports import EcosystemBrainPort

logger = logging.getLogger(__name__)


class EcosystemBrainCLIAdapter:
    """CLI adapter for ecosystem-brain."""

    def __init__(self, port: EcosystemBrainPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
