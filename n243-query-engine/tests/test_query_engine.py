"""
Tests for n243-query-engine.
"""

from __future__ import annotations

import json

import pytest

from n243_query_engine import QueryRequest, QueryResult, execute


def test_search_returns_results():
    result = execute(QueryRequest(query_type="search", target=""))
    assert result.ok is True
    assert isinstance(result.items, list)


def test_topology_returns_layers():
    result = execute(QueryRequest(query_type="topology"))
    assert result.ok is True
    assert "total_nodes" in result.meta
    assert "layers" in result.meta


def test_crossref_returns_results():
    result = execute(QueryRequest(query_type="crossref", target=""))
    assert result.ok is True
    assert isinstance(result.items, list)


def test_unknown_query_type_errors():
    result = execute(QueryRequest(query_type="unknown"))
    assert result.ok is False
    assert "error" in result.error.lower() or result.error != ""


def test_temporal_returns_pending():
    result = execute(QueryRequest(query_type="temporal"))
    assert result.ok is True
    assert result.meta.get("supported") is False


def test_contradiction_returns_pending():
    result = execute(QueryRequest(query_type="contradiction"))
    assert result.ok is True
    assert result.meta.get("supported") is False


def test_search_target_filter():
    result = execute(QueryRequest(query_type="search", target="L0"))
    assert result.ok is True
    assert result.meta.get("matches") is not None
