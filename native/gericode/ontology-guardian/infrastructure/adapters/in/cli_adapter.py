"""CLI adapter for ontology-guardian."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.ontology-guardian_ports import OntologyGuardianPort

logger = logging.getLogger(__name__)


class OntologyGuardianCLIAdapter:
    """CLI adapter for ontology-guardian."""

    def __init__(self, port: OntologyGuardianPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
