"""
m3-pgx-graph-analyzer — Exécuteur de requêtes TQL.

TQL (Ternary Query Language) sur le graphe de conversations M3-Tree.
Filtre par type de lien, date, auteur, tags.

Sorties : liste de conversations, chemins, communautés.
"""

import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class TQLExecutor:
    def __init__(self, graph: Dict[str, Any]):
        """
        graph: {"nodes": [...], "edges": [...]}
        nodes: {id, type, title, createdAt, author, tags, workspaceId, ...}
        edges: {source, target, type, ...}
        """
        self.nodes = {n["id"]: n for n in graph.get("nodes", []) if n.get("type") == "conversation"}
        self.edges = graph.get("edges", [])
        # Index adjacence
        self.adj: Dict[str, List[Dict[str, Any]]] = {}
        for e in self.edges:
            self.adj.setdefault(e["source"], []).append(e)
            self.adj.setdefault(e["target"], []).append(e)

    def run(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Exécute une requête TQL.
        query: {"op": "filter|path|communities|orphans|metrics", ...}
        Retourne une liste de résultats (dictionnaires).
        """
        op = query.get("op")
        if op == "filter":
            return self._filter(query)
        if op == "path":
            return [self._path(query)]
        if op == "communities":
            return [{"communities": self._communities(query)}]
        if op == "orphans":
            return [{"orphans": self._orphans()}]
        if op == "metrics":
            return [{"metrics": self._metrics()}]
        raise ValueError(f"Opération TQL inconnue: {op}")

    # --- filtres ---------------------------------------------------------
    def _filter(self, q: Dict[str, Any]) -> List[Dict[str, Any]]:
        results = []
        for node in self.nodes.values():
            if self._match(node, q):
                results.append(node)
        return results

    def _match(self, node: Dict[str, Any], q: Dict[str, Any]) -> bool:
        if "author" in q and node.get("author") != q["author"]:
            return False
        if "tags" in q:
            wanted = set(q["tags"]) if isinstance(q["tags"], list) else {q["tags"]}
            node_tags = set(node.get("tags", []))
            if not wanted & node_tags:
                return False
        if "created_after" in q:
            try:
                if node.get("createdAt", "") < q["created_after"]:
                    return False
            except TypeError:
                return False
        if "link_type" in q:
            # Ne garder que les nodes ayant au moins un edge de ce type
            wanted_type = q["link_type"]
            has_link = any(e.get("type") == wanted_type for e in self.edges
                           if e.get("source") == node["id"] or e.get("target") == node["id"])
            if not has_link:
                return False
        return True

    # --- chemin critique -------------------------------------------------
    def _path(self, q: Dict[str, Any]) -> Dict[str, Any]:
        source = q["source"]
        target = q["target"]
        if source not in self.nodes or target not in self.nodes:
            return {"source": source, "target": target, "path": [], "length": -1,
                    "error": "node introuvable"}
        # BFS sur les edges non dirigés (traversée CASIS)
        from collections import deque
        visited = {source}
        queue = deque([(source, [source])])
        while queue:
            current, path = queue.popleft()
            if current == target:
                return {"source": source, "target": target, "path": path,
                        "length": len(path) - 1}
            for e in self.adj.get(current, []):
                neighbor = e["target"] if e["source"] == current else e["source"]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return {"source": source, "target": target, "path": [], "length": -1,
                "error": "aucun chemin"}

    # --- communautés -----------------------------------------------------
    def _communities(self, q: Dict[str, Any]) -> List[List[str]]:
        """
        Détection simple de communautés par composantes connexes non dirigées.
        Seuil de similarité ignoré (graphe CASIS explicite).
        """
        visited = set()
        communities = []
        for node_id in self.nodes:
            if node_id in visited:
                continue
            # BFS pour trouver la composante
            comp = []
            queue = [node_id]
            visited.add(node_id)
            while queue:
                current = queue.pop(0)
                comp.append(current)
                for e in self.adj.get(current, []):
                    neighbor = e["target"] if e["source"] == current else e["source"]
                    if neighbor not in visited and neighbor in self.nodes:
                        visited.add(neighbor)
                        queue.append(neighbor)
            if comp:
                communities.append(sorted(comp))
        return communities

    # --- orphelins -------------------------------------------------------
    def _orphans(self) -> List[str]:
        linked = set()
        for e in self.edges:
            linked.add(e.get("source"))
            linked.add(e.get("target"))
        return sorted([nid for nid in self.nodes if nid not in linked])

    # --- métriques -------------------------------------------------------
    def _metrics(self) -> Dict[str, Any]:
        n_nodes = len(self.nodes)
        n_edges = len(self.edges)
        # diamètre = plus long chemin le plus court (BFS depuis chaque node)
        diameter = 0
        for start in self.nodes:
            dist = self._bfs_distances(start)
            if dist:
                diameter = max(diameter, max(dist.values()))
        density = (2 * n_edges / (n_nodes * (n_nodes - 1))) if n_nodes > 1 else 0.0
        return {
            "nodes": n_nodes,
            "edges": n_edges,
            "diameter": diameter,
            "density": round(density, 4),
            "orphans": len(self._orphans()),
        }

    def _bfs_distances(self, start: str) -> Dict[str, int]:
        from collections import deque
        dist = {start: 0}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for e in self.adj.get(current, []):
                neighbor = e["target"] if e["source"] == current else e["source"]
                if neighbor not in dist and neighbor in self.nodes:
                    dist[neighbor] = dist[current] + 1
                    queue.append(neighbor)
        return dist


def load_graph(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main(argv=None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Exécuteur TQL pour graphe M3-Tree")
    parser.add_argument("--graph", required=True, help="Chemin JSON du graphe M3-Tree")
    parser.add_argument("--op", required=True, choices=["filter", "path", "communities", "orphans", "metrics"])
    parser.add_argument("--source", help="ID node source (pour path)")
    parser.add_argument("--target", help="ID node cible (pour path)")
    parser.add_argument("--author", help="Filtre auteur")
    parser.add_argument("--tags", help="Tags séparés par des virgules")
    parser.add_argument("--created-after", help="Filtre date création (ISO-8601)")
    parser.add_argument("--link-type", help="Filtre type de lien")
    parser.add_argument("--output", default="-", help="Fichier de sortie (- = stdout)")
    args = parser.parse_args(argv)

    graph = load_graph(args.graph)
    executor = TQLExecutor(graph)

    query: Dict[str, Any] = {"op": args.op}
    if args.source:
        query["source"] = args.source
    if args.target:
        query["target"] = args.target
    if args.author:
        query["author"] = args.author
    if args.tags:
        query["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
    if args.created_after:
        query["created_after"] = args.created_after
    if args.link_type:
        query["link_type"] = args.link_type

    try:
        result = executor.run(query)
    except ValueError as exc:
        print(f"ERREUR TQL: {exc}", file=sys.stderr)
        return 2

    payload = {
        "op": args.op,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "result_count": len(result),
        "results": result,
    }
    out = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output == "-":
        print(out)
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
