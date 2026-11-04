# m3-gericode3-dashboard — tests unitaires du tableau de bord
import json
import tempfile
import os

from dashboard import (
    load_graph, conversation_nodes, graph_edges, find_orphans,
    compute_metrics, vault_health, mermaid_graph, dot_graph,
    filter_nodes, build_dashboard,
)


SAMPLE_GRAPH = {
    "nodes": [
        {"id": "conv-1", "type": "conversation", "title": "Réunion IA", "author": "alice",
         "tags": ["ia", "reunion"], "workspaceId": "vault-A",
         "createdAt": "2026-11-01T00:00:00Z", "updatedAt": "2026-11-04T00:00:00Z"},
        {"id": "conv-2", "type": "conversation", "title": "Base de données", "author": "bob",
         "tags": ["db"], "workspaceId": "vault-A",
         "createdAt": "2026-11-02T00:00:00Z", "updatedAt": "2026-11-04T00:00:00Z"},
        {"id": "conv-3", "type": "conversation", "title": "Orphelin", "author": "carol",
         "tags": [], "workspaceId": "vault-B",
         "createdAt": "2026-11-03T00:00:00Z", "updatedAt": "2026-11-03T00:00:00Z"},
    ],
    "edges": [
        {"source": "conv-1", "target": "conv-2", "type": "suite"},
    ],
}


def test_find_orphans():
    nodes = conversation_nodes(SAMPLE_GRAPH)
    edges = graph_edges(SAMPLE_GRAPH)
    orphans = find_orphans(nodes, edges)
    assert orphans == ["conv-3"], orphans
    print("OK test_find_orphans:", orphans)


def test_compute_metrics():
    nodes = conversation_nodes(SAMPLE_GRAPH)
    edges = graph_edges(SAMPLE_GRAPH)
    m = compute_metrics(nodes, edges)
    assert m["total_conversations"] == 3
    assert m["total_edges"] == 1
    assert m["by_author"]["alice"] == 1
    assert m["by_tag"]["ia"] == 1
    print("OK test_compute_metrics:", m)


def test_vault_health():
    nodes = conversation_nodes(SAMPLE_GRAPH)
    h = vault_health(nodes)
    assert "vault-A" in h
    assert "vault-B" in h
    assert h["vault-A"]["status"] == "active"
    assert h["vault-A"]["conversations"] == 2
    print("OK test_vault_health:", h)


def test_mermaid_graph():
    nodes = conversation_nodes(SAMPLE_GRAPH)
    edges = graph_edges(SAMPLE_GRAPH)
    orphans = find_orphans(nodes, edges)
    m = mermaid_graph(nodes, edges, orphans)
    assert "graph TD" in m
    assert "conv-1" in m
    assert "conv-2" in m
    print("OK test_mermaid_graph (len", len(m), ")")


def test_dot_graph():
    nodes = conversation_nodes(SAMPLE_GRAPH)
    edges = graph_edges(SAMPLE_GRAPH)
    orphans = find_orphans(nodes, edges)
    d = dot_graph(nodes, edges, orphans)
    assert "digraph CASIS" in d
    assert "conv-1" in d
    print("OK test_dot_graph (len", len(d), ")")


def test_filter_nodes():
    nodes = conversation_nodes(SAMPLE_GRAPH)
    f = filter_nodes(nodes, tags=["ia"])
    assert len(f) == 1
    assert f[0]["id"] == "conv-1"
    f2 = filter_nodes(nodes, author="bob")
    assert len(f2) == 1
    assert f2[0]["id"] == "conv-2"
    print("OK test_filter_nodes")


def test_build_dashboard(tmp_path):
    report = build_dashboard(SAMPLE_GRAPH)
    assert "# Tableau de bord OMNI-INTER-NOTEBOOK-LM" in report
    assert "```mermaid" in report
    assert "Conversations orphelines" in report
    assert "Santé des voûtes" in report
    print("OK test_build_dashboard")


def test_cli_output(tmp_path):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(SAMPLE_GRAPH, f)
        path = f.name
    try:
        from dashboard import main
        rc = main(["--graph", path, "--output", "-"])
        assert rc == 0
        print("OK test_cli_output")
    finally:
        os.unlink(path)


if __name__ == "__main__":
    test_find_orphans()
    test_compute_metrics()
    test_vault_health()
    test_mermaid_graph()
    test_dot_graph()
    test_filter_nodes()
    test_build_dashboard(tempfile.gettempdir())
    test_cli_output(tempfile.gettempdir())
    print("Tous les tests unitaires dashboard passés.")
