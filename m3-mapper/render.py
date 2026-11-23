#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render.py — Générateur de documentation M3.
Lit topology.json et produit TOPOLOGY_M3_CHROMIUM.md avec tableaux,
diagrammes Mermaid et rapport de navigation M3Navigator.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from m3_mapper import M3Navigator

DEFAULT_TOPOLOGY = Path(__file__).resolve().parent / "topology.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent.parent.parent / "L0-CANON" / "ENV3-repo" / "TOPOLOGY_M3_CHROMIUM.md"

STATUS_EMOJI = {
    "VALIDATED_PATH": "✅",
    "DEAD_END": "❌",
    "BLOCKED": "🛑",
    "FRAGILE_DEBT": "⚠️",
    None: "❓",
}


def load_topology(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def escape_mermaid(text: str) -> str:
    return text.replace('"', '\\"').replace("&", "&amp;")


def render_mermaid_tree(topo: Dict[str, Any], tree_id: str, tree: Dict[str, Any]) -> str:
    lines = []
    tree_name = escape_mermaid(tree.get("name", tree_id))
    lines.append(f"    Root[{tree_name}]")

    branches = tree.get("branches", {})
    for branch_id, branch in branches.items():
        branch_name = escape_mermaid(branch.get("name", branch_id))
        lines.append(f"    Root --> B_{branch_id}[{branch_name}]")
        synapses = branch.get("synapses", {})
        for syn_id, syn in synapses.items():
            status = syn.get("status")
            emoji = STATUS_EMOJI.get(status, "❓")
            syn_name = escape_mermaid(syn.get("name", syn_id))
            evidence = escape_mermaid(syn.get("evidence", "")[:60])
            label = f"{syn_name}{emoji}"
            if evidence:
                label += f'["{evidence}"]'
            lines.append(f"    B_{branch_id} --> S_{syn_id}[{label}]")

    return "\n".join(lines)


def render_mermaid_all(topo: Dict[str, Any]) -> str:
    parts = []
    trees = topo.get("trees", {})
    for tree_id, tree in trees.items():
        tree_name = tree.get("name", tree_id)
        parts.append(f"### {tree_name}\n")
        parts.append("```mermaid")
        parts.append("graph TD")
        parts.append(render_mermaid_tree(topo, tree_id, tree))
        parts.append("```\n")
    return "\n".join(parts)


def render_markdown_tree(topo: Dict[str, Any], tree_id: str, tree: Dict[str, Any]) -> str:
    print(f"[DEBUG render.py] Rendering tree: {tree_id} -> {tree.get('name', tree_id)}", file=sys.stderr)
    lines = []
    tree_name = tree.get("name", tree_id)
    tree_desc = tree.get("description", "")
    lines.append(f"## 🌳 M3 Tree : {tree_name}")
    if tree_desc:
        lines.append(f"\n*{tree_desc}*\n")
    lines.append("| Branche | Synapse | Statut | Preuve |")
    lines.append("|---------|---------|--------|--------|")

    branches = tree.get("branches", {})
    for branch_id, branch in branches.items():
        branch_name = branch.get("name", branch_id)
        synapses = branch.get("synapses", {})
        first_syn = True
        for syn_id, syn in synapses.items():
            syn_name = syn.get("name", syn_id)
            status = syn.get("status")
            emoji = STATUS_EMOJI.get(status, "❓")
            evidence = syn.get("evidence", "")
            script = syn.get("script", "")

            branch_cell = f"**{branch_name}**" if first_syn else ""
            first_syn = False

            line = f"| {branch_cell} | {syn_name} | {emoji} {status} | {evidence} |"
            if script:
                line = line.rstrip(" |") + f" | `{script}` |"
            lines.append(line)
    lines.append("")
    return "\n".join(lines)


def render_markdown_all(topo: Dict[str, Any]) -> str:
    lines = []

    meta = topo.get("metadata", {})
    domain = topo.get("domain", "default_domain")
    description = topo.get("description", "")
    version = topo.get("version", "1.0.0")
    generated_at = topo.get("generated_at_utc", "")

    lines.append(f"# TOPOLOGY_M3 — {domain}")
    lines.append("")
    lines.append(f"**Version** : {version}  |  **Généré le** : {generated_at}  |  **Domaine** : {domain}")
    if description:
        lines.append(f"\n{description}\n")
    lines.append("---")
    lines.append("")

    # Résumé métadonnées
    lines.append("## 📊 Résumé du graphe")
    lines.append("")
    lines.append(f"- **Trees** : {meta.get('total_trees', 0)}")
    lines.append(f"- **Branches** : {meta.get('total_branches', 0)}")
    lines.append(f"- **Synapses** : {meta.get('total_synapses', 0)}")
    lines.append(f"- **✅ Chemins validés** : {meta.get('validated_paths', 0)}")
    lines.append(f"- **❌ Impasses** : {meta.get('dead_ends', 0)}")
    lines.append(f"- **🛑 Blocages** : {meta.get('blocked', 0)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Détails par Tree
    lines.append("## 🌳 Arbres (Trees)")
    lines.append("")

    trees = topo.get("trees", {})
    for tree_id, tree in trees.items():
        tree_lines = render_markdown_tree(topo, tree_id, tree)
        print(f"[DEBUG render_markdown_all] Tree {tree_id}: {len(tree_lines)} lignes ajoutées", file=sys.stderr)
        print(f"[DEBUG render_markdown_all]   Contient T-JEVX: {'T-JEVX' in tree_lines}", file=sys.stderr)
        if tree_id == "T-JEVX":
            print(f"[DEBUG render_markdown_all]   tree_lines[:200]: {repr(tree_lines[:200])}", file=sys.stderr)
        lines.append(tree_lines)

    # Diagrammes Mermaid
    lines.append("## 🗺️ Visualisations Mermaid")
    lines.append("")
    lines.append(render_mermaid_all(topo))

    # Rapport de navigation M3 (boussole)
    lines.append("## 🧭 Rapport de Navigation M3")
    lines.append("")
    lines.append("Ce rapport ne décrit pas ce qui a été fait. Il indique où aller ensuite.")
    lines.append("")

    nav = M3Navigator(str(DEFAULT_TOPOLOGY))
    for tree_id, tree in trees.items():
        report = nav.generate_navigation_report(tree_id)
        lines.append(report)
        lines.append("")

    # Légende
    lines.append("---")
    lines.append("")
    lines.append("## 📋 Légende des statuts")
    lines.append("")
    lines.append("| Symbole | Statut | Signification |")
    lines.append("|---------|--------|---------------|")
    lines.append("| ✅ | VALIDATED_PATH | Chemin validé, méthode de référence |")
    lines.append("| ❌ | DEAD_END | Mur architectural, preuve d'échec documentée |")
    lines.append("| 🛑 | BLOCKED | Blocage systémique (timeout, UI dialog, etc.) |")
    lines.append("| ⚠️ | FRAGILE_DEBT | Fonctionne mais sous-optimal / fragile |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Document généré automatiquement par `m3_mapper.render` à partir de `topology.json`. Ne pas éditer manuellement.*")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="M3 Mapper — Générateur de documentation topologique")
    parser.add_argument("--topology", default=str(DEFAULT_TOPOLOGY), help="Chemin vers topology.json")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Chemin vers le fichier Markdown de sortie")
    args = parser.parse_args()

    topo_path = Path(args.topology)
    output_path = Path(args.output)

    if not topo_path.exists():
        print(f"[ERREUR] Fichier topology introuvable : {topo_path}")
        sys.exit(1)

    topo = load_topology(topo_path)
    trees = topo.get("trees", {})
    print(f"[DEBUG render.py] Trees trouvés dans le YAML: {list(trees.keys())}", file=sys.stderr)
    markdown = render_markdown_all(topo)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"[OK] Document généré : {output_path}")
    print(f"[OK] Trees : {topo.get('metadata', {}).get('total_trees', 0)} | "
          f"Synapses : {topo.get('metadata', {}).get('total_synapses', 0)} | "
          f"Validés : {topo.get('metadata', {}).get('validated_paths', 0)}")
    print(f"[DEBUG] Longueur du document généré: {len(markdown)} caractères")
    print(f"[DEBUG] Contient T-JEVX: {'T-JEVX' in markdown}")
    print(f"[DEBUG] Contient JEVX — Décideur: {'JEVX — Décideur' in markdown}")
    print(f"[DEBUG] Contient T-JEVX-IMPASSES: {'T-JEVX-IMPASSES' in markdown}")
    print(f"[DEBUG] Longueur du document généré: {len(markdown)} caractères")
    print(f"[DEBUG] Contient T-JEVX: {'T-JEVX' in markdown}")


if __name__ == "__main__":
    main()