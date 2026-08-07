"""
Hexagonal Ports — n243-graph-builder
"""

from typing import Protocol


class IGraphBuilderPort(Protocol):
    """Inbound port: graph construction."""

    def build(self, repositories: list[dict]) -> dict:
        ...


class IGraphRepositoryPort(Protocol):
    """Outbound port: graph persistence."""

    def save(self, graph: dict) -> None:
        ...

    def load(self) -> dict:
        ...
