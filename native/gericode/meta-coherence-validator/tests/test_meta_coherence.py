"""
Tests for Meta Coherence Validator.
"""

import sys
import os
from pathlib import Path

# Add skill root to path for imports
SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))

import pytest
from unittest.mock import MagicMock


class TestReference:
    """Tests for Reference value object."""

    def test_valid_reference_creation(self):
        from domain.value_objects.reference_vo import Reference
        ref = Reference(type="design", path="unified-design/designs/foo.yaml")
        assert ref.type == "design"
        assert ref.path == "unified-design/designs/foo.yaml"
        assert str(ref) == "design:unified-design/designs/foo.yaml"

    def test_invalid_reference_type_raises(self):
        from domain.value_objects.reference_vo import Reference
        with pytest.raises(ValueError):
            Reference(type="invalid", path="foo")

    def test_from_string_valid(self):
        from domain.value_objects.reference_vo import Reference
        ref = Reference.from_string("skill:D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/progress-sync/")
        assert ref.type == "skill"
        assert ref.path == "D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/progress-sync/"

    def test_from_string_invalid_raises(self):
        from domain.value_objects.reference_vo import Reference
        with pytest.raises(ValueError):
            Reference.from_string("no-colon-here")


class TestPrdMocEntity:
    """Tests for PrdMoc entity."""

    def test_add_reference(self):
        from domain.entities.prd_moc_entity import PrdMoc
        from domain.value_objects.reference_vo import Reference
        prd_moc = PrdMoc(path="test.md", title="Test", intent_hash="0xTEST")
        ref = Reference(type="design", path="foo.yaml")
        prd_moc.add_reference(ref)
        assert len(prd_moc.references) == 1

    def test_add_missing_reference(self):
        from domain.entities.prd_moc_entity import PrdMoc
        prd_moc = PrdMoc(path="test.md", title="Test", intent_hash="0xTEST")
        prd_moc.add_missing_reference("design:missing.yaml", "File not found")
        assert len(prd_moc.missing_references) == 1

    def test_compute_score_perfect(self):
        from domain.entities.prd_moc_entity import PrdMoc
        from domain.value_objects.reference_vo import Reference
        prd_moc = PrdMoc(path="test.md", title="Test", intent_hash="0xTEST")
        ref = Reference(type="design", path="foo.yaml")
        prd_moc.add_reference(ref)
        score = prd_moc.compute_score(total_references=1)
        assert score == 1.0

    def test_compute_score_with_missing(self):
        from domain.entities.prd_moc_entity import PrdMoc
        from domain.value_objects.reference_vo import Reference
        prd_moc = PrdMoc(path="test.md", title="Test", intent_hash="0xTEST")
        ref = Reference(type="design", path="foo.yaml")
        prd_moc.add_reference(ref)
        prd_moc.add_missing_reference("design:missing.yaml", "Not found")
        score = prd_moc.compute_score(total_references=2)
        assert score == 0.5


class TestMetaCoherenceService:
    """Tests for MetaCoherenceService."""

    def setup_method(self):
        """Set up test fixtures."""
        from application.services.meta_coherence_service import MetaCoherenceService
        from pathlib import Path
        from unittest.mock import MagicMock

        self.mock_reader = MagicMock()
        self.mock_checker = MagicMock()
        self.service = MetaCoherenceService(
            prd_moc_reader=self.mock_reader,
            reference_checker=self.mock_checker,
            base_path=Path("/fake/path"),
        )

    def test_validate_empty_list(self):
        """Test validation with no PRD MOC documents."""
        self.mock_reader.read_prd_mocs.return_value = []
        report = self.service.validate(
            prd_moc_paths=[],
            unified_design_path=Path("/designs"),
            ontology_path=Path("/ontology"),
            skills_registry=Path("/skills/REGISTRY.yaml"),
            boot_sequence_path=Path("/boot.md"),
        )
        assert report["global_score"] == 1.0
        assert report["prd_mocs_validated"] == 0
        assert report["blocked"] is False

    def test_validate_with_valid_references(self):
        """Test validation with all valid references."""
        self.mock_reader.read_prd_mocs.return_value = [
            {
                "path": "test.md",
                "title": "Test PRD MOC",
                "content": "References: `design:foo.yaml` `concept:bar`",
            }
        ]
        self.mock_checker.check_design_exists.return_value = True
        self.mock_checker.check_concept_exists.return_value = True
        self.mock_checker.check_skill_exists.return_value = True
        self.mock_checker.check_citizen_exists.return_value = True
        self.mock_checker.check_boot_step_exists.return_value = True
        self.mock_checker.check_prd_moc_exists.return_value = True
        self.mock_checker.check_adr_exists.return_value = True
        self.mock_checker.check_ontology_file_exists.return_value = True

        report = self.service.validate(
            prd_moc_paths=[Path("test.md")],
            unified_design_path=Path("/designs"),
            ontology_path=Path("/ontology"),
            skills_registry=Path("/skills/REGISTRY.yaml"),
            boot_sequence_path=Path("/boot.md"),
        )
        assert report["global_score"] == 1.0
        assert report["blocked"] is False

    def test_validate_with_missing_references(self):
        """Test validation with missing references."""
        self.mock_reader.read_prd_mocs.return_value = [
            {
                "path": "test.md",
                "title": "Test PRD MOC",
                "content": "References: `design:missing.yaml`",
            }
        ]
        self.mock_checker.check_design_exists.return_value = False

        report = self.service.validate(
            prd_moc_paths=[Path("test.md")],
            unified_design_path=Path("/designs"),
            ontology_path=Path("/ontology"),
            skills_registry=Path("/skills/REGISTRY.yaml"),
            boot_sequence_path=Path("/boot.md"),
        )
        assert report["global_score"] < 1.0
        assert len(report["details"][0]["missing_references"]) == 1
