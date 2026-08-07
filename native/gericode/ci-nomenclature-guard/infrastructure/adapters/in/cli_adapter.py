"""CLI adapter for ci-nomenclature-guard."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.ci-nomenclature-guard_ports import CiNomenclatureGuardPort

logger = logging.getLogger(__name__)


class CiNomenclatureGuardCLIAdapter:
    """CLI adapter for ci-nomenclature-guard."""

    def __init__(self, port: CiNomenclatureGuardPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
