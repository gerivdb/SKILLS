"""CLI adapter for git-atomic-rename."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.git-atomic-rename_ports import GitAtomicRenamePort

logger = logging.getLogger(__name__)


class GitAtomicRenameCLIAdapter:
    """CLI adapter for git-atomic-rename."""

    def __init__(self, port: GitAtomicRenamePort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
