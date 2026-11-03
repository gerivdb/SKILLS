---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_DQ_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-distributed-query/SKILL.md
---

# Skill - m3-distributed-query

## Objectif

Orchestrateur de requetes distribuees multi-voutes dans le maillage des ~60 NotebookLM. Fournit un point d'entree unique optimise pour une requete spanning plusieurs voutes, evitant le scan sequentiel de chaque voute. Primitive M3-Tree de requete distribuee.

## Declencheur

- Requete cible spanning plusieurs voutes simultanement.
- Demande de recherche transversale sur le maillage des ~60 voutes.
- Latence excessive due a un scan sequentiel des voutes.
- Requete necessitant une agregation de resultats provenant de plusieurs sources.

## Entrees

- Requete de recherche (mots-cles, filtres, profondeur).
- Liste des voutes cibles (toutes ou sous-ensemble).
- Strategie de parallele (nombre de voutes interrogees simultanement).
- Budget de temps maximal pour la requete (en secondes).

## Sorties

- Resultats agreges des voutes interrogees.
- Rapport de performance (temps de reponse, voutes repondantes, voutes en echec).
- Code retour 0 si requete reussie, 1 si resultats partiels, 2 si echec total.

## Regles Operationnelles

### 1. Parallelisation des requetes
Interroger les voutes cibles en parallele plutot qu'en sequence pour minimiser la latence totale.

### 2. Limite de parallelisme
Nombre de voutes interrogees simultanement configure (par defaut : 10) pour eviter de saturer le reseau ou les sources.

### 3. Agregation des resultats
Fusionner les resultats provenant de plusieurs voutes en une reponse coherente, en dedupliquant les chunks identiques.

### 4. Timeout par voute
Chaque sous-requete a un timeout individuel pour eviter qu'une voute lente ne bloque l'ensemble.

### 5. Journalisation
Chaque requete distribuee est consignee avec les voutes sollicitees, le temps de reponse et le nombre de resultats retournes.
