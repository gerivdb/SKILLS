"""Tests unitaires pour artifact-quality-checker."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from artifact_quality_checker import ArtifactQualityChecker


def _write_doc(tmp_path: Path, name: str, content: str) -> Path:
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return path


def _make_full_document() -> str:
    sections = "\n".join(
        f"## {section}\nContent for {section}.\n"
        for section in ArtifactQualityChecker.REQUIRED_SECTIONS
    )
    return (
        "---\n"
        "type: ADR\n"
        "version: 1.0\n"
        "status: accepted\n"
        "date: 2026-08-06\n"
        "intent_hash: 0xTEST_ARTIFACT_001\n"
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


def test_probes_pass(tmp_path: Path) -> None:
    """Document conforme - 100% probes passent."""
    doc_content = _make_full_document()
    doc_path = _write_doc(tmp_path, "valid.md", doc_content)

    checker = ArtifactQualityChecker(output_dir=tmp_path / "reports")
    artifact = checker.load_artifact(doc_path)
    report = checker.check(artifact)

    assert report.score == 1.0
    assert report.result == "PASS"
    assert report.artifact_type == "ADR"


def test_probes_fail(tmp_path: Path) -> None:
    """Document non conforme - P-106/P-107 échouent."""
    doc_content = (
        "---\n"
        "type: ADR\n"
        "---\n"
        "\n"
        "# ADR 001\n"
        "\n"
        "## Objectif\n"
        "\n"
        "Test NotebookLM.\n"
    )
    doc_path = _write_doc(tmp_path, "invalid.md", doc_content)

    checker = ArtifactQualityChecker(output_dir=tmp_path / "reports")
    artifact = checker.load_artifact(doc_path)
    report = checker.check(artifact)

    assert report.result == "FAIL"
    assert any(probe.id in ("P-106", "P-107") and probe.status == "FAIL" for probe in report.probes)


def test_report_generated(tmp_path: Path) -> None:
    """Rapport généré - Fichier YAML créé."""
    doc_content = _make_full_document()
    doc_path = _write_doc(tmp_path, "report.md", doc_content)

    checker = ArtifactQualityChecker(output_dir=tmp_path / "reports")
    artifact = checker.load_artifact(doc_path)
    report = checker.check(artifact)
    report_path = checker.generate_report(report)

    assert report_path.exists()
    assert report_path.suffix == ".yaml"
