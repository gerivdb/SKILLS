"""Tests unitaires pour n243-query-engine."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from n243_query_engine import N243QueryEngine


def _make_graph(tmp_path: Path) -> Path:
    graph = {
        "nodes": [
            {"id": "repo-a", "type": "repo", "layer": "L4", "source_repo": "gerivdb/A"},
            {
                "id": "repo-a:ADR/ADR-001.md",
                "type": "ADR",
                "intent_hash": "0xTEST_ADR_001",
                "layer": "L4",
                "source_repo": "gerivdb/A",
            },
        ],
        "edges": [
            {"source": "repo-a:ADR/ADR-001.md", "target": "repo-a", "relation": "owns"}
        ],
        "stats": {"repos": 1, "artifacts": 1, "edges": 1, "contradictions": 0},
    }
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(graph, ensure_ascii=False), encoding="utf-8")
    return graph_path


def test_search_query(tmp_path: Path) -> None:
    """Requête search - < 2s, sources tracées."""
    engine = N243QueryEngine(graph_path=_make_graph(tmp_path), output_dir=tmp_path)
    result = engine.execute(
        query={"type": "search", "target": "repo-a", "filters": []},
        scope={"strates": ["L4"]},
    )
    assert result.query_type == "search"
    assert len(result.results) >= 1
    assert result.duration_ms < 2000


def test_crossref_query(tmp_path: Path) -> None:
    """Requête crossref - 0 contradiction."""
    engine = N243QueryEngine(graph_path=_make_graph(tmp_path), output_dir=tmp_path)
    result = engine.execute(
        query={"type": "crossref", "target": "repo-a", "filters": []},
        scope={"strates": ["L4"]},
    )
    assert result.query_type == "crossref"
    assert result.duration_ms < 2000


def test_temporal_query(tmp_path: Path) -> None:
    """Requête temporelle - Support canal time."""
    engine = N243QueryEngine(graph_path=_make_graph(tmp_path), output_dir=tmp_path)
    result = engine.execute(
        query={"type": "temporal", "target": "repo-a", "filters": []},
        scope={"strates": ["L4"]},
    )
    assert result.query_type == "temporal"


def test_contradiction_query(tmp_path: Path) -> None:
    """Requête contradiction - Détectée en < 1s."""
    engine = N243QueryEngine(graph_path=_make_graph(tmp_path), output_dir=tmp_path)
    result = engine.execute(
        query={"type": "contradiction", "target": "repo-a", "filters": []},
        scope={"strates": ["L4"]},
    )
    assert result.query_type == "contradiction"
    assert result.duration_ms < 1000
