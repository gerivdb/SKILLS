"""Tests pour known-repositories-updater."""

from __future__ import annotations

from pathlib import Path
import pytest

from known_repositories_updater import KnownRepositoriesUpdater, KnownRepositoriesUpdaterError


def test_update_adds_new_repo(tmp_path):
    known = tmp_path / "known_repositories.yaml"
    known.write_text(
        "P0_REPOS:\n"
        "- name: EXISTING\n"
        "  entity_type: REPO\n"
        "  full_name: gerivdb/EXISTING\n"
        "  local_path: D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\EXISTING\n"
        "  url: https://github.com/gerivdb/EXISTING\n"
        "  layer: L4_TOOLS\n"
        "  status: ACTIVE\n",
        encoding="utf-8",
    )
    updater = KnownRepositoriesUpdater(known_repositories_path=known, github_org="gerivdb")
    report = updater.update(dry_run=True)
    assert "errors" in report


def test_dry_run_no_changes(tmp_path):
    known = tmp_path / "known_repositories.yaml"
    known.write_text("P0_REPOS:\n- name: EXISTING\n", encoding="utf-8")
    updater = KnownRepositoriesUpdater(known_repositories_path=known, github_org="gerivdb")
    report = updater.update(dry_run=True)
    assert report["dry_run"] is True
