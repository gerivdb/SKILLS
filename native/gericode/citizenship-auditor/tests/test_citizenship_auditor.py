"""Tests pour citizenship-auditor."""

from __future__ import annotations

from pathlib import Path
import pytest

from citizenship_auditor import CitizenshipAuditor


def test_audit_p801_pass(tmp_path):
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
    citizens.write_text("citizens:\n  - id: TEST\n", encoding="utf-8")
    verses = tmp_path / "verses"
    verses.mkdir()
    (verses / "test-verse.md").write_text("---\ncitizen: TEST\n---\n", encoding="utf-8")
    skills = tmp_path / "skills"
    skills.mkdir()
    registry = tmp_path / "REGISTRY.yaml"
    registry.write_text("skills:\n  - name: test-skill\n    source_repo: gerivdb/TEST\n", encoding="utf-8")

    auditor = CitizenshipAuditor(known, citizens, verses, skills, registry)
    report = auditor.audit()
    assert report["p801_repos_are_citizens"]["passed"] is True


def test_audit_p802_fail(tmp_path):
    known = tmp_path / "known_repositories.yaml"
    known.write_text("P0_REPOS:\n- name: TEST\n", encoding="utf-8")
    citizens = tmp_path / "citizens.yaml"
    citizens.write_text("citizens:\n  - id: TEST\n", encoding="utf-8")
    verses = tmp_path / "verses"
    verses.mkdir()
    # No verse for TEST
    skills = tmp_path / "skills"
    skills.mkdir()
    registry = tmp_path / "REGISTRY.yaml"
    registry.write_text("skills:\n", encoding="utf-8")

    auditor = CitizenshipAuditor(known, citizens, verses, skills, registry)
    report = auditor.audit()
    assert report["p802_citizens_have_verses"]["passed"] is False


def test_audit_p806_fail(tmp_path):
    known = tmp_path / "known_repositories.yaml"
    known.write_text("P0_REPOS:\n- name: TEST\n", encoding="utf-8")
    citizens = tmp_path / "citizens.yaml"
    citizens.write_text("citizens:\n  - id: TEST\n", encoding="utf-8")
    verses = tmp_path / "verses"
    verses.mkdir()
    (verses / "test-verse.md").write_text("---\ncitizen: TEST\n---\n", encoding="utf-8")
    skills = tmp_path / "skills"
    skills.mkdir()
    skill_dir = skills / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: test-skill\n---\n", encoding="utf-8")
    registry = tmp_path / "REGISTRY.yaml"
    registry.write_text("skills:\n", encoding="utf-8")

    auditor = CitizenshipAuditor(known, citizens, verses, skills, registry)
    report = auditor.audit()
    assert report["p806_skills_in_registry"]["passed"] is False


def test_audit_p807_fail(tmp_path):
    known = tmp_path / "known_repositories.yaml"
    known.write_text("P0_REPOS:\n- name: TEST\n", encoding="utf-8")
    citizens = tmp_path / "citizens.yaml"
    citizens.write_text("citizens:\n  - id: TEST\n", encoding="utf-8")
    verses = tmp_path / "verses"
    verses.mkdir()
    (verses / "test-verse.md").write_text("---\ncitizen: TEST\n---\n", encoding="utf-8")
    skills = tmp_path / "skills"
    skills.mkdir()
    registry = tmp_path / "REGISTRY.yaml"
    registry.write_text(
        "skills:\n"
        "  - name: test-skill\n"
        "    description: Test\n",
        encoding="utf-8",
    )

    auditor = CitizenshipAuditor(known, citizens, verses, skills, registry)
    report = auditor.audit()
    assert report["p807_registry_has_source_repo"]["passed"] is False
