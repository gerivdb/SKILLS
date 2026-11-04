#!/usr/bin/env python3
"""
m3-casis-intercharts - Graphe de dependances entre conversations NotebookLM.
Construit et maintient le graphe CASIS (Cross-Artifact Signal Intelligence System).
Modele les relations entre conversations sous forme de DAG.
"""

import json, hashlib, datetime
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple, Optional

class CasisGraph:
    """Graphe de dependances entre conversations NotebookLM."""

    def __init__(self):
        # nodes: node_id -> metadata
        self.nodes: Dict[str, dict] = {}
        # edges: edge_id -> {source, target, type, timestamp}
        self.edges: Dict[str, dict] = {}
        # adjacency: source_id -> list of target_ids
        self.adjacency: Dict[str, List[str]] = defaultdict(list)
        # reverse adjacency: target_id -> list of source_ids
        self.reverse_adjacency: Dict[str, List[str]] = defaultdict(list)

    def add_node(self, node_id: str, metadata: dict) -> bool:
        """Ajoute un node au graphe. Retourne False si le node existe deja."""
        if node_id in self.nodes:
            return False
        self.nodes[node_id] = metadata
        self.adjacency[node_id] = []
        self.reverse_adjacency[node_id] = []
        return True

    def add_edge(self, source_id: str, target_id: str, edge_type: str = 'reference') -> dict:
        """
        Ajoute un edge dans le graphe.
        Retourne un dict avec le statut et des informations.
        """
        # Verification des nodes
        if source_id not in self.nodes:
            return {'status': 'error', 'message': f'Node source inconnu: {source_id}'}
        if target_id not in self.nodes:
            return {'status': 'error', 'message': f'Node cible inconnu: {target_id}'}

        # Verification de l'existence de l'edge
        for edge in self.adjacency.get(source_id, []):
            if edge == target_id:
                return {'status': 'duplicate', 'message': 'Edge existe deja'}

        # Detection de cycle (DFS)
        if self._would_create_cycle(source_id, target_id):
            return {'status': 'cycle', 'message': 'Cycle detecte, edge refuse'}

        # Creation de l'edge
        edge_id = 'edge_' + hashlib.sha256((source_id + target_id).encode('utf-8')).hexdigest()[:12]
        edge = {
            'edge_id': edge_id,
            'source': source_id,
            'target': target_id,
            'type': edge_type,
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
        self.edges[edge_id] = edge
        self.adjacency[source_id].append(target_id)
        self.reverse_adjacency[target_id].append(source_id)

        return {'status': 'created', 'edge_id': edge_id, 'edges_created': 1}

    def _would_create_cycle(self, source_id: str, target_id: str) -> bool:
        """Verifie si ajouter l'edge source->target cree un cycle."""
        # BFS depuis target pour voir si on peut atteindre source
        visited = set()
        queue = deque([target_id])
        while queue:
            current = queue.popleft()
            if current == source_id:
                return True
            if current in visited:
                continue
            visited.add(current)
            for neighbor in self.adjacency.get(current, []):
                if neighbor not in visited:
                    queue.append(neighbor)
        return False

    def find_orphans(self) -> List[str]:
        """Trouve les nodes sans aucun edge entrant ni sortant."""
        orphans = []
        for node_id in self.nodes:
            if (node_id not in self.adjacency or not self.adjacency[node_id]) and \
               (node_id not in self.reverse_adjacency or not self.reverse_adjacency[node_id]):
                orphans.append(node_id)
        return orphans

    def find_communities(self) -> List[List[str]]:
        """Trouve les communautes de conversations liees (composantes connexes)."""
        visited = set()
        communities = []
        for node_id in self.nodes:
            if node_id not in visited:
                component = []
                queue = deque([node_id])
                while queue:
                    current = queue.popleft()
                    if current in visited:
                        continue
                    visited.add(current)
                    component.append(current)
                    for neighbor in self.adjacency.get(current, []):
                        if neighbor not in visited:
                            queue.append(neighbor)
                    for neighbor in self.reverse_adjacency.get(current, []):
                        if neighbor not in visited:
                            queue.append(neighbor)
                communities.append(component)
        return communities

    def find_shortest_path(self, source_id: str, target_id: str) -> Optional[List[str]]:
        """Trouve le chemin le plus court entre deux nodes (BFS)."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return None
        queue = deque([(source_id, [source_id])])
        visited = set()
        while queue:
            current, path = queue.popleft()
            if current == target_id:
                return path
            if current in visited:
                continue
            visited.add(current)
            for neighbor in self.adjacency.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return None

    def to_mermaid(self) -> str:
        """Genere un rendu Mermaid du graphe."""
        lines = ['graph TD']
        # Nodes
        for node_id, meta in self.nodes.items():
            label = meta.get('title', node_id)
            lines.append(f'    {node_id}["{label}"]')
        # Edges
        for edge_id, edge in self.edges.items():
            lines.append(f'    {edge["source"]} -->|{edge["type"]}| {edge["target"]}')
        return '\n'.join(lines)

    def to_dot(self) -> str:
        """Genere un rendu DOT du graphe."""
        lines = ['digraph G {']
        for node_id, meta in self.nodes.items():
            label = meta.get('title', node_id)
            lines.append(f'    "{node_id}" [label="{label}"];')
        for edge_id, edge in self.edges.items():
            lines.append(f'    "{edge["source"]}" -> "{edge["target"]}" [label="{edge["type"]}"];')
        lines.append('}')
        return '\n'.join(lines)

    def stats(self) -> dict:
        """Retourne des statistiques sur le graphe."""
        return {
            'node_count': len(self.nodes),
            'edge_count': len(self.edges),
            'orphan_count': len(self.find_orphans()),
            'community_count': len(self.find_communities())
        }


# Exemple d'utilisation (test)
if __name__ == '__main__':
    graph = CasisGraph()
    graph.add_node('n1', {'title': 'Conversation A', 'layer': 'L4-TOOLS'})
    graph.add_node('n2', {'title': 'Conversation B', 'layer': 'L4-TOOLS'})
    graph.add_node('n3', {'title': 'Conversation C', 'layer': 'L4-TOOLS'})
    result1 = graph.add_edge('n1', 'n2', 'reference')
    result2 = graph.add_edge('n2', 'n3', 'suite')
    print(result1)
    print(result2)
    print(graph.stats())
    print(graph.to_mermaid())
