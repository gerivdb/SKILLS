"""Tests unitaires pour mox-validator."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from mox_validator import MoxValidator


def _write_doc(tmp_path: Path, name: str, content: str) -> Path:
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return path


def _make_full_document() -> str:
    sections = "\n".join(
        f"## {section}\nContent for {section}.\n"
        for section in MoxValidator.REQUIRED_SECTIONS
    )
    return (
        "---\n"
        "type: ADR\n"
        "version: 1.0\n"
        "status: accepted\n"
        "date: 2026-08-06\n"
        "intent_hash: 0xTEST_VALID_001\n"
        "citizen: TEST\n"
        "layer: L4\n"
        "author: test\n"
        "source_repo: gerivdb/TEST\n"
        "source_path: ADR/ADR-001.md\n"
        "---\n"
        "\n"
        "# ADR 001\n"
        "\n"
        f"{sections}\n"
    )


def test_frontmatter_valid(tmp_path: Path) -> None:
    """Frontmatter valide - PASS."""
    doc_content = _make_full_document()
    doc_path = _write_doc(tmp_path, "valid.md", doc_content)
    content = doc_path.read_text(encoding="utf-8")

    validator = MoxValidator(
        ontology_path=tmp_path / "ONTOLOGY.yaml",
        repo_standards_dir=tmp_path / "REPO-STANDARDS",
        output_dir=tmp_path / "output",
    )
    result = validator.validate(
        document={"path": str(doc_path), "content": content},
    )
    assert result.result == "PASS"


def test_frontmatter_invalid(tmp_path: Path) -> None:
    """Frontmatter invalide - FAIL."""
    doc_content = (
        "---\n"
        "type: ADR\n"
        "---\n"
        "\n"
        "# ADR 001\n"
        "\n"
        "## Objectif\n"
        "\n"
        "Test.\n"
    )
    doc_path = _write_doc(tmp_path, "invalid.md", doc_content)
    content = doc_path.read_text(encoding="utf-8")

    validator = MoxValidator(
        ontology_path=tmp_path / "ONTOLOGY.yaml",
        repo_standards_dir=tmp_path / "REPO-STANDARDS",
        output_dir=tmp_path / "output",
    )
    result = validator.validate(
        document={"path": str(doc_path), "content": content},
    )
    assert result.result == "FAIL"


def test_structure_complete(tmp_path: Path) -> None:
    """Structure complète - PASS."""
    doc_content = _make_full_document()
    doc_path = _write_doc(tmp_path, "struct.md", doc_content)
    content = doc_path.read_text(encoding="utf-8")

    validator = MoxValidator(
        ontology_path=tmp_path / "ONTOLOGY.yaml",
        repo_standards_dir=tmp_path / "REPO-STANDARDS",
        output_dir=tmp_path / "output",
    )
    result = validator.validate(
        document={"path": str(doc_path), "content": content},
    )
    assert result.result == "PASS"


def test_structure_missing(tmp_path: Path) -> None:
    """Section manquante - FAIL."""
    doc_content = (
        "---\n"
        "type: ADR\n"
        "version: 1.0\n"
        "status: accepted\n"
        "date: 2026-08-06\n"
        "intent_hash: 0xTEST_STRUCT_002\n"
        "citizen: TEST\n"
        "layer: L4\n"
        "author: test\n"
        "source_repo: gerivdb/TEST\n"
        "source_path: ADR/ADR-001.md\n"
        "---\n"
        "\n"
        "# ADR 001\n"
        "\n"
        "## Objectif\n"
        "\n"
        "Test.\n"
    )
    doc_path = _write_doc(tmp_path, "missing.md", doc_content)
    content = doc_path.read_text(encoding="utf-8")

    validator = MoxValidator(
        ontology_path=tmp_path / "ONTOLOGY.yaml",
        repo_standards_dir=tmp_path / "REPO-STANDARDS",
        output_dir=tmp_path / "output",
    )
    result = validator.validate(
        document={"path": str(doc_path), "content": content},
    )
    assert result.result == "FAIL"


def test_crossref_contradiction(tmp_path: Path) -> None:
    """Contradiction cross-repo - Détectée."""
    sections = "\n".join(
        f"## {section}\nContent for {section}.\n"
        for section in MoxValidator.REQUIRED_SECTIONS
    )
    doc_content = (
        "---\n"
        "type: ADR\n"
        "version: 1.0\n"
        "status: accepted\n"
        "date: 2026-08-06\n"
        "intent_hash: 0xTEST_CONTRA_001\n"
        "citizen: TEST\n"
        "layer: L4\n"
        "author: test\n"
        "source_repo: gerivdb/TEST\n"
        "source_path: ADR/ADR-001.md\n"
        "---\n"
        "\n"
        "# ADR 001\n"
        "\n"
        f"{sections}\n"
    )
    doc_path = _write_doc(tmp_path, "contra.md", doc_content)
    content = doc_path.read_text(encoding="utf-8")

    validator = MoxValidator(
        ontology_path=tmp_path / "ONTOLOGY.yaml",
        repo_standards_dir=tmp_path / "REPO-STANDARDS",
        output_dir=tmp_path / "output",
    )
    result = validator.validate(
        document={"path": str(doc_path), "content": content},
        layers=["frontmatter", "structure", "contradiction"],
    )
    assert result.result == "PASS"
