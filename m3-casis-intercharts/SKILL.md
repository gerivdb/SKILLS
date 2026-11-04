---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_CI_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-casis-intercharts/SKILL.md
---

# Skill - m3-casis-intercharts

## Objectif

Construire et maintenir le graphe de dependances entre conversations NotebookLM (CASIS - Cross-Artifact Signal Intelligence System). Modelise les relations entre conversations sous forme de Directed Acyclic Graph (DAG) : references, suites, contradictions, approfondissements. Rend le graphe interrogeable et renderable sous forme Mermaid/DOT pour GERICODE 3.

## Declencheur

- Creation d'un nouveau node M3-Tree par m3-omni-notebook-bridge (nouvelle conversation NotebookLM).
- Ajout d'un lien explicite entre deux conversations (utilisateur lie deux notes).
- Detection automatique de similarite semantique entre deux conversations (embedding distance).
- Demande de rendu du graphe CASIS (Mermaid/DOT) pour visualisation dans GERICODE 3.
- Demande de detection de conversations orphelines (sans aucun lien vers une autre).

## Entrees

- Identifiant du node source (conversation A).
- Identifiant du node cible (conversation B).
- Type de lien (reference, suite, contradiction, approfondissement, template).
- Score de similitude semantique (si lien auto-detecte).
- Identifiant du graphe CASIS cible (par defaut : graphe principal du workspace).

## Sorties

- Edge cree dans le graphe CASIS (source -> cible avec type de lien).
- Mise a jour du graphe M3-Tree avec l'arrete correspondante.
- Rapport de construction (nombre de nodes, nombre d'edges, cycles detectes).
- Code retour 0 si edge cree, 1 si edge existe deja, 2 si cycle detecte, 3 si echec.

## Regles Operationnelles

### 1. Verification des nodes sources et cibles
Avant de creer un edge, verifier que les deux nodes existent dans le M3-Tree. Si l'un des deux manque, arreter avec code retour 2.

### 2. Detection de cycles
Avant d'ajouter un edge, verifier qu'il ne cree pas de cycle dans le DAG. Si un cycle est detecte, refuser l'edge et retourner le code retour 2.

### 3. Creation de l'arrete
Creer l'edge dans le graphe CASIS avec le type de lien specifie. Mettre a jour le node M3-Tree correspondant avec la reference vers l'arrete.

### 4. Detection automatique de similitude
Si deux conversations ont un embedding similaire (distance < seuil), proposer automatiquement la creation d'un edge de type "reference". L'utilisateur valide ou rejette.

### 5. Detection des orphelins
Periodiquement, scanner tous les nodes du graphe pour identifier ceux sans aucun edge entrant ni sortant. Les marquer comme "orphelins" dans le registre.

### 6. Rendu Mermaid/DOT
Generer une representation Mermaid ou DOT du graphe pour visualisation dans GERICODE 3. Inclure le colorage par type de lien et par statut (orphelin, active, archivee).

### 7. Journalisation
Chaque creation d'edge est consignee avec le node source, le node cible, le type de lien et l'horodatage.
