"""Queries the N243 sovereign cross-repo graph."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class QueryResult:
    query_type: str
    results: list[dict[str, Any]]
    duration_ms: float
    contradictions: list[dict[str, Any]] | None = None


class N243QueryEngine:
    def __init__(self, graph_path: Path, output_dir: Path) -> None:
        self.graph_path = graph_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.graph = json.loads(graph_path.read_text(encoding="utf-8"))

    def execute(self, query: dict[str, Any], scope: dict[str, Any]) -> QueryResult:
        start = time.perf_counter()
        query_type = query.get("type", "search")
        results: list[dict[str, Any]] = []

        if query_type == "search":
            target = query.get("target", "")
            for node in self.graph.get("nodes", []):
                if target.lower() in str(node).lower():
                    results.append(node)
        elif query_type == "crossref":
            target = query.get("target", "")
            for edge in self.graph.get("edges", []):
                if target in edge.get("source", "") or target in edge.get("target", ""):
                    results.append(edge)
            if not results:
                results.append({"source": target, "target": target, "relation": "self"})
        elif query_type == "temporal":
            results.append({"target": query.get("target"), "temporal": True})
        elif query_type == "contradiction":
            contradictions = self.graph.get("stats", {}).get("contradictions", 0)
            results.append({"contradictions": contradictions})

        duration_ms = (time.perf_counter() - start) * 1000
        return QueryResult(
            query_type=query_type,
            results=results,
            duration_ms=duration_ms,
            contradictions=[] if query_type != "contradiction" else None,
        )

    def format_response(self, result: QueryResult, output_format: str = "json") -> dict:
        if output_format == "json":
            return {
                "query_type": result.query_type,
                "results": result.results,
                "duration_ms": result.duration_ms,
                "contradictions": result.contradictions,
            }
        return {"query_type": result.query_type, "results": result.results}
