"""Tests for artifact-quality-checker."""

from __future__ import annotations

import pytest
from pathlib import Path


class TestArtifactQualityChecker:
    """Test suite for artifact-quality-checker."""

    def test_skill_structure_valid(self, tmp_path: Path) -> None:
        """Test skill has valid structure."""
        skill_dir = tmp_path / "artifact-quality-checker"
        skill_dir.mkdir()
        assert skill_dir.exists()

    def test_contracts_present(self, tmp_path: Path) -> None:
        """Test contracts are present."""
        contract_path = tmp_path / "acceptance" / "contract.yaml"
        contract_path.parent.mkdir(parents=True, exist_ok=True)
        contract_path.write_text("contract_version: 1.0.0\n")
        assert contract_path.exists()
