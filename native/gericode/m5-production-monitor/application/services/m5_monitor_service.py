"""Application service for m5-production-monitor."""

from __future__ import annotations

import importlib
import logging
from typing import Any

m5_in_module = importlib.import_module("application.ports.in.m5_production_monitor_ports")
M5MonitorPort = m5_in_module.M5MonitorPort

m5_out_module = importlib.import_module("application.ports.out.m5_production_monitor_ports")
M5MonitorRepositoryPort = m5_out_module.M5MonitorRepositoryPort

logger = logging.getLogger(__name__)


class M5MonitorService:
    """Application service for m5-production-monitor."""

    def __init__(
        self,
        in_port: M5MonitorPort,
        repo_port: M5MonitorRepositoryPort,
    ) -> None:
        self.in_port = in_port
        self.repo_port = repo_port

    def execute(self, input_data: dict) -> dict:
        """Execute the skill use case."""
        return self.in_port.execute(input_data)

    def classify_concept(self, concept: Any) -> dict:
        """Classify concept based on maturity score."""
        target_phase = concept.get_target_phase()
        transition_allowed = self._is_transition_allowed(concept.phase, target_phase)

        return {
            "concept_id": concept.concept_id,
            "current_phase": concept.phase,
            "target_phase": target_phase,
            "maturity_score": concept.maturity_score,
            "transition_allowed": transition_allowed,
            "classification": self._get_classification(concept),
        }

    def _is_transition_allowed(self, current: str, target: str) -> bool:
        """Check if phase transition is allowed."""
        allowed_transitions = {
            "detectBirth": ["develop"],
            "develop": ["stabilize"],
            "stabilize": ["integrate"],
            "integrate": ["lifecycle"],
            "lifecycle": [],
        }
        return target in allowed_transitions.get(current, [])

    def _get_classification(self, concept: Any) -> str:
        """Get classification label for concept."""
        if concept.is_embryo():
            return "embryo"
        if concept.is_developing():
            return "developing"
        if concept.is_stable():
            return "stable"
        if concept.is_mature():
            return "mature"
        return "unknown"

    def generate_report(self, concepts: list[Any]) -> dict:
        """Generate maturity report for a list of concepts."""
        report = {
            "total": len(concepts),
            "embryos": [],
            "developing": [],
            "stable": [],
            "integrated": [],
            "lifecycle": [],
        }

        for concept in concepts:
            if concept.is_embryo():
                report["embryos"].append(concept.to_dict())
            elif concept.is_developing():
                report["developing"].append(concept.to_dict())
            elif concept.is_stable():
                report["stable"].append(concept.to_dict())
            elif concept.is_mature():
                report["integrated"].append(concept.to_dict())
            else:
                report["lifecycle"].append(concept.to_dict())

        return report
