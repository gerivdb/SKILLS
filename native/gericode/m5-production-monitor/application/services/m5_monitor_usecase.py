"""M5 monitor use case / interactor."""

from __future__ import annotations

import importlib
import json
import logging
from pathlib import Path
from typing import Any

m5_in_module = importlib.import_module("application.ports.in.m5_production_monitor_ports")
M5MonitorPort = m5_in_module.M5MonitorPort

m5_out_module = importlib.import_module("application.ports.out.m5_production_monitor_ports")
M5MonitorRepositoryPort = m5_out_module.M5MonitorRepositoryPort

logger = logging.getLogger(__name__)

from domain.entities.m5_concept import M5ConceptEntity  # noqa: E402


class M5MonitorUseCase(M5MonitorPort):
    """Use case for m5-production-monitor."""

    def __init__(
        self,
        repo_port: M5MonitorRepositoryPort,
        service: Any | None = None,
    ) -> None:
        self.repo_port = repo_port
        self.service = service

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        if self.service is None:
            service_module = importlib.import_module("application.services.m5_monitor_service")
            M5MonitorService = service_module.M5MonitorService
            self.service = M5MonitorService(self, self.repo_port)

        concept_registry_path = input_data.get("concept_registry_path")
        m5_threshold = float(input_data.get("m5_threshold", 0.7))

        if not concept_registry_path:
            return {"error": "concept_registry_path is required"}

        path = Path(concept_registry_path)
        if not path.exists():
            return {"error": f"Registry path not found: {concept_registry_path}"}

        concepts = self._load_concepts(path)
        report = self.service.generate_report(concepts)

        ready_for_integration = [c for c in concepts if c.maturity_score >= m5_threshold]

        return {
            "report": report,
            "ready_for_integration_count": len(ready_for_integration),
            "ready_for_integration": [c.to_dict() for c in ready_for_integration],
            "threshold": m5_threshold,
        }

    def _load_concepts(self, path: Path) -> list[Any]:
        """Load concepts from registry path."""
        concepts: list[Any] = []

        if path.is_file():
            concepts.extend(self._parse_concept_file(path))
        elif path.is_dir():
            for file_path in path.glob("*.json"):
                concepts.extend(self._parse_concept_file(file_path))

        return concepts

    def _parse_concept_file(self, path: Path) -> list[Any]:
        """Parse a concept file into entities."""
        concepts: list[Any] = []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for item in data:
                    concepts.append(M5ConceptEntity.from_dict(item))
            elif isinstance(data, dict):
                concepts.append(M5ConceptEntity.from_dict(data))
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to parse concept file %s: %s", path, exc)

        return concepts
