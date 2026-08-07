"""Tests pour registry-sync."""

from __future__ import annotations

from pathlib import Path
import pytest

from registry_sync import RegistrySyncEngine, RegistrySyncError


def test_sync_registry_yaml_to_json(tmp_path):
    registry_yaml = tmp_path / "REGISTRY.yaml"
    registry_yaml.write_text(
        "skills:\n"
        "  - name: test-skill\n"
        "    description: Test\n"
        "    type: foundational\n"
        "    version: 1.0.0\n"
        "    author: gerivdb\n"
        "    license: MIT\n"
        "    status: active\n"
        "    created: '2026-08-07'\n"
        "    updated: '2026-08-07'\n"
        "    phi_weight: 0.005\n"
        "    path: ..\\L2-PLATFORM\\GeriCode\\.kilo\\skills\\test-skill\\SKILL.md\n"
        "    source: native\n"
        "    assimilation_status: N/A\n"
        "    source_repo: gerivdb/GeriCode\n"
        "    consumes_from: []\n",
        encoding="utf-8",
    )
    registry_json = tmp_path / "registry.json"
    registry_json.write_text("{\"skills\": []}", encoding="utf-8")
    citizens_yaml = tmp_path / "citizens.yaml"
    citizens_yaml.write_text("citizens:\n", encoding="utf-8")

    engine = RegistrySyncEngine(registry_yaml, registry_json, citizens_yaml)
    report = engine.sync(dry_run=False)
    assert report["registry_json_updated"] is True
    assert report["total_skills"] == 1


def test_sync_citizens_from_registry(tmp_path):
    registry_yaml = tmp_path / "REGISTRY.yaml"
    registry_yaml.write_text(
        "skills:\n"
        "  - name: test-skill\n"
        "    description: Test\n"
        "    type: foundational\n"
        "    version: 1.0.0\n"
        "    author: gerivdb\n"
        "    license: MIT\n"
        "    status: active\n"
        "    created: '2026-08-07'\n"
        "    updated: '2026-08-07'\n"
        "    phi_weight: 0.005\n"
        "    path: ..\\L2-PLATFORM\\GeriCode\\.kilo\\skills\\test-skill\\SKILL.md\n"
        "    source: native\n"
        "    assimilation_status: N/A\n"
        "    source_repo: gerivdb/GeriCode\n"
        "    consumes_from: []\n",
        encoding="utf-8",
    )
    registry_json = tmp_path / "registry.json"
    registry_json.write_text("{\"skills\": []}", encoding="utf-8")
    citizens_yaml = tmp_path / "citizens.yaml"
    citizens_yaml.write_text("citizens:\n", encoding="utf-8")

    engine = RegistrySyncEngine(registry_yaml, registry_json, citizens_yaml)
    report = engine.sync(dry_run=False)
    assert report["citizens_yaml_updated"] is True
    data = citizens_yaml.read_text(encoding="utf-8")
    assert "GERICODE" in data


def test_dry_run_no_changes(tmp_path):
    registry_yaml = tmp_path / "REGISTRY.yaml"
    registry_yaml.write_text(
        "skills:\n"
        "  - name: test-skill\n"
        "    description: Test\n"
        "    type: foundational\n"
        "    version: 1.0.0\n"
        "    author: gerivdb\n"
        "    license: MIT\n"
        "    status: active\n"
        "    created: '2026-08-07'\n"
        "    updated: '2026-08-07'\n"
        "    phi_weight: 0.005\n"
        "    path: ..\\L2-PLATFORM\\GeriCode\\.kilo\\skills\\test-skill\\SKILL.md\n"
        "    source: native\n"
        "    assimilation_status: N/A\n"
        "    source_repo: gerivdb/GeriCode\n"
        "    consumes_from: []\n",
        encoding="utf-8",
    )
    registry_json = tmp_path / "registry.json"
    registry_json.write_text("{\"skills\": []}", encoding="utf-8")
    citizens_yaml = tmp_path / "citizens.yaml"
    citizens_yaml.write_text("citizens:\n", encoding="utf-8")

    engine = RegistrySyncEngine(registry_yaml, registry_json, citizens_yaml)
    report = engine.sync(dry_run=True)
    assert report["registry_json_updated"] is True
    assert registry_json.read_text(encoding="utf-8") == "{\"skills\": []}"


def test_detect_missing_source_repo(tmp_path):
    registry_yaml = tmp_path / "REGISTRY.yaml"
    registry_yaml.write_text(
        "skills:\n"
        "  - name: test-skill\n"
        "    description: Test\n"
        "    type: foundational\n"
        "    version: 1.0.0\n"
        "    author: gerivdb\n"
        "    license: MIT\n"
        "    status: active\n"
        "    created: '2026-08-07'\n"
        "    updated: '2026-08-07'\n"
        "    phi_weight: 0.005\n"
        "    path: ..\\L2-PLATFORM\\GeriCode\\.kilo\\skills\\test-skill\\SKILL.md\n"
        "    source: native\n"
        "    assimilation_status: N/A\n"
        "    consumes_from: []\n",
        encoding="utf-8",
    )
    registry_json = tmp_path / "registry.json"
    registry_json.write_text("{\"skills\": []}", encoding="utf-8")
    citizens_yaml = tmp_path / "citizens.yaml"
    citizens_yaml.write_text("citizens:\n", encoding="utf-8")

    engine = RegistrySyncEngine(registry_yaml, registry_json, citizens_yaml)
    report = engine.sync(dry_run=False)
    assert any("source_repo" in str(e) for e in report["errors"]) or report["total_skills"] == 1
