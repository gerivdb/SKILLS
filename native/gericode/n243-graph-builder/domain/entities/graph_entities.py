"""
DDD Entities — n243-graph-builder
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class RepoVertex:
    full_name: str
    layer: str
    local_path: str
    verse_mapping: Optional[str] = None

    def key(self) -> str:
        return self.full_name


@dataclass
class GraphEdge:
    source: str
    target: str
    bridge_type: str
