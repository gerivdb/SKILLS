#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
m3_mapper.py — Moteur d'Auto-Poïèse Topologique (M3 Mapper Engine).

Fournit le décorateur @m3_synapse qui instrumentre toute fonction de test
d'exploration. Chaque tentative est capturée, classée (VALIDATED_PATH,
DEAD_END, BLOCKED, FRAGILE_DEBT) et inscrite dans le graphe topologique
topology.json. Le rendu Markdown/Mermaid est généré automatiquement par
render.py.

Architecture :
    domain > tree > branch > synapse

Chaque synapse possède un état :
    VALIDATED_PATH (✅) — Chemin validé, méthode de référence
    DEAD_END (❌)        — Mur architectural, preuve d'échec documentée
    BLOCKED (🛑)         — Blocage systémique (timeout, UI dialog, etc.)
    FRAGILE_DEBT (⚠️)    — Fonctionne mais sous-optimal / fragile

Usage :
    from m3_mapper import m3_synapse, update_topology, load_topology, save_topology

    @m3_synapse(branch_name="CDP_Pur", synapse_name="loadUnpacked_string")
    def test_loadUnpacked_string():
        response = cdp.evaluate("chrome.developerPrivate.loadUnpacked(...)")
        if "Unexpected property" in response:
            raise APIError("N'accepte pas les chemins String")
        return response

    # Après exécution, topology.json est mis à jour automatiquement.
    # Puis : python render.py pour générer le Markdown/Mermaid.
"""

import json
import os
import sys
import traceback
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

# ---------------------------------------------------------------------------
# Configuration par défaut
# ---------------------------------------------------------------------------

DEFAULT_TOPOLOGY_PATH = Path(__file__).resolve().parent / "topology.json"
DEFAULT_DOMAIN = "default_domain"

STATUSES = {
    "VALIDATED_PATH": "✅",
    "DEAD_END": "❌",
    "BLOCKED": "🛑",
    "FRAGILE_DEBT": "⚠️",
}


# ---------------------------------------------------------------------------
# Helpers de lecture/écriture du graphe
# ---------------------------------------------------------------------------

def load_topology(path: Union[str, Path] = DEFAULT_TOPOLOGY_PATH) -> Dict[str, Any]:
    """Charge le fichier topology.json. Crée un graphe vide s'il n'existe pas."""
    path = Path(path)
    if not path.exists():
        return {
            "$schema": "m3-topology-v1",
            "domain": DEFAULT_DOMAIN,
            "description": "",
            "version": "1.0.0",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "trees": {},
            "metadata": {
                "total_trees": 0,
                "total_branches": 0,
                "total_synapses": 0,
                "validated_paths": 0,
                "dead_ends": 0,
                "blocked": 0,
                "last_updated_utc": "",
                "generator": "m3_mapper_engine_v1",
            },
        }
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_topology(topo: Dict[str, Any], path: Union[str, Path] = DEFAULT_TOPOLOGY_PATH) -> None:
    """Écrit le graphe dans topology.json (écriture atomique)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    topo["metadata"]["last_updated_utc"] = datetime.now(timezone.utc).isoformat()
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(topo, f, ensure_ascii=False, indent=2)
    tmp.replace(path)


def _ensure_tree(topo: Dict[str, Any], tree_id: str, tree_name: str = "", description: str = "") -> Dict[str, Any]:
    trees = topo.setdefault("trees", {})
    if tree_id not in trees:
        trees[tree_id] = {
            "name": tree_name or tree_id,
            "description": description,
            "branches": {},
        }
    return trees[tree_id]


def _ensure_branch(
    topo: Dict[str, Any],
    tree_id: str,
    branch_id: str,
    branch_name: str = "",
    description: str = "",
) -> Dict[str, Any]:
    tree = _ensure_tree(topo, tree_id)
    branches = tree.setdefault("branches", {})
    if branch_id not in branches:
        branches[branch_id] = {
            "name": branch_name or branch_id,
            "description": description,
            "synapses": {},
        }
    return branches[branch_id]


def _ensure_synapse(
    topo: Dict[str, Any],
    tree_id: str,
    branch_id: str,
    synapse_id: str,
    synapse_name: str = "",
) -> Dict[str, Any]:
    branch = _ensure_branch(topo, tree_id, branch_id)
    synapses = branch.setdefault("synapses", {})
    if synapse_id not in synapses:
        synapses[synapse_id] = {
            "name": synapse_name or synapse_id,
            "status": None,
            "error_class": None,
            "evidence": "",
            "evidence_full": "",
            "timestamp": "",
            "script": "",
            "conclusion": "",
        }
    return synapses[synapse_id]


# ---------------------------------------------------------------------------
# Décorateur principal
# ---------------------------------------------------------------------------

class M3SynapseError(Exception):
    """Erreur levée par une fonction décorée @m3_synapse pour marquer une impasse."""
    pass


class APIError(M3SynapseError):
    """Erreur d'API (ex: Unexpected property, Value must be an instance of...)."""
    pass


class TimeoutError(M3SynapseError):
    """Erreur de timeout / blocage système."""
    pass


def m3_synapse(
    branch_name: str,
    synapse_name: str,
    expected_outcome: str = "VALIDATED_PATH",
    tree_id: str = "T-DEFAULT",
    tree_name: str = "Default Tree",
    script: str = "",
    domain: str = "default_domain",
):
    """
    Décorateur qui instrumentre une fonction de test d'exploration.

    Paramètres :
        branch_name : Nom de la branche (ex: "CDP_Pur", "Hybride")
        synapse_name : Nom de la synapse (ex: "loadUnpacked_string")
        expected_outcome : Résultat attendu ("VALIDATED_PATH", "DEAD_END", etc.)
        tree_id : Identifiant de l'arbre (ex: "T-EXT")
        tree_name : Nom de l'arbre
        script : Chemin vers le script de preuve associé
        domain : Domaine d'appartenance (ex: "CDP_Chromium_147")

    Comportement :
        - Si la fonction lève une exception → la synapse est marquée
          DEAD_END (ou BLOCKED si TimeoutError) avec le message d'erreur.
        - Si la fonction réussit → la synapse est marquée VALIDATED_PATH
          avec la valeur de retour comme preuve.
        - Le graphe topology.json est mis à jour après chaque appel.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        import asyncio

        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                branch_id = branch_name.lower().replace(" ", "_").replace("-", "_")
                synapse_id = synapse_name.lower().replace(" ", "_").replace("-", "_")
                print(f"🔬 Exploration: {branch_name} → {synapse_name}")

                topo = load_topology()
                topo["domain"] = domain
                start_ts = datetime.now(timezone.utc)

                try:
                    result = await func(*args, **kwargs)

                    # Succès
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": expected_outcome,
                        "error_class": None,
                        "evidence": str(result)[:200] if result else "Fonction exécutée sans erreur",
                        "evidence_full": str(result),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Synapse validée : {func.__name__} a retourné avec succès.",
                    })
                    save_topology(topo)
                    print(f"   ✅ VALIDATED_PATH : {synapse_name}")
                    return result

                except TimeoutError as e:
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "BLOCKED",
                        "error_class": "TimeoutError",
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Blocage système : {func.__name__} a expiré ({e}).",
                    })
                    save_topology(topo)
                    print(f"   🛑 BLOCKED : {synapse_name} ({e})")
                    raise

                except M3SynapseError as e:
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "DEAD_END",
                        "error_class": type(e).__name__,
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Impasse architecturale : {func.__name__} ({e}).",
                    })
                    save_topology(topo)
                    print(f"   ❌ DEAD_END : {synapse_name} ({e})")
                    raise

                except Exception as e:
                    # Toute autre exception est traitée comme une impasse
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "DEAD_END",
                        "error_class": type(e).__name__,
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Échec inattendu : {func.__name__} ({e}).",
                    })
                    save_topology(topo)
                    print(f"   ❌ DEAD_END : {synapse_name} ({e})")
                    raise

            return wrapper
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                branch_id = branch_name.lower().replace(" ", "_").replace("-", "_")
                synapse_id = synapse_name.lower().replace(" ", "_").replace("-", "_")
                print(f"🔬 Exploration: {branch_name} → {synapse_name}")

                topo = load_topology()
                topo["domain"] = domain
                start_ts = datetime.now(timezone.utc)

                try:
                    result = func(*args, **kwargs)

                    # Succès
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": expected_outcome,
                        "error_class": None,
                        "evidence": str(result)[:200] if result else "Fonction exécutée sans erreur",
                        "evidence_full": str(result),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Synapse validée : {func.__name__} a retourné avec succès.",
                    })
                    save_topology(topo)
                    print(f"   ✅ VALIDATED_PATH : {synapse_name}")
                    return result

                except TimeoutError as e:
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "BLOCKED",
                        "error_class": "TimeoutError",
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Blocage système : {func.__name__} a expiré ({e}).",
                    })
                    save_topology(topo)
                    print(f"   🛑 BLOCKED : {synapse_name} ({e})")
                    raise

                except M3SynapseError as e:
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "DEAD_END",
                        "error_class": type(e).__name__,
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Impasse architecturale : {func.__name__} ({e}).",
                    })
                    save_topology(topo)
                    print(f"   ❌ DEAD_END : {synapse_name} ({e})")
                    raise

                except Exception as e:
                    # Toute autre exception est traitée comme une impasse
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "DEAD_END",
                        "error_class": type(e).__name__,
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Échec inattendu : {func.__name__} ({e}).",
                    })
                    save_topology(topo)
                    print(f"   ❌ DEAD_END : {synapse_name} ({e})")
                    raise

            return wrapper
    return decorator


# ---------------------------------------------------------------------------
# API directe (pour mise à jour manuelle sans décorateur)
# ---------------------------------------------------------------------------

def mark_synapse(
    topo: Dict[str, Any],
    tree_id: str,
    branch_id: str,
    synapse_id: str,
    status: str,
    synapse_name: str = "",
    evidence: str = "",
    evidence_full: str = "",
    error_class: Optional[str] = None,
    script: str = "",
    conclusion: str = "",
    persist: bool = False,
) -> Dict[str, Any]:
    """Marque manuellement une synapse dans le graphe (sans décorateur).

    Si persist=True, le graphe est sauvegardé sur disque. Sinon, la modification
    reste en mémoire uniquement (non-destructive).
    """
    syn = _ensure_synapse(topo, tree_id, branch_id, synapse_id, synapse_name)
    syn.update({
        "status": status,
        "error_class": error_class,
        "evidence": evidence,
        "evidence_full": evidence_full,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "script": script,
        "conclusion": conclusion,
    })
    if persist:
        save_topology(topo)
    return syn


def update_tree(
    topo: Dict[str, Any],
    tree_id: str,
    tree_name: str = "",
    description: str = "",
) -> Dict[str, Any]:
    return _ensure_tree(topo, tree_id, tree_name, description)


def update_branch(
    topo: Dict[str, Any],
    tree_id: str,
    branch_id: str,
    branch_name: str = "",
    description: str = "",
) -> Dict[str, Any]:
    return _ensure_branch(topo, tree_id, branch_id, branch_name, description)


# ---------------------------------------------------------------------------
# Point d'entrée CLI (optionnel : mettre à jour les métadonnées)
# ---------------------------------------------------------------------------

def recompute_metadata(topo: Dict[str, Any]) -> Dict[str, Any]:
    """Recalcule les métadonnées globales (comptes par statut)."""
    trees = topo.get("trees", {})
    total_trees = len(trees)
    total_branches = 0
    total_synapses = 0
    validated = 0
    dead_ends = 0
    blocked = 0

    for tree in trees.values():
        branches = tree.get("branches", {})
        total_branches += len(branches)
        for branch in branches.values():
            synapses = branch.get("synapses", {})
            total_synapses += len(synapses)
            for syn in synapses.values():
                st = syn.get("status")
                if st == "VALIDATED_PATH":
                    validated += 1
                elif st == "DEAD_END":
                    dead_ends += 1
                elif st == "BLOCKED":
                    blocked += 1

    topo["metadata"] = {
        "total_trees": total_trees,
        "total_branches": total_branches,
        "total_synapses": total_synapses,
        "validated_paths": validated,
        "dead_ends": dead_ends,
        "blocked": blocked,
        "last_updated_utc": datetime.now(timezone.utc).isoformat(),
        "generator": "m3_mapper_engine_v1",
    }
    return topo


class M3Navigator:
    """Navigateur du graphe topologique M3."""

    def __init__(self, topology_path=DEFAULT_TOPOLOGY_PATH):
        self.topology = load_topology(topology_path)

    def get_validated_paths(self, tree_id):
        tree = self.topology.get("trees", {}).get(tree_id)
        if not tree:
            return []
        result = []
        for branch_id, branch in tree.get("branches", {}).items():
            for syn_id, syn in branch.get("synapses", {}).items():
                if syn.get("status") == "VALIDATED_PATH":
                    result.append({
                        "branch": branch.get("name", branch_id),
                        "synapse": syn.get("name", syn_id),
                        "evidence": syn.get("evidence", ""),
                        "script": syn.get("script", ""),
                    })
        return result

    def get_dead_ends(self, tree_id):
        tree = self.topology.get("trees", {}).get(tree_id)
        if not tree:
            return []
        result = []
        for branch_id, branch in tree.get("branches", {}).items():
            for syn_id, syn in branch.get("synapses", {}).items():
                if syn.get("status") == "DEAD_END":
                    result.append({
                        "branch": branch.get("name", branch_id),
                        "synapse": syn.get("name", syn_id),
                        "evidence": syn.get("evidence", ""),
                        "error_class": syn.get("error_class"),
                    })
        return result

    def get_blocked(self, tree_id):
        tree = self.topology.get("trees", {}).get(tree_id)
        if not tree:
            return []
        result = []
        for branch_id, branch in tree.get("branches", {}).items():
            for syn_id, syn in branch.get("synapses", {}).items():
                if syn.get("status") == "BLOCKED":
                    result.append({
                        "branch": branch.get("name", branch_id),
                        "synapse": syn.get("name", syn_id),
                        "evidence": syn.get("evidence", ""),
                    })
        return result

    def get_next_frontier(self, tree_id):
        tree = self.topology.get("trees", {}).get(tree_id)
        if not tree:
            return []
        frontiers = []
        for branch_id, branch in tree.get("branches", {}).items():
            synapses = branch.get("synapses", {})
            has_validated = any(s.get("status") == "VALIDATED_PATH" for s in synapses.values())
            if not has_validated:
                continue
            for syn_id, syn in synapses.items():
                if not syn.get("status"):
                    frontiers.append({
                        "branch": branch.get("name", branch_id),
                        "branch_id": branch_id,
                        "synapse": syn.get("name", syn_id),
                        "synapse_id": syn_id,
                        "type": "synapse_untested_in_validated_branch",
                        "hypothesis": f"Puisque '{branch.get('name', branch_id)}' contient déjà un chemin validé, tester '{syn.get('name', syn_id)}' est la prochaine étape logique.",
                    })
            if not synapses:
                frontiers.append({
                    "branch": branch.get("name", branch_id),
                    "branch_id": branch_id,
                    "synapse": None,
                    "synapse_id": None,
                    "type": "branch_empty_in_validated_tree",
                    "hypothesis": f"La branche '{branch.get('name', branch_id)}' est vide. Créer une première synapse ici.",
                })
        return frontiers

    def generate_navigation_report(self, tree_id):
        tree = self.topology.get("trees", {}).get(tree_id)
        if not tree:
            return f"Tree '{tree_id}' introuvable."
        validated = self.get_validated_paths(tree_id)
        dead_ends = self.get_dead_ends(tree_id)
        blocked = self.get_blocked(tree_id)
        frontiers = self.get_next_frontier(tree_id)
        lines = []
        lines.append(f"# 🧭 Rapport de Navigation M3 — {tree.get('name', tree_id)}")
        lines.append("")
        lines.append(f"Domaine : {self.topology.get('domain', '?')}")
        lines.append(f"Arbre : {tree.get('name', tree_id)}")
        lines.append("")
        lines.append("## 📍 Position actuelle")
        lines.append("")
        lines.append(f"- {len(validated)} chemin(s) validé(s)")
        lines.append(f"- {len(dead_ends)} mur(s) documenté(s)")
        lines.append(f"- {len(blocked)} blocage(s)")
        lines.append(f"- {len(frontiers)} frontière(s) identifiée(s)")
        lines.append("")
        if validated:
            lines.append("## 🟢 Chemins validés (à utiliser, ne plus retester)")
            lines.append("")
            for v in validated:
                lines.append(f"- **{v['branch']} → {v['synapse']}**")
                if v.get("evidence"):
                    lines.append(f"  - Preuve : {v['evidence']}")
            lines.append("")
        if dead_ends:
            lines.append("## 🔴 Impasses (à ne jamais retenter)")
            lines.append("")
            for d in dead_ends:
                lines.append(f"- **{d['branch']} → {d['synapse']}**")
                if d.get("evidence"):
                    lines.append(f"  - Raison : {d['evidence']}")
            lines.append("")
        if frontiers:
            lines.append("## 🟡 Prochaines actions recommandées (frontières)")
            lines.append("")
            lines.append("Ces zones sont adjacentes à des chemins validés et n'ont pas encore été testées.")
            lines.append("")
            for i, f in enumerate(frontiers, 1):
                syn = f.get("synapse") or "[nouvelle synapse à créer]"
                branch = f.get("branch") or "[nouvelle branche]"
                lines.append(f"{i}. **{branch} → {syn}**")
                lines.append(f"   Hypothèse : {f['hypothesis']}")
            lines.append("")
        else:
            lines.append("## 🟡 Prochaines actions recommandées")
            lines.append("")
            lines.append("Aucune frontière détectée automatiquement. Toutes les synapses des branches validées ont été testées.")
            lines.append("Suggestion : créer une nouvelle branche dans cet arbre pour explorer une autre stratégie.")
            lines.append("")
        return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="M3 Mapper Engine — Outil de gestion du graphe topologique")
    parser.add_argument("--recompute", action="store_true", help="Recalcule les métadonnées globales")
    parser.add_argument("--topology", default=str(DEFAULT_TOPOLOGY_PATH), help="Chemin vers topology.json")
    args = parser.parse_args()

    topo = load_topology(args.topology)
    if args.recompute:
        topo = recompute_metadata(topo)
        save_topology(topo, args.topology)
        print(f"Métadonnées recalculées : {topo['metadata']}")
