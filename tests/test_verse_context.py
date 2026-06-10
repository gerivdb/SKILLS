#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour VERSEContext
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from verse_context import VERSEContext
from datetime import datetime


def test_to_dict_contains_verse_id():
    ctx = VERSEContext(verse_id="WorkflowVerse", verse_name="Workflow Verse")
    d = ctx.to_dict()
    assert d["__verse_id"] == "WorkflowVerse"


def test_to_dict_merges_memory():
    ctx = VERSEContext(verse_id="test", verse_name="Test", memory={"repo": "DevTools"})
    d = ctx.to_dict()
    assert d["repo"] == "DevTools"


def test_to_dict_merges_params():
    ctx = VERSEContext(verse_id="test", verse_name="Test", params={"dry_run": True})
    d = ctx.to_dict()
    assert d["dry_run"] is True


def test_fluent_builder():
    ctx = (
        VERSEContext(verse_id="test", verse_name="Test")
        .with_memory("target", "CTULU")
        .with_param("verbose", True)
        .requires_skill("jurisdiction-checker")
        .requires_tool("repo-inspector")
        .requires_primitive("repo_tree_parser")
    )
    assert ctx.memory["target"] == "CTULU"
    assert ctx.params["verbose"] is True
    assert "jurisdiction-checker" in ctx.skills
    assert "repo-inspector" in ctx.tools
    assert "repo_tree_parser" in ctx.primitives


def test_from_verse_detector():
    detected = {
        "id": "bon_sens_python_verse",
        "name": "Bon Sens Python",
        "domain": "devtools",
        "memory": {"style": "pragmatic"},
        "params": {},
        "skills": ["code-reviewer"],
        "tools": [],
        "primitives": [],
    }
    ctx = VERSEContext.from_verse_detector(detected)
    assert ctx.verse_id == "bon_sens_python_verse"
    assert ctx.domain == "devtools"
    assert ctx.memory["style"] == "pragmatic"


if __name__ == "__main__":
    test_to_dict_contains_verse_id()
    test_to_dict_merges_memory()
    test_to_dict_merges_params()
    test_fluent_builder()
    test_from_verse_detector()
    print("✅ All VERSEContext tests passed")
