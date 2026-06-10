#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitaires pour CTULUResolver
(mode offline — mock du registry sans HTTP)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ctulu_resolver import CTULUResolver, ToolEntry

# Registry YAML minimal en mémoire pour les tests
_MOCK_REGISTRY = """
registry_version: "1.0"
tools:
  - id: dag-navigator
    status: SPIKE
    type: frontend
    path: src/frontend/dag-navigator/
    description: Compound DAG Navigator
    consumers:
      - BIRDY
      - SKILLS
  - id: cluster-importer
    status: DRAFT
    type: backend
    path: src/backend/cluster-importer/
    description: Parse clusters JSON
    consumers:
      - IRIS
    primitives:
      - repo_tree_parser
  - id: legacy-tool
    status: DEPRECATED
    type: backend
    path: src/legacy/
    description: Old tool
    consumers: []
"""


def make_resolver() -> CTULUResolver:
    resolver = CTULUResolver()
    resolver._parse_registry(_MOCK_REGISTRY)
    resolver._loaded = True
    return resolver


def test_resolve_known_tool():
    r = make_resolver()
    tool = r.resolve("dag-navigator")
    assert tool is not None
    assert tool.id == "dag-navigator"
    assert tool.type == "frontend"


def test_resolve_unknown_returns_none():
    r = make_resolver()
    assert r.resolve("nonexistent-tool") is None


def test_resolve_many():
    r = make_resolver()
    results = r.resolve_many(["dag-navigator", "cluster-importer", "missing"])
    assert results["dag-navigator"] is not None
    assert results["cluster-importer"] is not None
    assert results["missing"] is None


def test_find_by_consumer():
    r = make_resolver()
    tools = r.find_by_consumer("SKILLS")
    assert any(t.id == "dag-navigator" for t in tools)


def test_find_by_type():
    r = make_resolver()
    backends = r.find_by_type("backend")
    assert all(t.type == "backend" for t in backends)


def test_is_available_deprecated():
    r = make_resolver()
    tool = r.resolve("legacy-tool")
    assert tool is not None
    assert not tool.is_available


def test_ctulu_url():
    r = make_resolver()
    tool = r.resolve("dag-navigator")
    assert "gerivdb/CTULU" in tool.ctulu_url
    assert tool.path in tool.ctulu_url


def test_primitives_field():
    r = make_resolver()
    tool = r.resolve("cluster-importer")
    assert "repo_tree_parser" in tool.primitives


if __name__ == "__main__":
    test_resolve_known_tool()
    test_resolve_unknown_returns_none()
    test_resolve_many()
    test_find_by_consumer()
    test_find_by_type()
    test_is_available_deprecated()
    test_ctulu_url()
    test_primitives_field()
    print("✅ All CTULUResolver tests passed")
