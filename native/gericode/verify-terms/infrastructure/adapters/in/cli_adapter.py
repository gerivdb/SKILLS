"""CLI adapter for verify-terms."""

from __future__ import annotations

import logging
from pathlib import Path

from application.ports.in.verify-terms_ports import VerifyTermsPort

logger = logging.getLogger(__name__)


class VerifyTermsCLIAdapter:
    """CLI adapter for verify-terms."""

    def __init__(self, port: VerifyTermsPort) -> None:
        self.port = port

    def run(self, input_path: Path) -> dict:
        """Run skill from CLI input."""
        data = {"path": str(input_path)}
        return self.port.execute(data)
