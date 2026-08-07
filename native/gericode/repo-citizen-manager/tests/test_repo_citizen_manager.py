"""Tests pour repo-citizen-manager."""

from __future__ import annotations

from pathlib import Path
import pytest

from repo_citizen_manager import (
    RepoCitizenError,
    check_citizen,
    create_bridge,
    create_verse,
    register_citizen,
    register_skill,
    verify_repo,
)


def test_verify_repo_exists(tmp_path):
    known = tmp_path / "known_repositories.yaml"
    known.write_text(
        "P0_REPOS:\n"
        "- name: TEST\n"
        "  local_path: D:\\\\DO\\\\WEB\\\\TOOLS\\\\L4-TOOLS\\\\TEST\n",
        encoding="utf-8",
    )
    assert verify_repo("TEST", known) is True


def test_verify_repo_missing(tmp_path):
    known = tmp_path / "known_repositories.yaml"
    known.write_text("P0_REPOS:\n- name: OTHER\n", encoding="utf-8")
    assert verify_repo("TEST", known) is False


def test_check_citizen_true(tmp_path):
    citizens = tmp_path / "citizens.yaml"
    citizens.write_text(
        "citizens:\n"
        "  - id: TEST\n"
        "    intent_hash: 0xTEST\n",
        encoding="utf-8",
    )
    assert check_citizen("TEST", citizens) is True


def test_check_citizen_false(tmp_path):
    citizens = tmp_path / "citizens.yaml"
    citizens.write_text("citizens:\n  - id: OTHER\n", encoding="utf-8")
    assert check_citizen("TEST", citizens) is False


def test_create_verse(tmp_path):
    verses_dir = tmp_path / "verses"
    verses_dir.mkdir()
    verse_path = create_verse("TEST", verses_dir)
    assert verse_path.exists()
    assert verse_path.name == "test-verse.md"


def test_create_verse_raises_if_exists(tmp_path):
    verses_dir = tmp_path / "verses"
    verses_dir.mkdir()
    create_verse("TEST", verses_dir)
    with pytest.raises(RepoCitizenError):
        create_verse("TEST", verses_dir)


def test_register_citizen(tmp_path):
    citizens = tmp_path / "citizens.yaml"
    citizens.write_text("citizens:\n", encoding="utf-8")
    register_citizen("TEST", citizens)
    data = citizens.read_text(encoding="utf-8")
    assert "id: TEST" in data


def test_create_bridge(tmp_path):
    bridges = tmp_path / "BRIDGES.yaml"
    bridges.write_text("repos:\n", encoding="utf-8")
    entry = create_bridge("TEST", bridges, full_name="gerivdb/TEST", layer="L4_TOOLS", local_path="D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\TEST")
    assert entry["full_name"] == "gerivdb/TEST"
    assert entry["layer"] == "L4_TOOLS"
    assert "ONTOLOGY" in entry["bridges"]
    data = bridges.read_text(encoding="utf-8")
    assert "gerivdb/TEST" in data


def test_create_bridge_idempotent(tmp_path):
    bridges = tmp_path / "BRIDGES.yaml"
    bridges.write_text("repos:\n", encoding="utf-8")
    create_bridge("TEST", bridges, full_name="gerivdb/TEST", layer="L4_TOOLS")
    create_bridge("TEST", bridges, full_name="gerivdb/TEST", layer="L4_TOOLS")
    data = bridges.read_text(encoding="utf-8")
    assert data.count("gerivdb/TEST") == 1


def test_register_skill(tmp_path):
    registry = tmp_path / "REGISTRY.yaml"
    registry.write_text("skills:\nregistry:\n  version: 1.0.0\n  total_skills: 0\n", encoding="utf-8")
    register_skill("test-skill", registry, source_repo="gerivdb/GeriCode")
    data = registry.read_text(encoding="utf-8")
    assert "test-skill" in data
    assert "gerivdb/GeriCode" in data
    assert "total_skills: 1" in data


def test_register_skill_raises_if_exists(tmp_path):
    registry = tmp_path / "REGISTRY.yaml"
    registry.write_text(
        "skills:\n"
        "  - name: test-skill\n"
        "registry:\n"
        "  version: 1.0.0\n"
        "  total_skills: 1\n",
        encoding="utf-8",
    )
    with pytest.raises(RepoCitizenError):
        register_skill("test-skill", registry, source_repo="gerivdb/GeriCode")
