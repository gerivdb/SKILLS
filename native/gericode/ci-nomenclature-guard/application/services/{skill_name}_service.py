"""Application service for ci-nomenclature-guard."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.ci-nomenclature-guard_ports import CiNomenclatureGuardPort
from application.ports.out.ci-nomenclature-guard_ports import CiNomenclatureGuardRepositoryPort

logger = logging.getLogger(__name__)


class CiNomenclatureGuardService:
    """Application service for ci-nomenclature-guard."""

    def __init__(
        self,
        in_port: CiNomenclatureGuardPort,
        repo_port: CiNomenclatureGuardRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
