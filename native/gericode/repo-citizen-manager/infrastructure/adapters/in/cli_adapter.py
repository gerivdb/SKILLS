"""CLI adapter for repo-citizen-manager."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.repo-citizen-manager_ports import RepoCitizenManagerPort

logger = logging.getLogger(__name__)


class RepoCitizenManagerCLIAdapter:
    """CLI adapter for repo-citizen-manager."""

    def __init__(self, port: RepoCitizenManagerPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
