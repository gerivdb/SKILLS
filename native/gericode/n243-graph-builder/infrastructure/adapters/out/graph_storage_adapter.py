"""
Hexagonal Infrastructure Adapters — n243-graph-builder
"""

import json
from pathlib import Path
from typing import Protocol


class IGraphStorageAdapter(Protocol):
    """Outbound adapter: graph persistence."""

    def save_graph(self, path: str, graph: dict) -> None:
        ...

    def load_graph(self, path: str) -> dict:
        ...


class LocalGraphStorageAdapter:
    """Local filesystem implementation for graph storage."""

    def save_graph(self, path: str, graph: dict) -> None:
        Path(path).write_text(json.dumps(graph, indent=2), encoding="utf-8")

    def load_graph(self, path: str) -> dict:
        return json.loads(Path(path).read_text(encoding="utf-8"))
