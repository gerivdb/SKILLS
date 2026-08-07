"""Application service for progress-sync."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.progress_sync_ports import ProgressSyncPort
from application.ports.out.progress_sync_ports import ProgressSyncRepositoryPort

logger = logging.getLogger(__name__)


class ProgressSyncService:
    """Application service for progress-sync."""

    def __init__(
        self,
        in_port: ProgressSyncPort,
        repo_port: ProgressSyncRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
