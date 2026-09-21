#!/usr/bin/env python3
"""codebase-intelligence.py — Orchestrator combining ecosystem-brain + codebase-memory-mcp.

Usage:
    python codebase-intelligence.py --query "N243 sovereign cross-repo"
    python codebase-intelligence.py --query "MCP git configuration"
    python codebase-intelligence.py --struct "python"         # structural only
    python codebase-intelligence.py --semantic "N243 graph"  # semantic only
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path.cwd()
INDEX_FILE = REPO_ROOT / "ecosystem-index.json"
INDEX_SCRIPT = REPO_ROOT / ".kilo" / "scripts" / "index-ecosystem.py"


def run_index_query(query: str) -> List[Dict[str, Any]]:
    """Run ecosystem-brain query and return structural results."""
    try:
        result = subprocess.run(
            ["python", str(INDEX_SCRIPT), "--query", query],
            capture_output=True,
            text=True,
            check=True,
        )
        items = []
        for line in result.stdout.strip().splitlines():
            line = line.strip()
            if line.startswith("[") and "] " in line:
                # Format: [type] id: name
                bracket_end = line.index("] ")
                item_type = line[1:bracket_end]
                rest = line[bracket_end + 2:]
                if ": " in rest:
                    item_id, item_name = rest.split(": ", 1)
                    items.append({
                        "type": item_type,
                        "id": item_id.strip(),
                        "name": item_name.strip(),
                        "source": "ecosystem-brain",
                    })
        return items
    except Exception as e:
        print(f"[WARN] ecosystem-brain query failed: {e}")
        return []


def run_semantic_query(query: str) -> List[Dict[str, Any]]:
    """Placeholder for codebase-memory-mcp semantic query."""
    return [
        {
            "type": "semantic-hint",
            "id": "codebase-memory-mcp",
            "name": "Semantic search available via codebase-memory-mcp",
            "source": "codebase-memory-mcp",
            "query": query,
            "note": "Connect via MCP client for full semantic results",
        }
    ]


def combine_results(query: str, structural: List[Dict[str, Any]], semantic: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Combine structural and semantic results into unified response."""
    return {
        "query": query,
        "structural_count": len(structural),
        "semantic_count": len(semantic),
        "structural": structural,
        "semantic": semantic,
        "combined": structural + semantic,
    }


def display_results(results: Dict[str, Any]):
    """Display combined results in readable format."""
    print(f"\n[CODEBASE-INTEL] Query: {results['query']}")
    print(f"[CODEBASE-INTEL] Structural: {results['structural_count']} | Semantic: {results['semantic_count']}")
    print()
    
    if results["structural"]:
        print("=== STRUCTURAL (ecosystem-brain) ===")
        for item in results["structural"]:
            print(f"  [{item['type']}] {item['id']}: {item['name']}")
        print()
    
    if results["semantic"]:
        print("=== SEMANTIC (codebase-memory-mcp) ===")
        for item in results["semantic"]:
            print(f"  [{item['type']}] {item['id']}: {item['name']}")
            if "note" in item:
                print(f"    Note: {item['note']}")
        print()


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Codebase Intelligence — ecosystem-brain + codebase-memory-mcp")
    parser.add_argument("--query", type=str, help="Combined structural + semantic query")
    parser.add_argument("--struct", type=str, help="Structural query only (ecosystem-brain)")
    parser.add_argument("--semantic", type=str, help="Semantic query only (codebase-memory-mcp)")
    args = parser.parse_args()
    
    if args.query:
        query = args.query
        structural = run_index_query(query)
        semantic = run_semantic_query(query)
        results = combine_results(query, structural, semantic)
        display_results(results)
        return 0
    
    if args.struct:
        structural = run_index_query(args.struct)
        print(f"\n[STRUCTURAL] Found {len(structural)} results:")
        for item in structural:
            print(f"  [{item['type']}] {item['id']}: {item['name']}")
        return 0
    
    if args.semantic:
        semantic = run_semantic_query(args.semantic)
        print(f"\n[SEMANTIC] Found {len(semantic)} results:")
        for item in semantic:
            print(f"  [{item['type']}] {item['id']}: {item['name']}")
        return 0
    
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
