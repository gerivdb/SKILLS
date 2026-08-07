"""Tests pour bridge-auditor."""

from __future__ import annotations

from pathlib import Path
import pytest

from bridge_auditor import BridgeAuditor


def test_audit_no_orphans(tmp_path):
    bridges = tmp_path / "BRIDGES.yaml"
    bridges.write_text(
        "repos:\n"
        "  TEST:\n"
        "    full_name: gerivdb/TEST\n"
        "    local_path: D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\TEST\n"
        "    layer: L4_TOOLS\n"
        "    bridges:\n"
        "    - ONTOLOGY\n",
        encoding="utf-8",
    )
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
    auditor = BridgeAuditor(bridges, known)
    report = auditor.audit()
    assert len(report["orphaned_bridges"]) == 0


def test_audit_no_missing(tmp_path):
    bridges = tmp_path / "BRIDGES.yaml"
    bridges.write_text(
        "repos:\n"
        "  TEST:\n"
        "    full_name: gerivdb/TEST\n"
        "    local_path: D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\TEST\n"
        "    layer: L4_TOOLS\n"
        "    bridges:\n"
        "    - ONTOLOGY\n",
        encoding="utf-8",
    )
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
    auditor = BridgeAuditor(bridges, known)
    report = auditor.audit()
    assert len(report["missing_bridges"]) == 0


def test_audit_no_cycles(tmp_path):
    bridges = tmp_path / "BRIDGES.yaml"
    bridges.write_text(
        "repos:\n"
        "  TEST:\n"
        "    full_name: gerivdb/TEST\n"
        "    local_path: D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\TEST\n"
        "    layer: L4_TOOLS\n"
        "    bridges:\n"
        "    - ONTOLOGY\n",
        encoding="utf-8",
    )
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
    auditor = BridgeAuditor(bridges, known)
    report = auditor.audit()
    assert len(report["cycles"]) == 0


def test_audit_with_orphans(tmp_path):
    bridges = tmp_path / "BRIDGES.yaml"
    bridges.write_text(
        "repos:\n"
        "  ORPHAN:\n"
        "    full_name: gerivdb/ORPHAN\n"
        "    local_path: D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\ORPHAN\n"
        "    layer: L4_TOOLS\n"
        "    bridges:\n"
        "    - ONTOLOGY\n",
        encoding="utf-8",
    )
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
    auditor = BridgeAuditor(bridges, known)
    report = auditor.audit()
    assert "ORPHAN" in report["orphaned_bridges"]
