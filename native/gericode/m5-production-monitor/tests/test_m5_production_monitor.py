"""Tests for m5-production-monitor."""

from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

import pytest

m5_out_module = importlib.import_module("application.ports.out.m5_production_monitor_ports")
M5MonitorRepositoryPort = m5_out_module.M5MonitorRepositoryPort

from application.services.m5_monitor_service import M5MonitorService  # noqa: E402
from application.services.m5_monitor_usecase import M5MonitorUseCase  # noqa: E402
from domain.entities.m5_concept import M5ConceptEntity  # noqa: E402


class InMemoryRepository(M5MonitorRepositoryPort):
    """In-memory repository for tests."""

    def __init__(self, concepts: list[dict]) -> None:
        self._concepts = {c["concept_id"]: c for c in concepts}

    def save(self, data: dict) -> None:
        self._concepts[data["concept_id"]] = data

    def load(self, key: str) -> dict | None:
        return self._concepts.get(key)


class TestM5ProductionMonitor:
    """Test suite for m5-production-monitor."""

    def test_skill_structure_valid(self, tmp_path: Path) -> None:
        """Test skill has valid structure."""
        skill_dir = tmp_path / "m5-production-monitor"
        skill_dir.mkdir()
        assert skill_dir.exists()

    def test_contracts_present(self, tmp_path: Path) -> None:
        """Test contracts are present."""
        contract_path = tmp_path / "acceptance" / "contract.yaml"
        contract_path.parent.mkdir(parents=True, exist_ok=True)
        contract_path.write_text("contract_version: 1.0.0\n")
        assert contract_path.exists()

    def test_concept_embryo_classification(self) -> None:
        """Test embryo classification."""
        concept = M5ConceptEntity(
            concept_id="c1",
            phase="detectBirth",
            maturity_score=0.2,
            state="active",
        )
        assert concept.is_embryo() is True
        assert concept.get_target_phase() == "develop"

    def test_concept_mature_classification(self) -> None:
        """Test mature classification."""
        concept = M5ConceptEntity(
            concept_id="c2",
            phase="stabilize",
            maturity_score=0.9,
            state="active",
        )
        assert concept.is_mature() is True
        assert concept.get_target_phase() == "integrate"

    def test_service_generate_report(self) -> None:
        """Test report generation."""
        concepts = [
            M5ConceptEntity(concept_id="c1", phase="detectBirth", maturity_score=0.2, state="active"),
            M5ConceptEntity(concept_id="c2", phase="develop", maturity_score=0.5, state="active"),
            M5ConceptEntity(concept_id="c3", phase="stabilize", maturity_score=0.7, state="active"),
            M5ConceptEntity(concept_id="c4", phase="integrate", maturity_score=0.9, state="active"),
        ]

        repo = InMemoryRepository([])
        service = M5MonitorService(None, repo)  # type: ignore[arg-type]
        report = service.generate_report(concepts)

        assert report["total"] == 4
        assert len(report["embryos"]) == 1
        assert len(report["developing"]) == 1
        assert len(report["stable"]) == 1
        assert len(report["integrated"]) == 1

    def test_usecase_execute_with_registry(self, tmp_path: Path) -> None:
        """Test use case execution with registry."""
        registry = tmp_path / "concepts.json"
        registry.write_text(
            json.dumps(
                [
                    {"concept_id": "c1", "phase": "detectBirth", "maturity_score": 0.2, "state": "active"},
                    {"concept_id": "c2", "phase": "develop", "maturity_score": 0.5, "state": "active"},
                ]
            ),
            encoding="utf-8",
        )

        repo = InMemoryRepository([])
        service = M5MonitorService(None, repo)  # type: ignore[arg-type]
        usecase = M5MonitorUseCase(repo, service=service)

        result = usecase.execute({"concept_registry_path": str(registry), "m5_threshold": 0.7})

        assert "report" in result
        assert result["ready_for_integration_count"] == 0
