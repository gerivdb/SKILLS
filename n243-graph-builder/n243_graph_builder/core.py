"""
n243_graph_builder.core — core graph building logic.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from . import (
    SOTLoader,
    ScanCache,
    GraphResult,
    GraphWriter,
    GraphBuilder,
    scan_repos,
    build_graph,
)


def run_pipeline(target: Optional[Path] = None, force: bool = False, max_workers: int = 8) -> Dict[str, Any]:
    return build_graph(target, force=force, max_workers=max_workers)
