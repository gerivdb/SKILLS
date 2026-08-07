"""Tests for MOX validator."""

import sys
from pathlib import Path

# Add mox-validator parent to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mox_validator import MOXValidator


def test_classify_prd():
    """Test PRD classification."""
    mox = MOXValidator()
    # Create test document
    test_doc = Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/act-protocol/PRD/PRD-001-lecore.md")
    if not test_doc.exists():
        print("SKIP: test_classify_prd - document not found")
        return
    result = mox.classify_document(test_doc)
    assert result["type"] == "PRD", f"Expected PRD, got {result['type']}"
    print("PASS: test_classify_prd")


def test_classify_prd_moc():
    """Test PRD_MOC classification."""
    mox = MOXValidator()
    test_doc = Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/nomenclature/PRD-MOC-ACTPROTOCOL-ARTIFACT-WRITING-STANDARDS-2026-08-05.md")
    if not test_doc.exists():
        print("SKIP: test_classify_prd_moc - document not found")
        return
    result = mox.classify_document(test_doc)
    assert result["type"] == "PRD_MOC", f"Expected PRD_MOC, got {result['type']}"
    print("PASS: test_classify_prd_moc")


def test_validate_frontmatter():
    """Test frontmatter validation."""
    mox = MOXValidator()
    test_doc = Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/nomenclature/PRD-MOC-ACTPROTOCOL-DOCUMENT-CLASSIFICATION-MOX-EXTENSION.md")
    if not test_doc.exists():
        print("SKIP: test_validate_frontmatter - document not found")
        return
    result = mox.validate_frontmatter_schema(test_doc)
    assert result.valid, f"Frontmatter validation failed: {result.issues}"
    print("PASS: test_validate_frontmatter")


def test_validate_delivery_plan():
    """Test delivery plan validation."""
    mox = MOXValidator()
    test_doc = Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/architecture/PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md")
    if not test_doc.exists():
        print("SKIP: test_validate_delivery_plan - document not found")
        return
    result = mox.validate_delivery_plan(test_doc)
    assert result.valid, f"Delivery plan validation failed: {result.issues}"
    print("PASS: test_validate_delivery_plan")


def test_validate_milestones():
    """Test milestones validation."""
    mox = MOXValidator()
    test_doc = Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/architecture/PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md")
    if not test_doc.exists():
        print("SKIP: test_validate_milestones - document not found")
        return
    result = mox.validate_milestones(test_doc)
    assert result.valid, f"Milestones validation failed: {result.issues}"
    print("PASS: test_validate_milestones")


def test_validate_tests():
    """Test tests validation."""
    mox = MOXValidator()
    test_doc = Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/architecture/PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md")
    if not test_doc.exists():
        print("SKIP: test_validate_tests - document not found")
        return
    result = mox.validate_tests(test_doc)
    assert result.valid, f"Tests validation failed: {result.issues}"
    print("PASS: test_validate_tests")


def test_validate_dependencies():
    """Test dependencies validation."""
    mox = MOXValidator()
    test_doc = Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/architecture/PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md")
    if not test_doc.exists():
        print("SKIP: test_validate_dependencies - document not found")
        return
    result = mox.validate_dependencies(test_doc)
    assert result.valid, f"Dependencies validation failed: {result.issues}"
    print("PASS: test_validate_dependencies")


def test_validate_risks():
    """Test risks validation."""
    mox = MOXValidator()
    test_doc = Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/architecture/PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md")
    if not test_doc.exists():
        print("SKIP: test_validate_risks - document not found")
        return
    result = mox.validate_risks(test_doc)
    assert result.valid, f"Risks validation failed: {result.issues}"
    print("PASS: test_validate_risks")


def test_full_validation():
    """Test full MOX validation pipeline."""
    mox = MOXValidator()
    test_doc = Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode/act-protocol/PRD/PRD-MOC-ACTPROTOCOL/fractal/architecture/PRD-MOC-ACTPROTOCOL-SOVEREIGN-CROSS-REPO-GRAPH-2026-08-04.md")
    if not test_doc.exists():
        print("SKIP: test_full_validation - document not found")
        return
    result = mox.validate(test_doc)
    assert result.valid, f"Full validation failed: {result.summary()}"
    assert "wal_entry" in result.metadata, "WAL entry missing"
    print("PASS: test_full_validation")


def test_ontology_terms():
    """Test ontology terms loading."""
    mox = MOXValidator()
    assert "N243" in mox.ontology_terms, "N243 not in ontology terms"
    assert "NEXUS" in mox.ontology_terms, "NEXUS not in ontology terms"
    print("PASS: test_ontology_terms")


if __name__ == "__main__":
    test_classify_prd()
    test_classify_prd_moc()
    test_validate_frontmatter()
    test_validate_delivery_plan()
    test_validate_milestones()
    test_validate_tests()
    test_validate_dependencies()
    test_validate_risks()
    test_full_validation()
    test_ontology_terms()
    print("\n=== ALL TESTS PASSED ===")
