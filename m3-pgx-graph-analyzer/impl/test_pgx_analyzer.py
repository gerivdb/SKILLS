# m3-pgx-graph-analyzer — tests unitaires de l'analyseur de graphe PGX
import json
import tempfile
import os

from pgx_analyzer import cmd_orphans, cmd_path, cmd_communities, cmd_metrics
from tql_executor import TQLExecutor, load_graph


SAMPLE_GRAPH = {
    "nodes": [
        {"id": "conv-1", "type": "conversation", "title": "A", "author": "alice", "tags": ["ia"], "createdAt": "2026-01-01T00:00:00Z"},
        {"id": "conv-2", "type": "conversation", "title": "B", "author": "bob", "tags": ["ia"], "createdAt": "2026-01-02T00:00:00Z"},
        {"id": "conv-3", "type": "conversation", "title": "C", "author": "alice", "tags": ["db"], "createdAt": "2026-01-03T00:00:00Z"},
        {"id": "conv-4", "type": "conversation", "title": "D", "author": "carol", "tags": [], "createdAt": "2026-01-04T00:00:00Z"},  # orphelin
    ],
    "edges": [
        {"source": "conv-1", "target": "conv-2", "type": "suite"},
        {"source": "conv-2", "target": "conv-3", "type": "reference"},
    ],
}


def test_orphans():
    executor = TQLExecutor(SAMPLE_GRAPH)
    orphans = executor._orphans()
    assert "conv-4" in orphans
    assert "conv-1" not in orphans
    print("OK test_orphans:", orphans)


def test_path():
    executor = TQLExecutor(SAMPLE_GRAPH)
    res = executor._path({"source": "conv-1", "target": "conv-3"})
    assert res["path"] == ["conv-1", "conv-2", "conv-3"]
    assert res["length"] == 2
    print("OK test_path:", res)


def test_path_nonexistent():
    executor = TQLExecutor(SAMPLE_GRAPH)
    res = executor._path({"source": "conv-1", "target": "conv-4"})
    assert res["length"] == -1
    assert "error" in res
    print("OK test_path_nonexistent:", res)


def test_communities():
    executor = TQLExecutor(SAMPLE_GRAPH)
    comms = executor._communities({})
    # conv-1,2,3 liés ; conv-4 isolé
    assert len(comms) == 2
    sizes = sorted([len(c) for c in comms])
    assert sizes == [1, 3]
    print("OK test_communities:", comms)


def test_metrics():
    executor = TQLExecutor(SAMPLE_GRAPH)
    m = executor._metrics()
    assert m["nodes"] == 4
    assert m["edges"] == 2
    assert m["orphans"] == 1
    assert m["diameter"] == 2
    print("OK test_metrics:", m)


def test_cli_orphans(tmp_path):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(SAMPLE_GRAPH, f)
        path = f.name
    try:
        rc = cmd_orphans(TQLExecutor(load_graph(path)))
        assert rc["count"] == 1
        assert rc["orphan_conversation_ids"] == ["conv-4"]
        print("OK test_cli_orphans")
    finally:
        os.unlink(path)


if __name__ == "__main__":
    test_orphans()
    test_path()
    test_path_nonexistent()
    test_communities()
    test_metrics()
    test_cli_orphans(tempfile.gettempdir())
    print("Tous les tests unitaires PGX passés.")
