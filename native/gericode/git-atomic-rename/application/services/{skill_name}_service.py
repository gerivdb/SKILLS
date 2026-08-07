"""Application service for git-atomic-rename."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.git-atomic-rename_ports import GitAtomicRenamePort
from application.ports.out.git-atomic-rename_ports import GitAtomicRenameRepositoryPort

logger = logging.getLogger(__name__)


class GitAtomicRenameService:
    """Application service for git-atomic-rename."""

    def __init__(
        self,
        in_port: GitAtomicRenamePort,
        repo_port: GitAtomicRenameRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
