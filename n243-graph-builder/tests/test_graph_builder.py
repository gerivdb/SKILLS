"""
Tests for n243-graph-builder.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from n243_graph_builder.core import run_pipeline


N243_DATA = Path("D:/DO/WEB/TOOLS/L4-TOOLS/N243/data")


def test_pipeline_runs():
    result = run_pipeline(N243_DATA)
    assert result.valid is True
    assert len(result.nodes) > 0
    assert "graph" in result.outputs


def test_outputs_exist():
    result = run_pipeline(N243_DATA)
    for name, path in result.outputs.items():
        assert path.exists(), f"{name} missing at {path}"


def test_graph_yaml_format():
    result = run_pipeline(N243_DATA)
    graph_path = result.outputs.get("graph")
    assert graph_path is not None
    content = graph_path.read_text(encoding="utf-8")
    assert "graph:" in content
    assert "repositories:" in content


def test_embeddings_json_schema():
    result = run_pipeline(N243_DATA)
    emb_path = result.outputs.get("embeddings")
    assert emb_path is not None
    data = json.loads(emb_path.read_text(encoding="utf-8"))
    assert "generated" in data
    assert "nodes" in data
    assert len(data["nodes"]) > 0


def test_metadata_json_schema():
    result = run_pipeline(N243_DATA)
    meta_path = result.outputs.get("metadata")
    assert meta_path is not None
    data = json.loads(meta_path.read_text(encoding="utf-8"))
    assert "generated" in data
    assert "nodes" in data
    assert "edges" in data
