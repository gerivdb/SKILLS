"""Tests pour ecosystem-probe."""

from __future__ import annotations

import json

from pathlib import Path
import pytest

from ecosystem_probe import EcosystemProbe


def test_scan_skills(tmp_path):
    skills_dir = tmp_path / ".kilo" / "skills" / "my-skill"
    skills_dir.mkdir(parents=True)
    (skills_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n", encoding="utf-8")

    probe = EcosystemProbe(tmp_path)
    index = probe.scan_all()

    assert len(index.skills) == 1
    assert index.skills[0].name == "my-skill"


def test_scan_workflows(tmp_path):
    workflows_dir = tmp_path / ".kilo" / "workflows"
    workflows_dir.mkdir(parents=True)
    (workflows_dir / "my_workflow.py").write_text("# workflow\n", encoding="utf-8")

    probe = EcosystemProbe(tmp_path)
    index = probe.scan_all()

    assert len(index.workflows) == 1
    assert index.workflows[0].name == "my_workflow"


def test_scan_citizens(tmp_path):
    citizens_file = tmp_path / "act-protocol" / "citizens.yaml"
    citizens_file.parent.mkdir(parents=True)
    citizens_file.write_text("citizens: []\n", encoding="utf-8")

    probe = EcosystemProbe(tmp_path)
    index = probe.scan_all()

    assert len(index.citizens) == 1


def test_scan_designs(tmp_path):
    designs_dir = tmp_path / "unified-design" / "designs"
    designs_dir.mkdir(parents=True)
    (designs_dir / "my-design.yaml").write_text("---\nname: my-design\n---\n", encoding="utf-8")

    probe = EcosystemProbe(tmp_path)
    index = probe.scan_all()

    assert len(index.designs) == 1
    assert index.designs[0].name == "my-design"


def test_save_index(tmp_path):
    probe = EcosystemProbe(tmp_path)
    probe.scan_all()
    output = tmp_path / "ecosystem-index.json"
    probe.save(output)

    assert output.exists()
    data = json.loads(output.read_text(encoding="utf-8"))
    assert "skills" in data
    assert "workflows" in data
    assert "citizens" in data
    assert "designs" in data
