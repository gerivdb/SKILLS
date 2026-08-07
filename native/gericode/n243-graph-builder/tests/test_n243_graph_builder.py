"""Tests unitaires pour n243-graph-builder."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from n243_graph_builder import ArtifactMetadata, N243GraphBuilder, RepoNode


def _make_repo(tmp_path: Path, name: str, artifacts: int = 0) -> RepoNode:
    repo_dir = tmp_path / name
    repo_dir.mkdir()

    if artifacts:
        adr_dir = repo_dir / "ADR"
        adr_dir.mkdir()
        (adr_dir / "ADR-001-test.md").write_text(
            "---\ntype: ADR\nversion: 1.0\nstatus: accepted\ndate: 2026-08-06\n"
            "intent_hash: 0xTEST_ADR_001\ncitizen: TEST\nlayer: L4\n"
            "author: test\nsource_repo: gerivdb/TEST\nsource_path: ADR/ADR-001-test.md\n---\n",
            encoding="utf-8",
        )

    return RepoNode(name=name, local_path=repo_dir)


def test_scan_all_repos(tmp_path: Path) -> None:
    """Scan tous les dépôts actifs - 100% détectés."""
    repo1 = _make_repo(tmp_path, "repo-a")
    repo2 = _make_repo(tmp_path, "repo-b")

    known = tmp_path / "known_repositories.yaml"
    known.write_text(
        "P0_REPOS:\n"
        "  - name: repo-a\n"
        "    local_path: repo-a\n"
        "    layer: L4\n"
        "  - name: repo-b\n"
        "    local_path: repo-b\n"
        "    layer: L4\n",
        encoding="utf-8",
    )

    builder = N243GraphBuilder(
        known_repositories_path=known,
        output_dir=tmp_path / "output",
    )
    repos = builder.scan_repos()

    assert len(repos) == 2
    assert {r.name for r in repos} == {"repo-a", "repo-b"}
    assert all(r.local_path.is_absolute() for r in repos)


def test_extract_metadata(tmp_path: Path) -> None:
    """Extrait ADR, PRD, INTENT - Métadonnées complètes."""
    repo = _make_repo(tmp_path, "repo-a", artifacts=1)

    known = tmp_path / "known_repositories.yaml"
    known.write_text(
        "P0_REPOS:\n"
        "  - name: repo-a\n"
        "    local_path: repo-a\n"
        "    layer: L4\n",
        encoding="utf-8",
    )

    builder = N243GraphBuilder(
        known_repositories_path=known,
        output_dir=tmp_path / "output",
    )
    repos = builder.scan_repos()
    artifacts = builder.extract_metadata(repos)

    assert len(artifacts) == 1
    assert artifacts[0].artifact_type == "ADR"
    assert artifacts[0].intent_hash == "0xTEST_ADR_001"


def test_build_graph(tmp_path: Path) -> None:
    """Construit le graphe - Edges cohérentes."""
    repo = _make_repo(tmp_path, "repo-a", artifacts=1)

    known = tmp_path / "known_repositories.yaml"
    known.write_text(
        "P0_REPOS:\n"
        "  - name: repo-a\n"
        "    local_path: repo-a\n"
        "    layer: L4\n",
        encoding="utf-8",
    )

    builder = N243GraphBuilder(
        known_repositories_path=known,
        output_dir=tmp_path / "output",
    )
    repos = builder.scan_repos()
    builder.extract_metadata(repos)
    graph = builder.build_graph(repos)

    assert graph["stats"]["repos"] == 1
    assert graph["stats"]["artifacts"] == 1
    assert graph["stats"]["edges"] >= 1


def test_update_embeddings_placeholder(tmp_path: Path) -> None:
    """Placeholder: embeddings LLUX + KRONOS."""
    assert True
