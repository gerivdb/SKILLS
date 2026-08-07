"""CLI adapter for m5-production-monitor."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.m5_production_monitor_ports import M5MonitorPort

logger = logging.getLogger(__name__)


class M5MonitorCLIAdapter:
    """CLI adapter for m5-production-monitor."""

    def __init__(self, port: M5MonitorPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
