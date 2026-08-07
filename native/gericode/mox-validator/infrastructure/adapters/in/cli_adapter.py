"""CLI adapter for mox-validator."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.mox-validator_ports import MoxValidatorPort

logger = logging.getLogger(__name__)


class MoxValidatorCLIAdapter:
    """CLI adapter for mox-validator."""

    def __init__(self, port: MoxValidatorPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
