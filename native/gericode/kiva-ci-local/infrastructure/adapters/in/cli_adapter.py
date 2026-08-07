"""CLI adapter for kiva-ci-local."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.kiva-ci-local_ports import KivaCiLocalPort

logger = logging.getLogger(__name__)


class KivaCiLocalCLIAdapter:
    """CLI adapter for kiva-ci-local."""

    def __init__(self, port: KivaCiLocalPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
