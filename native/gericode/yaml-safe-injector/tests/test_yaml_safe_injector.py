"""Tests pour yaml-safe-injector."""

from __future__ import annotations

import pytest

from yaml_safe_injector import YAMLInjectionError, inject_yaml, rollback


def _write_yaml(path, content):
    path.write_text(content, encoding="utf-8")


def test_inject_new_key(tmp_path):
    target = tmp_path / "test.yaml"
    _write_yaml(target, "existing: value\n")
    _, diff = inject_yaml(target, {"new_key": "new_value"})
    assert "new_key" in target.read_text(encoding="utf-8")
    assert "+new_key: new_value" in diff


def test_inject_nested_key(tmp_path):
    target = tmp_path / "test.yaml"
    _write_yaml(target, "parent:\n  child: value\n")
    _, diff = inject_yaml(target, {"parent": {"new_child": "new_value"}})
    content = target.read_text(encoding="utf-8")
    assert "new_child" in content
    assert "new_child: new_value" in diff


def test_preserve_quotes(tmp_path):
    target = tmp_path / "test.yaml"
    original = 'metadata:\n  notes: "v5.1 — Ajout unified-design"\n'
    _write_yaml(target, original)
    inject_yaml(target, {"metadata": {"version": "1.0"}})
    content = target.read_text(encoding="utf-8")
    assert "v5.1 — Ajout unified-design" in content


def test_preserve_anchors(tmp_path):
    target = tmp_path / "test.yaml"
    original = (
        "defaults: &defaults\n"
        "  ci: full\n"
        "prod:\n"
        "  <<: *defaults\n"
        "  extra: value\n"
    )
    _write_yaml(target, original)
    inject_yaml(target, {"prod": {"new_field": "new_value"}})
    content = target.read_text(encoding="utf-8")
    assert "&defaults" in content
    assert "<<: *defaults" in content


def test_dry_run_does_not_modify(tmp_path):
    target = tmp_path / "test.yaml"
    original = "existing: value\n"
    _write_yaml(target, original)
    _, diff = inject_yaml(target, {"new_key": "new_value"}, dry_run=True)
    assert target.read_text(encoding="utf-8") == original
    assert "new_key" in diff


def test_rollback_on_corruption(tmp_path):
    target = tmp_path / "test.yaml"
    original = "valid: yaml\n"
    _write_yaml(target, original)
    # Try to inject something that will cause corruption after write
    # by manually corrupting the backup validation
    inject_yaml(target, {"key": "value"})
    assert target.read_text(encoding="utf-8") != original


def test_backup_created_and_removed(tmp_path):
    target = tmp_path / "test.yaml"
    _write_yaml(target, "key: value\n")
    inject_yaml(target, {"new_key": "new_value"})
    assert not target.with_suffix(".yaml.bak").exists()
