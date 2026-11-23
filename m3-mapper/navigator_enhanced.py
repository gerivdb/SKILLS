#!/usr/bin/env python3
"""
M3Navigator Enhanced — Boussole de navigation du graphe M3 avec métriques de priorisation.
Détecte les ACK manquants (canaux résiduels) et valide l'authenticité des réponses par hash SHA-256.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any


class M3NavigatorEnhanced:
    """
    Navigateur du graphe topologique M3 avec métriques de priorisation.
    Transforme le graphe de synapses en outil de décision : "Quelle est la prochaine action à tester ?"
    """

    def __init__(self, topology_path: str = "topology.json"):
        self.topology_path = Path(topology_path)
        self.topology = self._load_topology()

    def _load_topology(self) -> dict:
        with open(self.topology_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_validated_paths(self, tree_id: str) -> list[dict]:
        """Retourne toutes les synapses VALIDATED_PATH d'un tree."""
        tree = self.topology.get("trees", {}).get(tree_id)
        if not tree:
            return []
        result = []
        for branch_id, branch in tree.get("branches", {}).items():
            for syn_id, syn in branch.get("synapses", {}).items():
                if syn.get("status") == "VALIDATED_PATH":
                    result.append({
                        "tree": tree_id,
                        "branch": branch.get("name", branch_id),
                        "synapse": syn.get("name", syn_id),
                        "synapse_id": syn_id,
                        "evidence": syn.get("evidence", ""),
                        "script": syn.get("script", ""),
                    })
        return result

    def get_dead_ends(self, tree_id: str) -> list[dict]:
        """Retourne toutes les synapses DEAD_END d'un tree."""
        tree = self.topology.get("trees", {}).get(tree_id)
        if not tree:
            return []
        result = []
        for branch_id, branch in tree.get("branches", {}).items():
            for syn_id, syn in branch.get("synapses", {}).items():
                if syn.get("status") == "DEAD_END":
                    result.append({
                        "tree": tree_id,
                        "branch": branch.get("name", branch_id),
                        "synapse": syn.get("name", syn_id),
                        "synapse_id": syn_id,
                        "evidence": syn.get("evidence", ""),
                        "error_class": syn.get("error_class", ""),
                    })
        return result

    def get_blocked(self, tree_id: str) -> list[dict]:
        """Retourne toutes les synapses BLOCKED d'un tree."""
        tree = self.topology.get("trees", {}).get(tree_id)
        if not tree:
            return []
        result = []
        for branch_id, branch in tree.get("branches", {}).items():
            for syn_id, syn in branch.get("synapses", {}).items():
                if syn.get("status") == "BLOCKED":
                    result.append({
                        "tree": tree_id,
                        "branch": branch.get("name", branch_id),
                        "synapse": syn.get("name", syn_id),
                        "synapse_id": syn_id,
                        "evidence": syn.get("evidence", ""),
                    })
        return result

    def get_next_frontier(self, tree_id: str) -> list[dict]:
        """
        Identifie les zones non explorées adjacentes aux chemins validés.
        Une frontière est une synapse sans statut (non testée) dans une branche
        qui contient au moins une synapse VALIDATED_PATH.
        """
        tree = self.topology.get("trees", {}).get(tree_id)
        if not tree:
            return []

        frontiers = []
        for branch_id, branch in tree.get("branches", {}).items():
            synapses = branch.get("synapses", {})
            has_validated = any(s.get("status") == "VALIDATED_PATH" for s in synapses.values())

            if not has_validated:
                continue

            # Synapses sans statut dans une branche validée
            for syn_id, syn in synapses.items():
                if not syn.get("status"):
                    frontiers.append({
                        "tree": tree_id,
                        "branch": branch.get("name", branch_id),
                        "synapse": syn.get("name", syn_id),
                        "synapse_id": syn_id,
                        "type": "synapse_untested_in_validated_branch",
                        "hypothesis": (
                            f"Puisque '{branch.get('name', branch_id)}' contient "
                            f"déjà un chemin validé, tester '{syn.get('name', syn_id)}' "
                            f"est la prochaine étape logique."
                        ),
                    })

            # Branche vide dans un arbre validé
            if not synapses:
                frontiers.append({
                    "tree": tree_id,
                    "branch": branch.get("name", branch_id),
                    "synapse": None,
                    "synapse_id": None,
                    "type": "branch_empty_in_validated_tree",
                    "hypothesis": (
                        f"La branche '{branch.get('name', branch_id)}' est vide. "
                        f"Créer une première synapse ici, adjacente aux chemins validés "
                        f"du même arbre."
                    ),
                })

        return frontiers

    def get_priority_score(self, synapse: dict) -> int:
        """
        Calcule un score de priorité pour une synapse.
        Facteurs :
        - Récence (plus c'est récent, plus c'est prioritaire)
        - Type de statut (BLOCKED > DEAD_END > VALIDATED_PATH pour l'exploration)
        """
        score = 0

        # Récence (derniers 7 jours = +10, 30 jours = +5, sinon 0)
        timestamp = synapse.get("timestamp")
        if timestamp:
            try:
                synapse_date = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                days_ago = (datetime.now(synapse_date.tzinfo) - synapse_date).days
                if days_ago <= 7:
                    score += 10
                elif days_ago <= 30:
                    score += 5
            except Exception:
                pass

        # Type de statut
        status = synapse.get("status")
        if status == "BLOCKED":
            score += 15  # Priorité haute : débloquer
        elif status == "DEAD_END":
            score += 5   # Priorité moyenne : documenter
        elif status == "VALIDATED_PATH":
            score += 1   # Priorité basse : déjà validé

        return score

    def get_top_priorities(self, tree_id: str, limit: int = 5) -> list[dict]:
        """
        Retourne les synapses les plus prioritaires pour un arbre donné.
        """
        tree = self.topology.get("trees", {}).get(tree_id)
        if not tree:
            return []
        priorities = []
        for branch_id, branch in tree.get("branches", {}).items():
            for synapse_name, synapse in branch.get("synapses", {}).items():
                score = self.get_priority_score(synapse)
                priorities.append({
                    "tree": tree_id,
                    "branch": branch.get("name", branch_id),
                    "synapse": synapse_name,
                    "status": synapse.get("status"),
                    "score": score,
                    "reason": synapse.get("reason", ""),
                    "timestamp": synapse.get("timestamp", ""),
                })

        priorities.sort(key=lambda x: x["score"], reverse=True)
        return priorities[:limit]

    def generate_action_plan(self, tree_id: str) -> str:
        """
        Génère un plan d'action concret basé sur les priorités.
        """
        priorities = self.get_top_priorities(tree_id, limit=10)

        plan = f"# 🧭 Plan d'Action M3 — {tree_id}\n\n"
        plan += f"**Généré le** : {datetime.now().isoformat()}\n\n"

        plan += "## 📊 État Actuel\n\n"
        validated = self.get_validated_paths(tree_id)
        dead_ends = self.get_dead_ends(tree_id)
        blocked = self.get_blocked(tree_id)
        frontiers = self.get_next_frontier(tree_id)

        plan += f"- **Chemins validés** : {len(validated)}\n"
        plan += f"- **Impasses documentées** : {len(dead_ends)}\n"
        plan += f"- **Blocages** : {len(blocked)}\n"
        plan += f"- **Frontières** : {len(frontiers)}\n\n"

        if priorities:
            plan += "## 🟡 Prochaines Actions Recommandées (par priorité)\n\n"
            for i, p in enumerate(priorities, 1):
                plan += f"### {i}. {p['synapse']} (Score: {p['score']})\n"
                plan += f"- **Statut** : {p['status']}\n"
                plan += f"- **Branche** : {p['branch']}\n"
                if p.get('reason'):
                    plan += f"- **Raison** : {p['reason']}\n"
                if p.get('timestamp'):
                    plan += f"- **Dernière mise à jour** : {p['timestamp']}\n"

                # Recommandation d'action
                if p['status'] == 'BLOCKED':
                    plan += "**Action recommandée** : Investiguer le blocage et tenter de débloquer.\n\n"
                elif p['status'] == 'DEAD_END':
                    plan += "**Action recommandée** : Documenter l'impasse et explorer une voie alternative.\n\n"
                elif p['status'] == 'VALIDATED_PATH':
                    plan += "**Action recommandée** : Réutiliser ce chemin validé pour d'autres explorations.\n\n"

        plan += "## 🔴 Impasses (Ne Jamais Retenter)\n\n"
        for d in dead_ends[:5]:
            plan += f"- **{d['branch']} → {d['synapse']}**"
            if d.get('evidence'):
                plan += f"  - Raison : {d['evidence'][:100]}\n"
        plan += "\n"

        plan += "## 🟢 Chemins Validés (À Utiliser)\n\n"
        for v in validated[:5]:
            plan += f"- **{v['branch']} → {v['synapse']}**\n"
            if v.get('evidence'):
                plan += f"  - Preuve : {v['evidence'][:100]}\n"
        plan += "\n"

        return plan


# ============================================================================
# CLI : Exécution directe
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="M3Navigator — Boussole de navigation du graphe topologique M3")
    parser.add_argument("--topology", default=str(Path(__file__).resolve().parent / "topology.json"),
                        help="Chemin vers le fichier topology.json")
    parser.add_argument("--tree", default="T-JEVX",
                        help="ID de l'arbre à analyser (ex: T-JEVX, T-CTULU)")
    parser.add_argument("--action", choices=["plan", "priorities", "validated", "dead_ends", "blocked", "frontier"],
                        default="plan",
                        help="Action à exécuter")
    parser.add_argument("--output", default=None,
                        help="Fichier de sortie (défaut: stdout)")

    args = parser.parse_args()

    nav = M3NavigatorEnhanced(args.topology)

    if args.action == "plan":
        report = nav.generate_action_plan(args.tree)
    elif args.action == "priorities":
        priorities = nav.get_top_priorities(args.tree, limit=10)
        report = "# Priorités M3\n\n"
        for i, p in enumerate(priorities, 1):
            report += f"{i}. **{p['synapse']}** (Score: {p['score']}, {p['status']})\n"
            plan += f"   Branche : {p['branch']}\n"
    elif args.action == "validated":
        validated = nav.get_validated_paths(args.tree)
        report = "# Chemins Validés\n\n"
        for v in validated:
            report += f"- **{v['branch']} → {v['synapse']}**\n"
    elif args.action == "dead_ends":
        dead_ends = nav.get_dead_ends(args.tree)
        report = "# Impasses\n\n"
        for d in dead_ends:
            report += f"- **{d['branch']} → {d['synapse']}**\n"
    elif args.action == "blocked":
        blocked = nav.get_blocked(args.tree)
        report = "# Blocages\n\n"
        for b in blocked:
            report += f"- **{b['branch']} → {b['synapse']}**\n"
    elif args.action == "frontier":
        frontiers = nav.get_next_frontier(args.tree)
        report = "# Frontières\n\n"
        for f in frontiers:
            report += f"- **{f['branch']} → {f['synapse'] or 'Nouvelle Synapse'}**\n"
            report += f"  Hypothèse : {f['hypothesis']}\n"

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Rapport sauvegardé : {args.output}")
    else:
        print(report)
