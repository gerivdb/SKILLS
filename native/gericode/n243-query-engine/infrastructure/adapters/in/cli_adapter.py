"""CLI adapter for n243-query-engine."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.n243-query-engine_ports import N243QueryEnginePort

logger = logging.getLogger(__name__)


class N243QueryEngineCLIAdapter:
    """CLI adapter for n243-query-engine."""

    def __init__(self, port: N243QueryEnginePort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
