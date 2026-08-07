"""Tests pour yaml-debug-forensic."""

from __future__ import annotations

import pytest

from yaml_debug_forensic import YAMLDebugForensic


def _write_yaml(path, content):
    path.write_text(content, encoding="utf-8")


def test_valid_yaml(tmp_path):
    target = tmp_path / "test.yaml"
    _write_yaml(target, "key: value\nlist:\n  - a\n  - b\n")
    forensic = YAMLDebugForensic(target)
    report = forensic.diagnose()
    assert report.is_clean is True
    assert report.parse_ok is True


def test_parse_error(tmp_path):
    target = tmp_path / "test.yaml"
    _write_yaml(target, "key: value\ninvalid: [unclosed\n")
    forensic = YAMLDebugForensic(target)
    report = forensic.diagnose()
    assert report.parse_ok is False
    assert report.parse_error != ""


def test_duplicate_keys(tmp_path):
    target = tmp_path / "test.yaml"
    _write_yaml(target, "key: value1\nkey: value2\n")
    forensic = YAMLDebugForensic(target)
    report = forensic.diagnose()
    assert len(report.duplicate_keys) >= 1
    assert not report.is_clean


def test_broken_quotes(tmp_path):
    target = tmp_path / "test.yaml"
    _write_yaml(target, 'key: "value\n')
    forensic = YAMLDebugForensic(target)
    report = forensic.diagnose()
    assert len(report.broken_quotes) >= 1
    assert not report.is_clean


def test_invalid_anchors(tmp_path):
    target = tmp_path / "test.yaml"
    _write_yaml(target, "defaults: &defaults\n  ci: full\nprod:\n  <<: *nonexistent\n")
    forensic = YAMLDebugForensic(target)
    report = forensic.diagnose()
    assert len(report.invalid_anchors) >= 1
    assert not report.is_clean
