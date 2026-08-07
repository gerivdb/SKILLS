"""Tests pour skill-scaffold."""

from __future__ import annotations

import pytest

from skill_scaffold import SkillScaffoldError, scaffold_skill


def test_scaffold_creates_directory(tmp_path):
    skill_dir = scaffold_skill(
        skill_name="test-skill",
        description="Test skill",
        citizen="DEV-EXPERIENCE",
        layer="L4",
        target_dir=tmp_path,
    )
    assert skill_dir.exists()
    assert skill_dir.is_dir()


def test_scaffold_creates_files(tmp_path):
    skill_dir = scaffold_skill(
        skill_name="test-skill",
        description="Test skill",
        target_dir=tmp_path,
    )
    assert (skill_dir / "SKILL.md").exists()
    assert (skill_dir / "test_skill.py").exists()
    assert (skill_dir / "tests" / "conftest.py").exists()
    assert (skill_dir / "tests" / "test_test_skill.py").exists()


def test_scaffold_raises_if_exists(tmp_path):
    scaffold_skill(
        skill_name="test-skill",
        description="Test skill",
        target_dir=tmp_path,
    )
    with pytest.raises(SkillScaffoldError):
        scaffold_skill(
            skill_name="test-skill",
            description="Test skill",
            target_dir=tmp_path,
        )
