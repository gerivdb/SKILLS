"""
n243_query_engine — N243 Query Engine.
Executes TQL-style queries over the sovereign cross-repo graph.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


N243_DATA = Path("D:/DO/WEB/TOOLS/L4-TOOLS/N243/data")


@dataclass
class QueryRequest:
    query_type: str
    target: str = ""
    scope: Dict[str, Any] = field(default_factory=dict)
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryResult:
    ok: bool
    query_type: str
    items: List[Dict[str, Any]] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)
    error: str = ""


def _load_graph() -> Dict[str, Any]:
    graph_path = N243_DATA / "graph.yaml"
    if not graph_path.exists():
        return {}
    return {"graph": graph_path.read_text(encoding="utf-8", errors="replace")}


def _load_metadata() -> Dict[str, Any]:
    meta_path = N243_DATA / "metadata.json"
    if not meta_path.exists():
        return {"nodes": [], "edges": []}
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return {"nodes": [], "edges": []}


def search(req: QueryRequest) -> QueryResult:
    meta = _load_metadata()
    nodes = meta.get("nodes", [])
    target = req.target.lower()
    matched = []
    for node in nodes:
        hay = json.dumps(node, ensure_ascii=False).lower()
        if target in hay:
            matched.append(node)
    return QueryResult(
        ok=True,
        query_type="search",
        items=matched,
        meta={"total": len(nodes), "matches": len(matched)},
    )


def crossref(req: QueryRequest) -> QueryResult:
    meta = _load_metadata()
    edges = meta.get("edges", [])
    target = req.target.lower()
    matched = []
    for edge in edges:
        hay = json.dumps(edge, ensure_ascii=False).lower()
        if target in hay:
            matched.append(edge)
    return QueryResult(
        ok=True,
        query_type="crossref",
        items=matched,
        meta={"total": len(edges), "matches": len(matched)},
    )


def topology(req: QueryRequest) -> QueryResult:
    meta = _load_metadata()
    nodes = meta.get("nodes", [])
    edges = meta.get("edges", [])
    layers: Dict[str, int] = {}
    for node in nodes:
        layer = node.get("layer", "UNKNOWN")
        layers[layer] = layers.get(layer, 0) + 1
    return QueryResult(
        ok=True,
        query_type="topology",
        items=[
            {"nodes": nodes, "edges": edges, "layer_counts": layers},
        ],
        meta={"total_nodes": len(nodes), "total_edges": len(edges), "layers": len(layers)},
    )


def temporal(req: QueryRequest) -> QueryResult:
    return QueryResult(
        ok=True,
        query_type="temporal",
        items=[],
        meta={"supported": False, "reason": "KRONOS integration pending"},
    )


def contradiction(req: QueryRequest) -> QueryResult:
    return QueryResult(
        ok=True,
        query_type="contradiction",
        items=[],
        meta={"supported": False, "reason": "MOX validation integration pending"},
    )


QUERY_HANDLERS = {
    "search": search,
    "crossref": crossref,
    "topology": topology,
    "temporal": temporal,
    "contradiction": contradiction,
}


def execute(req: QueryRequest) -> QueryResult:
    handler = QUERY_HANDLERS.get(req.query_type)
    if handler is None:
        return QueryResult(ok=False, query_type=req.query_type, error=f"unknown query_type={req.query_type}")
    return handler(req)


def run_query(query_type: str, target: str = "", scope: Optional[Dict[str, Any]] = None) -> QueryResult:
    req = QueryRequest(query_type=query_type, target=target, scope=scope or {})
    return execute(req)
