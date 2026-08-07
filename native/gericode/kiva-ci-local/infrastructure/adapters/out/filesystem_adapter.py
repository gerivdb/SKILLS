"""Filesystem adapter for kiva-ci-local."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from domain.repository_contracts.kiva-ci-local_repo import KivaCiLocalRepositoryContract

logger = logging.getLogger(__name__)


class KivaCiLocalFilesystemAdapter(KivaCiLocalRepositoryContract):
    """Filesystem adapter for kiva-ci-local."""

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path

    def get(self, id: str) -> dict | None:
        """Get entity by ID from filesystem."""
        path = self.base_path / f"{id}.json"
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def save(self, entity: dict) -> None:
        """Save entity to filesystem."""
        entity_id = entity.get("id", "unknown")
        path = self.base_path / f"{entity_id}.json"
        path.write_text(json.dumps(entity, indent=2), encoding="utf-8")

    def delete(self, id: str) -> bool:
        """Delete entity by ID."""
        path = self.base_path / f"{id}.json"
        if path.exists():
            path.unlink()
            return True
        return False
