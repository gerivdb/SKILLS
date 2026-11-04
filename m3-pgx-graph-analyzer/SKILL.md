---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_PGX_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-pgx-graph-analyzer/SKILL.md
---

# Skill - m3-pgx-graph-analyzer

## Objectif

Moteur d'analyse de graphe PGX (Parallel Graph Analytics) sur le graphe de conversations NotebookLM. Execute des requetes TQL sur le graphe M3-Tree pour detecter les conversations orphelines, les communautes de conversations, les chemins critiques et les contradictions. Fournit des analyses topologiques pour GERICODE 3.

## Declencheur

- Demande d'analyse du graphe de conversations (communautes, chemins, orphelins).
- Detection de conversations orphelines (sans aucun lien vers une autre).
- Demande de chemin critique entre deux conversations.
- Analyse periodique de la topologie du graphe M3-Tree.

## Entrees

- Requete TQL (Ternary Query Language) sur le graphe de conversations.
- Identifiant de conversation source et cible pour l'analyse de chemin.
- Seuil de similarite pour la detection de communautes.
- Identifiant du graphe CASIS cible.

## Sorties

- Resultat de la requete TQL (liste de conversations, chemins, communautes).
- Liste des conversations orphelines detectees.
- Rapport d'analyse topologique (nombre de noeuds, nombre d'aretes, diametre, densite).
- Code retour 0 si analyse reussie, 1 si aucun resultat, 2 si echec de requete.

## Regles Operationnelles

### 1. Execution de requete TQL
Executer une requete TQL sur le graphe M3-Tree pour extraire les informations demandees. La requete peut filtrer par type de lien, par date, par auteur, par tags.

### 2. Detection de conversations orphelines
Identifier les conversations qui n'ont aucun edge entrant ni sortant dans le graphe CASIS. Les marquer comme "orphelines" dans le registre.

### 3. Analyse de chemin critique
Calculer le chemin le plus court entre deux conversations dans le graphe. Retourner la liste des conversations intermediaires et la longueur du chemin.

### 4. Detection de communautes
Grouper les conversations par similitude semantique et par liens directs. Identifier les communautes de conversations liees par un theme commun.

### 5. Calcul de metriques topologiques
Calculer le diametre du graphe, la densite, le nombre de noeuds et d'aretes. Fournir une vue d'ensemble de la topologie du graphe de conversations.

### 6. Journalisation
Chaque requete TQL est consignee avec le type de requete, le nombre de resultates retournes et l'horodatage.
