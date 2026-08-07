"""
n243_query_engine.core — core query execution pipeline.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import QueryRequest, QueryResult, execute


def run_query_pipeline(query_type: str, target: str = "", scope: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    req = QueryRequest(query_type=query_type, target=target, scope=scope or {})
    result = execute(req)
    payload = {
        "ok": result.ok,
        "query_type": result.query_type,
        "items": result.items,
        "meta": result.meta,
        "error": result.error,
    }
    return payload
