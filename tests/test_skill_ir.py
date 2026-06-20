"""
test_skill_ir.py — Tests SKILL-IR v1.0 (S1→S3)

≥ 15 tests couvrant AC-1 a AC-4.

IntentHash: 0xTEST_SKILL_IR_20260620
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
import yaml

from skill_ir import SkillIR
from skill_ir.skill_ir import SkillValidationError

import skill_ir.skill_ir as _mod
IRNode = _mod.IRNode
DAG = _mod.DAG
TritLevel = _mod.TritLevel


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def skills_dir(tmp_path: Path) -> Path:
    """Cree 5 repertoires skills avec manifest.yaml."""
    skills = tmp_path / "skills"
    skills.mkdir()

    manifests = {
        "nexus-core": {
            "name": "nexus-core", "version": "1.3.0",
            "description": "Core skill", "deps": [],
            "triggers": ["nexus"], "strata": "L3",
            "intent_hash": "0x1001",
        },
        "repo-health": {
            "name": "repo-health", "version": "1.0.0",
            "description": "Health checker",
            "deps": ["nexus-core: >=1.0.0"],
            "triggers": ["health"], "strata": "L3",
            "intent_hash": "0x1002",
        },
        "repo-scanner": {
            "name": "repo-scanner", "version": "2.0.0",
            "description": "Scanner",
            "deps": ["nexus-core: >=1.0.0"],
            "triggers": ["scan"], "strata": "L3",
            "intent_hash": "0x1003",
        },
        "code-gate": {
            "name": "code-gate", "version": "1.1.0",
            "description": "Gate",
            "deps": ["repo-health: >=1.0.0", "repo-scanner: >=1.0.0"],
            "triggers": ["gate"], "strata": "L3",
            "intent_hash": "0x1004",
        },
        "standalone": {
            "name": "standalone", "version": "0.1.0",
            "description": "Standalone", "deps": [],
            "triggers": [], "strata": "L3",
            "intent_hash": "0x1005",
        },
    }

    for name, data in manifests.items():
        d = skills / name
        d.mkdir()
        (d / "manifest.yaml").write_text(
            yaml.safe_dump(data, default_flow_style=False), encoding="utf-8"
        )

    return skills


def _load_all(skills_dir: Path) -> list:
    nodes = []
    for f in sorted(skills_dir.glob("*/manifest.yaml")):
        nodes.append(SkillIR.load(f))
    return nodes


# ---------------------------------------------------------------------------
# S1: SKILL_LOAD
# ---------------------------------------------------------------------------

class TestSkillLoad:
    def test_load_valid(self, skills_dir: Path) -> None:
        node = SkillIR.load(skills_dir / "nexus-core" / "manifest.yaml")
        assert node.id == "nexus-core"
        assert node.node_type == "skill"
        assert node.meta["version"] == "1.3.0"

    def test_load_all_5(self, skills_dir: Path) -> None:
        nodes = _load_all(skills_dir)
        assert len(nodes) == 5

    def test_load_missing_path(self, tmp_path: Path) -> None:
        with pytest.raises(SkillValidationError):
            SkillIR.load(tmp_path / "nonexistent")

    def test_load_parses_deps(self, skills_dir: Path) -> None:
        node = SkillIR.load(skills_dir / "repo-health" / "manifest.yaml")
        deps = node.meta.get("deps", [])
        assert len(deps) == 1
        assert "nexus-core" in deps[0]

    def test_load_parses_triggers(self, skills_dir: Path) -> None:
        node = SkillIR.load(skills_dir / "nexus-core" / "manifest.yaml")
        assert "nexus" in node.meta.get("triggers", [])

    def test_load_generates_intent_hash(self, tmp_path: Path) -> None:
        d = tmp_path / "test-skill"
        d.mkdir()
        (d / "manifest.yaml").write_text("name: test-skill\n", encoding="utf-8")
        node = SkillIR.load(d / "manifest.yaml")
        assert node.meta.get("intent_hash", "").startswith("0x")


# ---------------------------------------------------------------------------
# S2: SKILL_LINK + SKILL_GATE + SKILL_DAG
# ---------------------------------------------------------------------------

class TestSkillLink:
    def test_link_requires(self) -> None:
        a = IRNode(id="a")
        b = IRNode(id="b")
        arc = SkillIR.link(a, b, "requires")
        assert arc.source == "a"
        assert arc.target == "b"
        assert arc.arc_type == "requires"

    def test_link_supersedes(self) -> None:
        a = IRNode(id="a")
        b = IRNode(id="b")
        arc = SkillIR.link(a, b, "supersedes")
        assert arc.arc_type == "supersedes"

    def test_link_invalid_defaults(self) -> None:
        a = IRNode(id="a")
        b = IRNode(id="b")
        arc = SkillIR.link(a, b, "invalid")
        assert arc.arc_type == "requires"


class TestSkillGate:
    def test_gate_t1(self) -> None:
        node = IRNode(id="x", meta={"version": "1.0.0", "deps": []})
        assert SkillIR.gate(node) == "T1"

    def test_gate_t2_bad_version(self) -> None:
        node = IRNode(id="x", meta={"version": "bad", "deps": []})
        assert SkillIR.gate(node) == "T2"

    def test_gate_t2_unresolved_dep(self, skills_dir: Path) -> None:
        nodes = _load_all(skills_dir)
        dag = SkillIR.build_dag(nodes)
        orphan = IRNode(id="orphan", meta={"version": "1.0.0", "deps": ["nonexistent"]})
        dag.add_node(orphan)
        assert SkillIR.gate(orphan, dag) == "T2"


class TestSkillDag:
    def test_build_dag(self, skills_dir: Path) -> None:
        nodes = _load_all(skills_dir)
        dag = SkillIR.build_dag(nodes)
        assert dag.node_count == 5

    def test_build_dag_arcs(self, skills_dir: Path) -> None:
        nodes = _load_all(skills_dir)
        dag = SkillIR.build_dag(nodes)
        assert dag.arc_count >= 4

    def test_build_dag_acyclic(self, skills_dir: Path) -> None:
        nodes = _load_all(skills_dir)
        dag = SkillIR.build_dag(nodes)
        for node in nodes:
            result = SkillIR.gate(node, dag)
            assert result == "T1"


# ---------------------------------------------------------------------------
# S3: SKILL_PROPAGATOR + SKILL_SCORE
# ---------------------------------------------------------------------------

class TestSkillPropagator:
    def test_propagate_nexus_core_change(self, skills_dir: Path) -> None:
        nodes = _load_all(skills_dir)
        dag = SkillIR.build_dag(nodes)
        impacted = SkillIR.propagate("nexus-core", dag)
        assert "repo-health" in impacted
        assert "repo-scanner" in impacted
        assert "code-gate" in impacted

    def test_propagate_leaf_no_impact(self, skills_dir: Path) -> None:
        nodes = _load_all(skills_dir)
        dag = SkillIR.build_dag(nodes)
        impacted = SkillIR.propagate("standalone", dag)
        assert impacted == []


class TestSkillScore:
    def test_score_empty(self) -> None:
        assert SkillIR.score(DAG()) == 0.0

    def test_score_no_deps(self) -> None:
        node = IRNode(id="standalone", meta={"deps": []})
        dag = DAG()
        dag.add_node(node)
        assert SkillIR.score(dag) == 1.0

    def test_score_range(self, skills_dir: Path) -> None:
        nodes = _load_all(skills_dir)
        dag = SkillIR.build_dag(nodes)
        score = SkillIR.score(dag)
        assert 0.0 <= score <= 1.0

    def test_score_with_unresolved(self, skills_dir: Path) -> None:
        nodes = _load_all(skills_dir)
        dag = SkillIR.build_dag(nodes)
        orphan = IRNode(id="orphan", meta={"deps": ["missing: >=1.0.0"]})
        dag.add_node(orphan)
        score = SkillIR.score(dag)
        assert score < 1.0


# ---------------------------------------------------------------------------
# Import test (AC-1)
# ---------------------------------------------------------------------------

class TestImport:
    def test_import_skill_ir(self) -> None:
        from skill_ir import SkillIR
        assert SkillIR is not None

    def test_version(self) -> None:
        from skill_ir import __version__
        assert __version__ == "1.0.0"
