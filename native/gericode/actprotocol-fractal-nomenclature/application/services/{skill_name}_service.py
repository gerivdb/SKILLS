"""Application service for actprotocol-fractal-nomenclature."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.actprotocol-fractal-nomenclature_ports import ActprotocolFractalNomenclaturePort
from application.ports.out.actprotocol-fractal-nomenclature_ports import ActprotocolFractalNomenclatureRepositoryPort

logger = logging.getLogger(__name__)


class ActprotocolFractalNomenclatureService:
    """Application service for actprotocol-fractal-nomenclature."""

    def __init__(
        self,
        in_port: ActprotocolFractalNomenclaturePort,
        repo_port: ActprotocolFractalNomenclatureRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
