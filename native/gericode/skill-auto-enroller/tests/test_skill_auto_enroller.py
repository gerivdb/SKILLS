"""Tests pour skill-auto-enroller."""

from __future__ import annotations

from pathlib import Path
import pytest

from skill_auto_enroller import SkillAutoEnroller, SkillAutoEnrollerError


def test_enroll_new_skill(tmp_path):
    known = tmp_path / "known_repositories.yaml"
    known.write_text(
        "P0_REPOS:\n"
        "- name: TEST\n"
        "  entity_type: REPO\n"
        "  full_name: gerivdb/TEST\n"
        "  local_path: D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\TEST\n"
        "  url: https://github.com/gerivdb/TEST\n"
        "  layer: L4_TOOLS\n"
        "  status: ACTIVE\n",
        encoding="utf-8",
    )
    citizens = tmp_path / "citizens.yaml"
    citizens.write_text("citizens:\n", encoding="utf-8")
    verses = tmp_path / "verses"
    verses.mkdir()
    bridges = tmp_path / "BRIDGES.yaml"
    bridges.write_text("repos:\n", encoding="utf-8")
    registry = tmp_path / "REGISTRY.yaml"
    registry.write_text("skills:\nregistry:\n  version: 1.0.0\n  total_skills: 0\n", encoding="utf-8")
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()

    enroller = SkillAutoEnroller(known, citizens, verses, bridges, registry, skills_dir)
    report = enroller.enroll(
        skill_name="test-skill",
        repo_name="TEST",
        layer="L4",
        local_path=tmp_path / "TEST",
        source_path=".kilo/skills/test-skill/SKILL.md",
    )
    assert report["errors"] == []
    assert len(report["steps"]) == 5


def test_enroll_missing_repo(tmp_path):
    known = tmp_path / "known_repositories.yaml"
    known.write_text("P0_REPOS:\n- name: OTHER\n", encoding="utf-8")
    citizens = tmp_path / "citizens.yaml"
    citizens.write_text("citizens:\n", encoding="utf-8")
    verses = tmp_path / "verses"
    verses.mkdir()
    bridges = tmp_path / "BRIDGES.yaml"
    bridges.write_text("repos:\n", encoding="utf-8")
    registry = tmp_path / "REGISTRY.yaml"
    registry.write_text("skills:\n", encoding="utf-8")
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()

    enroller = SkillAutoEnroller(known, citizens, verses, bridges, registry, skills_dir)
    report = enroller.enroll(
        skill_name="test-skill",
        repo_name="TEST",
        layer="L4",
    )
    assert len(report["errors"]) > 0
    assert report["rolled_back"] is False


def test_enroll_rollback_on_failure(tmp_path):
    known = tmp_path / "known_repositories.yaml"
    known.write_text(
        "P0_REPOS:\n"
        "- name: TEST\n"
        "  entity_type: REPO\n"
        "  full_name: gerivdb/TEST\n"
        "  local_path: D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\TEST\n"
        "  url: https://github.com/gerivdb/TEST\n"
        "  layer: L4_TOOLS\n"
        "  status: ACTIVE\n",
        encoding="utf-8",
    )
    citizens = tmp_path / "citizens.yaml"
    citizens.write_text("citizens:\n", encoding="utf-8")
    verses = tmp_path / "verses"
    verses.mkdir()
    bridges = tmp_path / "BRIDGES.yaml"
    bridges.write_text("repos:\n", encoding="utf-8")
    registry = tmp_path / "REGISTRY.yaml"
    # Invalid YAML that will cause a parse error
    registry.write_text("skills:\n  - name: test\n    bad: [", encoding="utf-8")
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()

    enroller = SkillAutoEnroller(known, citizens, verses, bridges, registry, skills_dir)
    report = enroller.enroll(
        skill_name="test-skill",
        repo_name="TEST",
        layer="L4",
    )
    assert len(report["errors"]) > 0
