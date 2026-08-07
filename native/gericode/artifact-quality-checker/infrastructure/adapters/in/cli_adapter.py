"""CLI adapter for artifact-quality-checker."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.artifact-quality-checker_ports import ArtifactQualityCheckerPort

logger = logging.getLogger(__name__)


class ArtifactQualityCheckerCLIAdapter:
    """CLI adapter for artifact-quality-checker."""

    def __init__(self, port: ArtifactQualityCheckerPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
