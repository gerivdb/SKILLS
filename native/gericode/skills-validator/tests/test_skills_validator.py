"""Tests pour skills-validator."""

from __future__ import annotations

from pathlib import Path
import pytest

from skills_validator import SkillsValidator, SkillValidationError


def test_validate_valid_skill(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    skill_dir = skills_dir / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\n"
        "name: test-skill\n"
        "description: Test skill\n"
        "triggers:\n"
        "  - test\n"
        "domain: foundational\n"
        "version: 1.0.0\n"
        "author: gerivdb\n"
        "license: MIT\n"
        "status: active\n"
        "---\n"
        "# Test\n",
        encoding="utf-8",
    )
    validator = SkillsValidator(
        skills_dir=skills_dir,
        taxonomy_path=tmp_path / "TAXONOMY.md",
        registry_path=tmp_path / "REGISTRY.yaml",
    )
    report = validator.validate_all()
    assert len(report["errors"]) == 0


def test_validate_missing_field(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    skill_dir = skills_dir / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\n"
        "name: test-skill\n"
        "---\n"
        "# Test\n",
        encoding="utf-8",
    )
    validator = SkillsValidator(
        skills_dir=skills_dir,
        taxonomy_path=tmp_path / "TAXONOMY.md",
        registry_path=tmp_path / "REGISTRY.yaml",
    )
    report = validator.validate_all()
    assert any("Missing fields" in str(e["message"]) for e in report["errors"])


def test_detect_duplicate_names(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    for name in ["test-skill-a", "test-skill-b"]:
        skill_dir = skills_dir / name
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            "name: test-skill\n"
            "description: Test\n"
            "triggers:\n"
            "  - test\n"
            "domain: foundational\n"
            "version: 1.0.0\n"
            "author: gerivdb\n"
            "license: MIT\n"
            "status: active\n"
            "---\n",
            encoding="utf-8",
        )
    validator = SkillsValidator(
        skills_dir=skills_dir,
        taxonomy_path=tmp_path / "TAXONOMY.md",
        registry_path=tmp_path / "REGISTRY.yaml",
    )
    report = validator.validate_all()
    assert "test-skill" in report["duplicates"]
