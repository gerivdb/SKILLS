"""Tests pour registry-prune."""

from __future__ import annotations

from pathlib import Path
import pytest

from registry_prune import RegistryPrune, RegistryPruneError


def test_prune_orphan_skills(tmp_path):
    registry_yaml = tmp_path / "REGISTRY.yaml"
    registry_yaml.write_text(
        "skills:\n"
        "  - name: orphan-skill\n"
        "    description: Orphan\n"
        "    type: foundational\n"
        "    version: 1.0.0\n"
        "    author: gerivdb\n"
        "    license: MIT\n"
        "    status: active\n"
        "    created: '2026-08-07'\n"
        "    updated: '2026-08-07'\n"
        "    phi_weight: 0.005\n"
        "    path: ..\\L4-TOOLS\\orphan-skill\\SKILL.md\n"
        "    source: native\n"
        "    assimilation_status: N/A\n"
        "    source_repo: gerivdb/NONEXISTENT\n"
        "    consumes_from: []\n",
        encoding="utf-8",
    )
    registry_json = tmp_path / "registry.json"
    registry_json.write_text("{\"skills\": []}", encoding="utf-8")
    citizens = tmp_path / "citizens.yaml"
    citizens.write_text("citizens:\n  - id: NONEXISTENT\n", encoding="utf-8")
    bridges = tmp_path / "BRIDGES.yaml"
    bridges.write_text("repos:\n  NONEXISTENT:\n    full_name: gerivdb/NONEXISTENT\n", encoding="utf-8")
    known = tmp_path / "known_repositories.yaml"
    known.write_text("P0_REPOS:\n- name: EXISTING\n", encoding="utf-8")

    prune = RegistryPrune(registry_yaml, registry_json, citizens, bridges, known)
    report = prune.prune(dry_run=True)
    assert report["dry_run"] is True
    assert "errors" in report


def test_prune_orphan_citizens(tmp_path):
    registry_yaml = tmp_path / "REGISTRY.yaml"
    registry_yaml.write_text("skills:\n", encoding="utf-8")
    registry_json = tmp_path / "registry.json"
    registry_json.write_text("{\"skills\": []}", encoding="utf-8")
    citizens = tmp_path / "citizens.yaml"
    citizens.write_text("citizens:\n  - id: NONEXISTENT\n  - id: EXISTING\n", encoding="utf-8")
    bridges = tmp_path / "BRIDGES.yaml"
    bridges.write_text("repos:\n", encoding="utf-8")
    known = tmp_path / "known_repositories.yaml"
    known.write_text("P0_REPOS:\n- name: EXISTING\n", encoding="utf-8")

    prune = RegistryPrune(registry_yaml, registry_json, citizens, bridges, known)
    report = prune.prune(dry_run=True)
    assert report["dry_run"] is True
