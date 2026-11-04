---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_G3D_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-gericode3-dashboard/SKILL.md
---

# Skill - m3-gericode3-dashboard

## Objectif

Interface de pilotage unifiee dans GERICODE 3 pour le maillage OMNI-INTER-NOTEBOOK-LM. Affiche le graphe CASIS, la liste des conversations orphelines, les metriques BigQuery et la sante des voutes NotebookLM (~60). Permet le pilotage centralise de tout le maillage depuis une interface unique.

## Declencheur

- Demande d'affichage du tableau de bord CASIS dans GERICODE 3.
- Demande de visualisation du graphe de conversations (Mermaid/DOT).
- Demande de liste des conversations orphelines.
- Demande de visualisation des metriques BigQuery (nombre de conversations par semaine, par auteur, par tag).
- Demande de verification de la sante des ~60 voutes NotebookLM.

## Entrees

- Identifiant de la voute cible (optionnel, pour filtrer par voute).
- Filtre de recherche (mots-cles, tags, date).
- Type de visualisation demandee (graphe, liste, tableau de bord).
- Identifiant du workspace cible (optionnel).

## Sorties

- Tableau de bord CASIS affiche (graphe de conversations, metriques, alertes).
- Liste des conversations orphelines (sans aucun lien).
- Metriques BigQuery (nombre de conversations, distribution par auteur, par tag).
- Statut de sante des voutes NotebookLM (active / inactive / orpheline).
- Code retour 0 si affichage reussi, 1 si aucune donnee, 2 si echec d'affichage.

## Regles Operationnelles

### 1. Affichage du tableau de bord CASIS
Rendre le graphe de conversations sous forme Mermaid/DOT dans GERICODE 3. Inclure le colorage par type de lien et par statut (orphelin, active, archivee).

### 2. Liste des conversations orphelines
Afficher la liste des conversations qui n'ont aucun lien vers une autre conversation. Permettre le rattachement manuel ou automatique a une conversation existante.

### 3. Metriques BigQuery
Afficher les statistiques aggregees : nombre total de conversations, nombre par semaine, par auteur, par tag, par voute.

### 4. Sante des voutes
Afficher l'etat de chaque voute NotebookLM (~60) : active, inactive, en erreur. Indiquer le dernier horodatage d'activite de chaque voute.

### 5. Filtrage et recherche
Permettre le filtrage des conversations par mots-cles, par tags, par date, par workspace cible.

### 6. Journalisation
Chaque consultation du tableau de bord est consignee avec le type de visualisation, le nombre de resultats retournes et l'horodatage.
