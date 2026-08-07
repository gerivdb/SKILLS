"""
n243_graph_builder — Build and maintain the sovereign cross-repo graph N243.

Pipeline:
  Load SOT (TOPOS, GOVERNANCE-HUB) -> Scan repos (cached) -> Extract metadata (batched) ->
  Build graph (nodes/edges) -> Write outputs (graph.yaml, embeddings.json, metadata.json)

Performance optimizations:
  - Cache scan results to avoid re-scanning unchanged repos
  - Batch rglob scans per repo to reduce syscalls
  - Parallel metadata extraction using ThreadPoolExecutor
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
TOOLS_ROOT = Path("D:/DO/WEB/TOOLS")
TOPOS = TOOLS_ROOT / "L1-INFRA/TOPOS"
GOVERNANCE_HUB = TOOLS_ROOT / "L0-CANON/GOVERNANCE-HUB"
N243_DATA = TOOLS_ROOT / "L4-TOOLS/N243/data"
CACHE_PATH = N243_DATA / ".cache" / "repo-scan-cache.json"


@dataclass
class RepoNode:
    id: str
    name: str
    full_name: str
    layer: str
    status: str
    local_path: Optional[str] = None
    role: str = ""
    bridges: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    source: str
    target: str
    edge_type: str
    bridge: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphResult:
    valid: bool
    nodes: List[RepoNode] = field(default_factory=list)
    edges: List[GraphEdge] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Path] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# SOT Loader
# ---------------------------------------------------------------------------
class SOTLoader:
    """Load Source of Truth from TOPOS and GOVERNANCE-HUB."""

    def __init__(self):
        self.topos_manifest: Dict[str, Any] = {}
        self.known_repos: Dict[str, Any] = {}
        self.ontology_terms: set = set()

    def load(self) -> None:
        self._load_topos()
        self._load_governance()
        self._load_ontology()

    def _load_topos(self) -> None:
        candidates = [
            TOPOS / "repo-manifest.yaml",
            TOPOS / "manifest.yaml",
            TOPOS / "repos.json",
        ]
        for path in candidates:
            if path.exists():
                text = path.read_text(encoding="utf-8", errors="replace")
                if path.suffix == ".json":
                    try:
                        self.topos_manifest = json.loads(text)
                    except Exception:
                        pass
                else:
                    try:
                        import yaml
                        self.topos_manifest = yaml.safe_load(text) or {}
                    except Exception:
                        pass
                return

    def _load_governance(self) -> None:
        candidates = [
            GOVERNANCE_HUB / "known_repositories.yaml",
            GOVERNANCE_HUB / "known_repositories.yml",
        ]
        for path in candidates:
            if path.exists():
                text = path.read_text(encoding="utf-8", errors="replace")
                try:
                    import yaml
                    self.known_repos = yaml.safe_load(text) or {}
                except Exception:
                    pass
                return

    def _load_ontology(self) -> None:
        ontology_path = TOOLS_ROOT / "ONTOLOGY/ONTOLOGY.yaml"
        if not ontology_path.exists():
            return
        text = ontology_path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped and ":" in stripped and not stripped.startswith("#"):
                term = stripped.split(":")[0].strip()
                if term:
                    self.ontology_terms.add(term)


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
class ScanCache:
    """Cache repo scan results to avoid re-scanning unchanged repos."""

    def __init__(self, cache_path: Path):
        self.cache_path = cache_path
        self.data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if self.cache_path.exists():
            try:
                self.data = json.loads(self.cache_path.read_text(encoding="utf-8"))
            except Exception:
                self.data = {}

    def _save(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self.data.get(key)

    def set(self, key: str, value: Dict[str, Any]) -> None:
        self.data[key] = value
        self._save()

    def invalidate(self, key: str) -> None:
        self.data.pop(key, None)
        self._save()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _collect_repo_dicts(known_repos: Dict[str, Any]) -> List[Dict[str, Any]]:
    repos = known_repos.get("repositories", [])
    if not repos:
        repos = known_repos.get("repos", [])
    if not repos:
        buckets: List[Any] = []
        for key, value in known_repos.items():
            if isinstance(key, str) and key.endswith("_REPOS") and isinstance(value, list):
                buckets.extend(value)
        repos = buckets
    return [r for r in repos if isinstance(r, dict)]


def _repo_cache_key(repo: Dict[str, Any]) -> str:
    full_name = repo.get("full_name", repo.get("name", ""))
    local_path = repo.get("local_path", "")
    raw = f"{full_name}|{local_path}"
    return hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()[:16]


def _is_repo_changed(repo_dir: Path, cache_entry: Optional[Dict[str, Any]]) -> bool:
    if cache_entry is None:
        return True
    try:
        st = repo_dir.stat()
        return abs(st.st_mtime - float(cache_entry.get("mtime", 0))) > 1.0 or abs(st.st_size - float(cache_entry.get("size", 0))) > 1.0
    except Exception:
        return True


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------
MARKERS = {
    "adr": ["ADR"],
    "prd": ["PRD"],
    "intent": ["INTENT"],
    "epic": ["EPIC"],
    "report": ["REPORT"],
    "roadmap": ["ROADMAP"],
    "spec": ["SPEC"],
}

_SKIP_DIRS = {".git", "node_modules", "target", "__pycache__", ".cargo", "vendor", "dist", "build", ".next", ".nuxt", "coverage", ".pytest_cache", "venv", ".venv", "env", ".env"}


def _detect_bridges(repo_dir: Path) -> List[str]:
    bridges: List[str] = []
    crosslinks = repo_dir / "CROSSLINKS"
    if crosslinks.is_dir():
        for f in crosslinks.iterdir():
            if f.is_file() and f.suffix in (".md", ".yaml", ".yml"):
                bridges.append(f"crosslink:{f.name}")
    bridges_file = repo_dir / "bridges.yaml"
    if bridges_file.exists():
        bridges.append("bridges:yaml")
    return bridges


def _scan_repo_metadata(repo_dir: Path) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {k: [] for k in MARKERS}
    # Build a flat set of marker basenames for fast matching
    marker_basenames: set = set()
    for markers in MARKERS.values():
        marker_basenames.update(markers)

    try:
        for entry in os.scandir(repo_dir):
            if entry.is_dir():
                if entry.name in _SKIP_DIRS:
                    continue
                _walk_dir(Path(entry.path), marker_basenames, metadata, repo_dir)
            elif entry.is_file():
                _check_file(Path(entry.path), repo_dir, marker_basenames, metadata)
    except Exception:
        pass
    return metadata


def _walk_dir(dir_path: Path, marker_basenames: set, metadata: Dict[str, Any], repo_root: Path) -> None:
    try:
        for entry in os.scandir(dir_path):
            if entry.is_dir():
                if entry.name in _SKIP_DIRS:
                    continue
                _walk_dir(Path(entry.path), marker_basenames, metadata, repo_root)
            elif entry.is_file():
                _check_file(Path(entry.path), repo_root, marker_basenames, metadata)
    except Exception:
        pass


def _check_file(file_path: Path, repo_root: Path, marker_basenames: set, metadata: Dict[str, Any]) -> None:
    if file_path.suffix not in (".md", ".yaml", ".yml"):
        return
    name = file_path.name
    for category, markers in MARKERS.items():
        for marker in markers:
            if marker in name:
                try:
                    rel = str(file_path.relative_to(repo_root))
                    if rel not in metadata[category]:
                        metadata[category].append(rel)
                except Exception:
                    pass
                return


def _scan_one_repo(repo: Dict[str, Any], cache: ScanCache) -> Optional[RepoNode]:
    full_name = repo.get("full_name", repo.get("name", ""))
    local_path = repo.get("local_path", "")
    if not full_name or not local_path:
        return None

    path = Path(local_path)
    if not path.exists():
        return None

    key = _repo_cache_key(repo)
    entry = cache.get(key)
    if not _is_repo_changed(path, entry):
        try:
            return RepoNode(
                id=f"repo:{full_name}",
                name=entry.get("name", full_name),
                full_name=full_name,
                layer=entry.get("layer", repo.get("layer", repo.get("stratum", "L?"))),
                status=str(entry.get("status", repo.get("status", "active"))).lower(),
                local_path=str(path),
                role=entry.get("role", repo.get("role", "")),
                bridges=entry.get("bridges", []),
                metadata=entry.get("metadata", {}),
            )
        except Exception:
            pass

    node = RepoNode(
        id=f"repo:{full_name}",
        name=repo.get("name", full_name),
        full_name=full_name,
        layer=repo.get("layer", repo.get("stratum", "L?")),
        status=str(repo.get("status", "active")).lower(),
        local_path=str(path),
        role=repo.get("role", ""),
        bridges=_detect_bridges(path),
        metadata={},
    )
    node.metadata = _scan_repo_metadata(path)

    try:
        st = path.stat()
        mtime = st.st_mtime
        size = st.st_size
    except Exception:
        mtime = time.time()
        size = 0

    cache.set(key, {
        "name": node.name,
        "layer": node.layer,
        "status": node.status,
        "role": node.role,
        "bridges": node.bridges,
        "metadata": node.metadata,
        "mtime": mtime,
        "size": size,
    })
    return node


def scan_repos(sot: SOTLoader, cache: ScanCache, max_workers: int = 8) -> List[RepoNode]:
    repo_dicts = _collect_repo_dicts(sot.known_repos)
    seen: set = set()
    nodes: List[RepoNode] = []

    unique: List[Dict[str, Any]] = []
    for repo in repo_dicts:
        full_name = repo.get("full_name", repo.get("name", ""))
        if full_name and full_name not in seen:
            seen.add(full_name)
            unique.append(repo)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_scan_one_repo, repo, cache): repo for repo in unique}
        for future in as_completed(futures):
            node = future.result()
            if node is not None:
                nodes.append(node)

    return nodes


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------
class GraphBuilder:
    """Build cross-repo graph from scanned nodes."""

    def __init__(self, nodes: List[RepoNode]):
        self.nodes = nodes
        self.node_map: Dict[str, RepoNode] = {n.id: n for n in nodes}

    def build(self) -> GraphResult:
        edges: List[GraphEdge] = []

        for node in self.nodes:
            for bridge in node.bridges:
                if bridge.startswith("crosslink:"):
                    target = self._find_crosslink_target(node, bridge)
                    if target:
                        edges.append(GraphEdge(
                            source=node.id,
                            target=target,
                            edge_type="crosslink",
                            bridge=bridge,
                        ))
                elif bridge == "bridges:yaml":
                    target = self._find_bridge_target(node)
                    if target:
                        edges.append(GraphEdge(
                            source=node.id,
                            target=target,
                            edge_type="bridge",
                            bridge="bridges.yaml",
                        ))

        layer_order = ["L0", "L1", "L1b", "L2", "L2b", "L3", "L4", "L5", "L6", "P2P"]
        layer_nodes: Dict[str, List[RepoNode]] = {l: [] for l in layer_order}
        for node in self.nodes:
            if node.layer in layer_nodes:
                layer_nodes[node.layer].append(node)

        for i, layer in enumerate(layer_order):
            if i == 0:
                continue
            prev_layer = layer_order[i - 1]
            if layer_nodes[layer] and layer_nodes[prev_layer]:
                edges.append(GraphEdge(
                    source=layer_nodes[prev_layer][0].id,
                    target=layer_nodes[layer][0].id,
                    edge_type="strata_hierarchy",
                    bridge=f"{prev_layer}->{layer}",
                ))

        stats = {
            "total_nodes": len(self.nodes),
            "total_edges": len(edges),
            "layers": sum(1 for nodes in layer_nodes.values() if nodes),
            "repos_with_bridges": sum(1 for n in self.nodes if n.bridges),
        }

        return GraphResult(
            valid=True,
            nodes=self.nodes,
            edges=edges,
            stats=stats,
        )

    @staticmethod
    def _find_crosslink_target(node: RepoNode, bridge: str) -> Optional[str]:
        return None

    @staticmethod
    def _find_bridge_target(node: RepoNode) -> Optional[str]:
        return None


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------
class GraphWriter:
    """Write graph outputs to N243/data/."""

    def __init__(self, result: GraphResult, target_path: Path):
        self.result = result
        self.target_path = target_path
        self.outputs: Dict[str, Path] = {}

    def write(self) -> Dict[str, Path]:
        self.outputs["graph"] = self._write_graph()
        self.outputs["embeddings"] = self._write_embeddings()
        self.outputs["metadata"] = self._write_metadata()
        return self.outputs

    def _write_graph(self) -> Path:
        out = N243_DATA / "graph.yaml"
        lines = [
            "graph:",
            f"  generated: {datetime.now().isoformat()}",
            f"  nodes: {len(self.result.nodes)}",
            f"  edges: {len(self.result.edges)}",
            "  repositories:",
        ]
        for node in self.result.nodes:
            lines.append(f"    - id: {node.id}")
            lines.append(f"      name: {node.name}")
            lines.append(f"      layer: {node.layer}")
            lines.append(f"      status: {node.status}")
            lines.append(f"      role: {node.role}")
            lines.append(f"      bridges: {len(node.bridges)}")
        lines.append("  edges:")
        for edge in self.result.edges:
            lines.append(f"    - source: {edge.source}")
            lines.append(f"      target: {edge.target}")
            lines.append(f"      type: {edge.edge_type}")
            lines.append(f"      bridge: {edge.bridge}")
        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def _write_embeddings(self) -> Path:
        out = N243_DATA / "embeddings.json"
        data = {
            "generated": datetime.now().isoformat(),
            "stats": self.result.stats,
            "nodes": [
                {
                    "id": n.id,
                    "name": n.name,
                    "layer": n.layer,
                    "status": n.status,
                    "bridges": n.bridges,
                }
                for n in self.result.nodes
            ],
        }
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return out

    def _write_metadata(self) -> Path:
        out = N243_DATA / "metadata.json"
        data = {
            "generated": datetime.now().isoformat(),
            "stats": self.result.stats,
            "nodes": [
                {
                    "id": n.id,
                    "name": n.name,
                    "layer": n.layer,
                    "status": n.status,
                    "role": n.role,
                    "local_path": n.local_path,
                    "metadata": n.metadata,
                }
                for n in self.result.nodes
            ],
            "edges": [
                {
                    "source": e.source,
                    "target": e.target,
                    "type": e.edge_type,
                    "bridge": e.bridge,
                }
                for e in self.result.edges
            ],
        }
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return out


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def build_graph(target_path: Optional[Path] = None, *, force: bool = False, max_workers: int = 8) -> GraphResult:
    t0 = time.perf_counter()
    sot = SOTLoader()
    sot.load()
    load_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    cache = ScanCache(CACHE_PATH)
    if force:
        cache.data = {}

    nodes = scan_repos(sot, cache, max_workers=max_workers)
    scan_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    builder = GraphBuilder(nodes)
    result = builder.build()
    build_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    if result.valid and result.nodes:
        writer = GraphWriter(result, target_path or N243_DATA)
        result.outputs = writer.write()
    write_time = time.perf_counter() - t0

    result.stats["perf"] = {
        "load_s": round(load_time, 3),
        "scan_s": round(scan_time, 3),
        "build_s": round(build_time, 3),
        "write_s": round(write_time, 3),
        "total_s": round(load_time + scan_time + build_time + write_time, 3),
    }
    return result


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="N243 Graph Builder")
    parser.add_argument("--target", type=str, help="Target path for outputs")
    parser.add_argument("--force", action="store_true", help="Force full scan, ignore cache")
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    parser.add_argument("--workers", type=int, default=8, help="Parallel workers")
    args = parser.parse_args()

    target = Path(args.target) if args.target else N243_DATA
    result = build_graph(target, force=args.force, max_workers=args.workers)

    if args.json:
        payload = {
            "valid": result.valid,
            "stats": result.stats,
            "issues": result.issues,
            "outputs": {k: str(v) for k, v in result.outputs.items()},
        }
        print(json.dumps(payload, ensure_ascii=False))
    else:
        status = "OK" if result.valid else "FAIL"
        perf = result.stats.get("perf", {})
        print(f"[N243] status={status} nodes={len(result.nodes)} edges={len(result.edges)}")
        print(f"[N243] perf: load={perf.get('load_s', '?')}s scan={perf.get('scan_s', '?')}s build={perf.get('build_s', '?')}s write={perf.get('write_s', '?')}s total={perf.get('total_s', '?')}s")
        for name, path in result.outputs.items():
            print(f"[N243] {name} -> {path}")
        if result.issues:
            print("[N243] issues:")
            for issue in result.issues:
                print(f"  - {issue}")

    return 0 if result.valid else 1


if __name__ == "__main__":
    sys.exit(main())
