"""CLI adapter for progress-sync."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.progress_sync_ports import ProgressSyncPort

logger = logging.getLogger(__name__)


class ProgressSyncCLIAdapter:
    """CLI adapter for progress-sync."""

    def __init__(self, port: ProgressSyncPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
