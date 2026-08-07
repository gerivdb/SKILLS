"""Application service for verify-terms."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.verify-terms_ports import VerifyTermsPort
from application.ports.out.verify-terms_ports import VerifyTermsRepositoryPort

logger = logging.getLogger(__name__)


class VerifyTermsService:
    """Application service for verify-terms."""

    def __init__(
        self,
        in_port: VerifyTermsPort,
        repo_port: VerifyTermsRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)
