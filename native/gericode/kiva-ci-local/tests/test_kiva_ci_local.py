"""Tests pour kiva-ci-local."""

from __future__ import annotations

from pathlib import Path
import pytest

from kiva_ci_local import generate_ci_yaml


def test_generate_ci_yaml(tmp_path):
    ci_path = generate_ci_yaml(tmp_path)
    assert ci_path.exists()
    assert ci_path.name == "ci.yaml"


def test_ci_yaml_has_stages(tmp_path):
    generate_ci_yaml(tmp_path)
    content = (tmp_path / ".kiva" / "ci.yaml").read_text(encoding="utf-8")
    assert "lint:" in content
    assert "test:" in content
    assert "typecheck:" in content
    assert "validate:" in content


def test_ci_yaml_has_hooks(tmp_path):
    generate_ci_yaml(tmp_path)
    content = (tmp_path / ".kiva" / "ci.yaml").read_text(encoding="utf-8")
    assert "pre_commit:" in content
    assert "post_merge:" in content
