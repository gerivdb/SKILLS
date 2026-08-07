"""Skill — sot-registry-guardian

Protège known_repositories.yaml contre les modifications non validées.
Bloque les writes directs, force l'usage du mapping local ou du skill d'injection.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)

APPROVED_CHANNELS = {
    "yaml-safe-injector",
    "verse_mapping",
    "sot-registry-guardian",
}


class SOTGuardianError(Exception):
    """Erreur de protection SOT."""


class SOTGuardian:
    def __init__(self, known_repositories_path: Path) -> None:
        self.known_repositories_path = known_repositories_path
        self._log: list[dict] = []

    def check_write(
        self,
        caller: str,
        channel: Literal["yaml-safe-injector", "verse_mapping", "sot-registry-guardian", "unknown"] = "unknown",
    ) -> None:
        """Vérifie qu'un write est autorisé.

        Args:
            caller: Nom de l'appelant (skill/script).
            channel: Canal d'écriture utilisé.

        Raises:
            SOTGuardianError: Si le write n'est pas autorisé.
        """
        entry = {
            "caller": caller,
            "channel": channel,
            "path": str(self.known_repositories_path),
            "allowed": channel in APPROVED_CHANNELS,
        }
        self._log.append(entry)

        if channel not in APPROVED_CHANNELS:
            logger.error(
                "SOT write bloqué: caller=%s channel=%s path=%s",
                caller,
                channel,
                self.known_repositories_path,
            )
            raise SOTGuardianError(
                f"Write direct dans {self.known_repositories_path} interdit. "
                f"Utiliser 'yaml-safe-injector' ou 'verse_mapping'. "
                f"Caller: {caller}, channel: {channel}"
            )

        logger.info(
            "SOT write autorisé: caller=%s channel=%s path=%s",
            caller,
            channel,
            self.known_repositories_path,
        )

    def audit(self) -> list[dict]:
        """Retourne le journal des accès."""
        return list(self._log)
