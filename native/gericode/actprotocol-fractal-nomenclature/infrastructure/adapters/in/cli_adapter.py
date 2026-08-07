"""CLI adapter for actprotocol-fractal-nomenclature."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.actprotocol-fractal-nomenclature_ports import ActprotocolFractalNomenclaturePort

logger = logging.getLogger(__name__)


class ActprotocolFractalNomenclatureCLIAdapter:
    """CLI adapter for actprotocol-fractal-nomenclature."""

    def __init__(self, port: ActprotocolFractalNomenclaturePort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
