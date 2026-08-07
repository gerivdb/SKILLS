"""
Hexagonal Adapters — n243-graph-builder
"""

from typing import Protocol


class GraphBuilderService:
    """Application service orchestrating graph construction."""

    def __init__(self) -> None:
        self._vertices: list[dict] = []
        self._edges: list[dict] = []

    def add_vertex(self, repo: dict) -> None:
        self._vertices.append(repo)

    def add_edge(self, source: str, target: str, bridge_type: str) -> None:
        self._edges.append({"source": source, "target": target, "type": bridge_type})

    def build(self) -> dict:
        return {"vertices": self._vertices, "edges": self._edges}


class CLIGraphBuilderAdapter:
    """CLI adapter for n243-graph-builder."""

    def execute(self, command: str, payload: dict) -> dict:
        if command == "build":
            service = GraphBuilderService()
            for repo in payload.get("repositories", []):
                service.add_vertex(repo)
            return service.build()
        raise ValueError(f"Unknown command: {command}")
