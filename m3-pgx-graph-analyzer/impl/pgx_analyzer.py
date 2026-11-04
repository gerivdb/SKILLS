"""
m3-pgx-graph-analyzer — Analyse de graphe PGX (Parallel Graph Analytics).

Point d'entrée unifié pour les analyses topologiques du graphe de
conversations NotebookLM (M3-Tree / CASIS).

Analyses supportées :
- conversations orphelines (aucun edge entrant/sortant)
- chemin critique (plus court chemin entre deux conversations)
- détection de communautés (composantes connexes)
- métriques topologiques (nœuds, arêtes, diamètre, densité)

Dépendances : tql_executor (même package).
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict

from tql_executor import TQLExecutor, load_graph  # noqa: E402


def cmd_orphans(executor: TQLExecutor) -> Dict:
    orphans = executor._orphans()
    return {
        "analysis": "orphans",
        "count": len(orphans),
        "orphan_conversation_ids": orphans,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def cmd_path(executor: TQLExecutor, source: str, target: str) -> Dict:
    return {
        "analysis": "critical_path",
        "source": source,
        "target": target,
        **executor._path({"source": source, "target": target}),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def cmd_communities(executor: TQLExecutor) -> Dict:
    communities = executor._communities({})
    return {
        "analysis": "communities",
        "count": len(communities),
        "communities": communities,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def cmd_metrics(executor: TQLExecutor) -> Dict:
    return {
        "analysis": "topology_metrics",
        **executor._metrics(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Analyseur de graphe PGX M3-Tree")
    parser.add_argument("--graph", required=True, help="Chemin JSON du graphe M3-Tree")
    parser.add_argument("--analysis", required=True,
                        choices=["orphans", "path", "communities", "metrics", "all"])
    parser.add_argument("--source", help="ID node source (pour path)")
    parser.add_argument("--target", help="ID node cible (pour path)")
    parser.add_argument("--output", default="-", help="Fichier de sortie (- = stdout)")
    args = parser.parse_args(argv)

    graph = load_graph(args.graph)
    executor = TQLExecutor(graph)

    results = []
    if args.analysis in ("orphans", "all"):
        results.append(cmd_orphans(executor))
    if args.analysis in ("path", "all"):
        if not args.source or not args.target:
            print("ERREUR: --source et --target requis pour l'analyse path", file=sys.stderr)
            return 2
        results.append(cmd_path(executor, args.source, args.target))
    if args.analysis in ("communities", "all"):
        results.append(cmd_communities(executor))
    if args.analysis in ("metrics", "all"):
        results.append(cmd_metrics(executor))

    out = json.dumps(results, ensure_ascii=False, indent=2)
    if args.output == "-":
        print(out)
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
