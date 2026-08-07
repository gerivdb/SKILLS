"""Builds the N243 sovereign cross-repo graph."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, List

import yaml

from verse_mapping import verse_for

logger = logging.getLogger(__name__)


@dataclass
class RepoNode:
    name: str
    local_path: Path
    layer: str = "L4"
    verse_mapping: str = "none"


@dataclass
class ArtifactMetadata:
    repo: RepoNode
    artifact_type: str
    path: Path
    intent_hash: str = ""
    frontmatter: dict = field(default_factory=dict)


class ScanCache:
    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> str | None:
        path = self.cache_dir / f"{key}.json"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None

    def set(self, key: str, value: str) -> None:
        path = self.cache_dir / f"{key}.json"
        path.write_text(value, encoding="utf-8")


def _extract_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    match = re.search(r"---\s*(.*?)\s*---", text, re.DOTALL)
    if not match:
        return {}
    frontmatter = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            frontmatter[key.strip()] = value.strip()
    return frontmatter


_LAYER_TO_STRATE = {
    "L0-CANON": "L0-CANON",
    "L0-INFRASTRUCTURE": "L0-CANON",
    "L1_CAUSALITY": "L1-INFRA",
    "L1b": "L1-INFRA",
    "L2_COMPOSITION": "L2-PLATFORM",
    "L2_PLATFORM": "L2-PLATFORM",
    "L3_EMERGENCE": "L3-CITIZENS",
    "L4_TOOLS": "L4-TOOLS",
    "L5_ARCHIVE": "L5-ARCHIVE",
}


def _infer_local_path(name: str, layer: str) -> Path:
    strate = _LAYER_TO_STRATE.get(layer, "L4-TOOLS")
    return Path(f"D:\\DO\\WEB\\TOOLS\\{strate}\\{name}")


class N243GraphBuilder:
    def __init__(
        self,
        known_repositories_path: Path,
        output_dir: Path,
        cache: ScanCache | None = None,
    ) -> None:
        self.known_repositories_path = known_repositories_path
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache = cache or ScanCache(output_dir / "cache")

    def scan_repos(self) -> List[RepoNode]:
        content = self.known_repositories_path.read_text(encoding="utf-8")
        base_dir = self.known_repositories_path.parent

        try:
            data = yaml.safe_load(content) or {}
        except Exception:
            data = {}

        if not isinstance(data, dict):
            return []

        repo_items: List[dict[str, Any]] = []
        for key, value in data.items():
            if isinstance(key, str) and key.endswith("_REPOS") and isinstance(value, list):
                repo_items.extend(value)

        repos: List[RepoNode] = []
        for item in repo_items:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name") or "").strip()
            if not name:
                continue

            raw_path = item.get("local_path")
            layer = str(item.get("layer") or "L4")
            yaml_verse = item.get("verse_mapping")
            if yaml_verse is None:
                verse_mapping = verse_for(name)
                source = "local"
            else:
                verse_mapping = str(yaml_verse)
                source = "yaml"

            logger.debug("verse_mapping for %s: %s (source=%s)", name, verse_mapping, source)

            if raw_path is None:
                local_path = _infer_local_path(name, layer)
            else:
                local_path = Path(raw_path)
                if not local_path.is_absolute():
                    local_path = (base_dir / local_path).resolve()

            repos.append(
                RepoNode(
                    name=name,
                    local_path=local_path,
                    layer=layer,
                    verse_mapping=verse_mapping,
                )
            )

        return repos

    def extract_metadata(self, repos: Iterable[RepoNode]) -> List[ArtifactMetadata]:
        artifacts: List[ArtifactMetadata] = []
        for repo in repos:
            adr_dir = repo.local_path / "ADR"
            if adr_dir.exists():
                for path in adr_dir.glob("*.md"):
                    text = path.read_text(encoding="utf-8")
                    frontmatter = _extract_frontmatter(text)
                    artifacts.append(
                        ArtifactMetadata(
                            repo=repo,
                            artifact_type="ADR",
                            path=path,
                            intent_hash=frontmatter.get("intent_hash", ""),
                            frontmatter=frontmatter,
                        )
                    )
        return artifacts

    def build_graph(self, repos: Iterable[RepoNode]) -> dict:
        repo_list = list(repos)
        artifacts = self.extract_metadata(repo_list)
        edges = 0
        for artifact in artifacts:
            edges += 1
        return {
            "stats": {
                "repos": len(repo_list),
                "artifacts": len(artifacts),
                "edges": edges,
            },
            "repos": [repo.name for repo in repo_list],
            "edges": [],
        }

    def run(self, limit: int = 0) -> dict:
        repos = self.scan_repos()
        if limit > 0:
            repos = repos[:limit]
        artifacts = self.extract_metadata(repos)
        graph = self.build_graph(repos)
        graph_path = self.output_dir / "graph.json"
        graph_path.write_text(
            json.dumps(graph, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        wal_entry = {
            "intent_hash": "0xWAL_N243_INGESTION",
            "timestamp": "",
            "repos_scanned": graph["stats"]["repos"],
            "artifacts_indexed": graph["stats"]["artifacts"],
        }
        return {
            "graph": graph,
            "wal_entry": wal_entry,
        }
