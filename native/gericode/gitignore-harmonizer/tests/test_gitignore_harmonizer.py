"""Tests pour gitignore-harmonizer."""

from __future__ import annotations

from pathlib import Path
import pytest

from gitignore_harmonizer import GitignoreHarmonizer


def test_harmonize_gitignore(tmp_path):
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("out/\nnode_modules/\n", encoding="utf-8")
    harmonizer = GitignoreHarmonizer(repo_path=tmp_path)
    report = harmonizer.harmonize(dry_run=False)
    assert "out/" in report["broad_patterns_found"]
    assert "out/" in report["replacements_made"]


def test_dry_run_no_changes(tmp_path):
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("out/\n", encoding="utf-8")
    harmonizer = GitignoreHarmonizer(repo_path=tmp_path)
    report = harmonizer.harmonize(dry_run=True)
    assert report["dry_run"] is True
    assert gitignore.read_text(encoding="utf-8") == "out/\n"


def test_detect_broad_patterns(tmp_path):
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("out/\ninfrastructure/adapters/\n", encoding="utf-8")
    harmonizer = GitignoreHarmonizer(repo_path=tmp_path)
    found = harmonizer.detect_broad_patterns()
    assert "out/" in found
    assert "infrastructure/adapters/" in found
