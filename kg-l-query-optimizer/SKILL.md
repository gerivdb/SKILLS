---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_KLQO_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/kg-l-query-optimizer/SKILL.md
---

# Skill - kg-l-query-optimizer

## Objectif

Optimise le temps de traversee du Knowledge Graph L4 lors de la resolution de dependances complexes. Reduit la latence des requetes causales sur le graphe KG-L.

## Declencheur

- Requete de traversee du graphe KG-L lente.
- Resolution de dependances complexes dans le Knowledge Graph.
- Latence excessive sur les requetes causales inter-repos.

## Entrees

- Requete TQL (Triadic Query Language) a executer sur le graphe KG-L.
- Noeuds de depart et de fin pour la traversee.
- Profondeur maximale de traversee.

## Sorties

- Resultat de la requete optimisee.
- Temps de traversee mesure (en millisecondes).
- Code retour 0 si requete executee, 1 si timeout, 2 si graphe inaccessible.

## Regles Operationnelles

### 1. Optimisation de traversee
Utiliser des algorithmes de parcours optimises (BFS, Dijkstra) pour reduire le temps de traversee du graphe.

### 2. Mise en cache des requetes frequentes
Mettre en cache les resultats des requetes KG-L les plus courantes pour eviter les recalculs.

### 3. Limite de profondeur
Limiter la profondeur de traversee pour eviter les boucles infinies et les requetes trop longues.

### 4. Timeout de requete
Chaque requete KG-L a un timeout maximum pour ne pas bloquer le systeme.

### 5. Journalisation
Chaque requete est consignee avec le temps de reponse, le nombre de noeuds visites et le statut.
