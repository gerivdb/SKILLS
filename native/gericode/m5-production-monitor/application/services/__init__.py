"""Application service for m5-production-monitor."""

from __future__ import annotations

import logging

from application.ports.in.m5_production_monitor_ports import M5MonitorPort
from application.ports.out.m5_production_monitor_ports import M5MonitorRepositoryPort

logger = logging.getLogger(__name__)


class M5MonitorService:
    """Application service for m5-production-monitor."""

    def __init__(
        self,
        in_port: M5MonitorPort,
        repo_port: M5MonitorRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
