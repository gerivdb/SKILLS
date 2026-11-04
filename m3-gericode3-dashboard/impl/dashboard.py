"""
m3-gericode3-dashboard — Générateur de tableau de bord OMNI-INTER-NOTEBOOK-LM.

Produit un tableau de bord centralisé (Markdown + Mermaid) pour GERICODE 3 :
- graphe CASIS (Mermaid/DOT, coloré par type de lien et statut)
- liste des conversations orphelines
- métriques BigQuery (total, par semaine, auteur, tag, voûte)
- santé des ~60 voûtes NotebookLM (active / inactive / erreur)
- filtrage et recherche par mots-clés, tags, date, workspace

Dépendances : aucun package externe (pure stdlib).
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta


# ---------------------------------------------------------------------------
# Chargement du graphe M3-Tree
# ---------------------------------------------------------------------------

def load_graph(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def conversation_nodes(graph: dict) -> list:
    return [n for n in graph.get("nodes", []) if n.get("type") == "conversation"]


def graph_edges(graph: dict) -> list:
    return graph.get("edges", [])


# ---------------------------------------------------------------------------
# Détection des orphelins
# ---------------------------------------------------------------------------

def find_orphans(nodes: list, edges: list) -> list:
    linked = set()
    for e in edges:
        linked.add(e.get("source"))
        linked.add(e.get("target"))
    return sorted([n["id"] for n in nodes if n["id"] not in linked])


# ---------------------------------------------------------------------------
# Métriques BigQuery (agrégations)
# ---------------------------------------------------------------------------

def compute_metrics(nodes: list, edges: list) -> dict:
    total = len(nodes)
    by_author = Counter(n.get("author", "inconnu") for n in nodes)
    by_tag = Counter()
    for n in nodes:
        for t in n.get("tags", []):
            by_tag[t] += 1
    # par semaine (selon createdAt)
    by_week = Counter()
    for n in nodes:
        created = n.get("createdAt")
        if created:
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                week = dt.strftime("%Y-W%U")
                by_week[week] += 1
            except ValueError:
                by_week["date_inconnue"] += 1
        else:
            by_week["date_inconnue"] += 1
    return {
        "total_conversations": total,
        "by_author": dict(by_author),
        "by_tag": dict(by_tag),
        "by_week": dict(sorted(by_week.items())),
        "total_edges": len(edges),
    }


# ---------------------------------------------------------------------------
# Santé des voûtes (~60)
# ---------------------------------------------------------------------------

def vault_health(nodes: list, days_inactive_warning: int = 30) -> dict:
    """
    Évalue la santé de chaque voûte (workspaceId).
    Statuts : active, inactive, erreur.
    """
    now = datetime.now(timezone.utc)
    vaults = defaultdict(list)
    for n in nodes:
        vaults[n.get("workspaceId", "sans_voûte")].append(n)

    report = {}
    for vault_id, convs in vaults.items():
        last_activity = None
        status = "active"
        for n in convs:
            for field in ("updatedAt", "createdAt"):
                val = n.get(field)
                if val:
                    try:
                        dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
                        if last_activity is None or dt > last_activity:
                            last_activity = dt
                    except ValueError:
                        pass
        if last_activity is None:
            status = "erreur"
        elif (now - last_activity) > timedelta(days=days_inactive_warning):
            status = "inactive"
        report[vault_id] = {
            "conversations": len(convs),
            "status": status,
            "last_activity": last_activity.isoformat() if last_activity else None,
        }
    return report


# ---------------------------------------------------------------------------
# Graphe CASIS -> Mermaid / DOT
# ---------------------------------------------------------------------------

LINK_COLOR = {
    "reference": "#1f77b4",   # bleu
    "suite": "#2ca02c",       # vert
    "contradiction": "#d62728",  # rouge
    "approfondissement": "#9467bd",  # violet
    "template": "#ff7f0e",    # orange
}


def mermaid_graph(nodes: list, edges: list, orphans: list) -> str:
    lines = ["graph TD", "    classDef orphan fill:#f9f,stroke:#333,stroke-width:2px;",
             "    classDef active fill:#e1f7e1,stroke:#333;",
             "    classDef default fill:#ffffff,stroke:#333;", ""]
    node_set = {n["id"] for n in nodes}
    # nœuds
    for n in nodes:
        nid = n["id"]
        label = n.get("title", nid).replace('"', '\\"')
        cls = "orphan" if nid in orphans else "active"
        lines.append(f'    {nid}("{label}")::: {cls}'.replace("::: ", ":::"))
    lines.append("")
    # arêtes
    for e in edges:
        src = e.get("source")
        tgt = e.get("target")
        etype = e.get("type", "reference")
        color = LINK_COLOR.get(etype, "#666")
        if src in node_set and tgt in node_set:
            lines.append(f'    {src} -->|{etype}| {tgt}')
    return "\n".join(lines)


def dot_graph(nodes: list, edges: list, orphans: list) -> str:
    lines = ["digraph CASIS {", '    rankdir=LR;', '    node [shape=box, style=filled];', ""]
    for n in nodes:
        nid = n["id"]
        label = n.get("title", nid).replace('"', '\\"')
        fill = "#f9f" if nid in orphans else "#e1f7e1"
        lines.append(f'    {nid} [label="{label}", fillcolor={fill}];')
    lines.append("")
    for e in edges:
        src = e.get("source")
        tgt = e.get("target")
        etype = e.get("type", "reference")
        if src in {n["id"] for n in nodes} and tgt in {n["id"] for n in nodes}:
            lines.append(f'    {src} -> {tgt} [label="{etype}"];')
    lines.append("}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Filtrage / recherche
# ---------------------------------------------------------------------------

def filter_nodes(nodes: list, keywords: list = None, tags: list = None,
                 author: str = None, created_after: str = None) -> list:
    result = []
    for n in nodes:
        ok = True
        text = " ".join([n.get("title", ""), n.get("author", ""),
                         " ".join(n.get("tags", []))]).lower()
        if keywords:
            if not any(k.lower() in text for k in keywords):
                ok = False
        if tags:
            node_tags = set(n.get("tags", []))
            if not set(tags) & node_tags:
                ok = False
        if author and n.get("author") != author:
            ok = False
        if created_after and n.get("createdAt", "") < created_after:
            ok = False
        if ok:
            result.append(n)
    return result


# ---------------------------------------------------------------------------
# Rapport Markdown du tableau de bord
# ---------------------------------------------------------------------------

def build_dashboard(graph: dict, keywords: list = None, tags: list = None,
                    author: str = None, created_after: str = None,
                    days_inactive: int = 30) -> str:
    nodes = conversation_nodes(graph)
    edges = graph_edges(graph)
    filtered = filter_nodes(nodes, keywords, tags, author, created_after)
    filtered_ids = {n["id"] for n in filtered}
    filtered_edges = [e for e in edges
                      if e.get("source") in filtered_ids and e.get("target") in filtered_ids]
    orphans = find_orphans(filtered, filtered_edges)
    metrics = compute_metrics(filtered, filtered_edges)
    health = vault_health(filtered, days_inactive)

    lines = []
    lines.append("# Tableau de bord OMNI-INTER-NOTEBOOK-LM (GERICODE 3)")
    lines.append(f"_Généré le : {datetime.now(timezone.utc).isoformat()}_")
    lines.append("")
    lines.append("## 1. Aperçu")
    lines.append(f"- Conversations affichées : {metrics['total_conversations']}")
    lines.append(f"- Arêtes CASIS : {metrics['total_edges']}")
    lines.append(f"- Conversations orphelines : {len(orphans)}")
    lines.append("")

    lines.append("## 2. Graphe CASIS (Mermaid)")
    lines.append("```mermaid")
    lines.append(mermaid_graph(filtered, filtered_edges, orphans))
    lines.append("```")
    lines.append("")

    lines.append("## 3. Conversations orphelines")
    if orphans:
        for oid in orphans:
            n = next((x for x in filtered if x["id"] == oid), {})
            lines.append(f"- {oid} — {n.get('title', '(sans titre)')}")
    else:
        lines.append("_Aucune conversation orpheline._")
    lines.append("")

    lines.append("## 4. Métriques BigQuery")
    lines.append(f"- Total conversations : {metrics['total_conversations']}")
    lines.append("### Par auteur")
    for a, c in sorted(metrics["by_author"].items(), key=lambda x: -x[1]):
        lines.append(f"- {a} : {c}")
    lines.append("### Par tag")
    for t, c in sorted(metrics["by_tag"].items(), key=lambda x: -x[1]):
        lines.append(f"- {t} : {c}")
    lines.append("### Par semaine")
    for w, c in sorted(metrics["by_week"].items()):
        lines.append(f"- {w} : {c}")
    lines.append("")

    lines.append("## 5. Santé des voûtes NotebookLM")
    active = sum(1 for v in health.values() if v["status"] == "active")
    inactive = sum(1 for v in health.values() if v["status"] == "inactive")
    erreur = sum(1 for v in health.values() if v["status"] == "erreur")
    lines.append(f"- Voûtes actives : {active}")
    lines.append(f"- Voûtes inactives (> {days_inactive} j) : {inactive}")
    lines.append(f"- Voûtes en erreur : {erreur}")
    lines.append("")
    lines.append("### Détail par voûte")
    for vid, info in sorted(health.items()):
        lines.append(f"- {vid} : {info['status']} ({info['conversations']} conv., "
                     f"dernière activité {info['last_activity'] or 'NC'})")
    lines.append("")

    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Générateur de tableau de bord OMNI-INTER-NOTEBOOK-LM"
    )
    parser.add_argument("--graph", required=True, help="Chemin JSON du graphe M3-Tree")
    parser.add_argument("--output", default="-", help="Fichier de sortie Markdown (- = stdout)")
    parser.add_argument("--dot", help="Génère aussi le fichier DOT du graphe CASIS")
    parser.add_argument("--keywords", help="Mots-clés de recherche (séparés par des virgules)")
    parser.add_argument("--tags", help="Tags de filtre (séparés par des virgules)")
    parser.add_argument("--author", help="Filtre par auteur")
    parser.add_argument("--created-after", help="Filtre date création (ISO-8601)")
    parser.add_argument("--days-inactive", type=int, default=30,
                        help="Jours d'inactivité pour marquer une voûte inactive")
    args = parser.parse_args(argv)

    graph = load_graph(args.graph)
    keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None

    report = build_dashboard(
        graph, keywords=keywords, tags=tags, author=args.author,
        created_after=args.created_after, days_inactive=args.days_inactive,
    )

    if args.output == "-":
        print(report)
    else:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(report)

    if args.dot:
        nodes = conversation_nodes(graph)
        edges = graph_edges(graph)
        orphans = find_orphans(nodes, edges)
        with open(args.dot, "w", encoding="utf-8") as fh:
            fh.write(dot_graph(nodes, edges, orphans))

    return 0


if __name__ == "__main__":
    sys.exit(main())
