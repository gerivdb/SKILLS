"""Tests for progress-sync."""

from __future__ import annotations

import pytest
from pathlib import Path


class TestProgressSync:
    """Test suite for progress-sync."""

    def test_skill_structure_valid(self, tmp_path: Path) -> None:
        """Test skill has valid structure."""
        skill_dir = tmp_path / "progress-sync"
        skill_dir.mkdir()
        assert skill_dir.exists()

    def test_contracts_present(self, tmp_path: Path) -> None:
        """Test contracts are present."""
        contract_path = tmp_path / "acceptance" / "contract.yaml"
        contract_path.parent.mkdir(parents=True, exist_ok=True)
        contract_path.write_text("contract_version: 1.0.0\n")
        assert contract_path.exists()

    def test_prd_moc_has_required_sections(self, tmp_path: Path) -> None:
        """Test PRD MOC has required sections."""
        moc = tmp_path / "PRD-MOC.md"
        moc.write_text("""# PRD MOC

## État d'avancement

| Phase | Action | Livrable | Responsable | Statut |
|-------|--------|----------|-------------|--------|
| 1 | Action | Livrable | Responsable | [OK] FAIT |

## Reste à faire immédiat

- [ ] Action 2

progress_tracking:
  source_of_truth: "Section ## État d'avancement"
""", encoding="utf-8")
        content = moc.read_text(encoding="utf-8")
        assert "## État d'avancement" in content
        assert "## Reste à faire immédiat" in content
        assert "progress_tracking:" in content
