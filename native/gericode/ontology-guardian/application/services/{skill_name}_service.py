"""Application service for ontology-guardian."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.ontology-guardian_ports import OntologyGuardianPort
from application.ports.out.ontology-guardian_ports import OntologyGuardianRepositoryPort

logger = logging.getLogger(__name__)


class OntologyGuardianService:
    """Application service for ontology-guardian."""

    def __init__(
        self,
        in_port: OntologyGuardianPort,
        repo_port: OntologyGuardianRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
