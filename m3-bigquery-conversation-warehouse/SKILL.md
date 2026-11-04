---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_BCW_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-bigquery-conversation-warehouse/SKILL.md
---

# Skill - m3-bigquery-conversation-warehouse

## Objectif

Entrepot SQL des conversations NotebookLM dans BigQuery. Centralise les metadonnees de toutes les conversations du maillage (~60 vaults) pour permettre des requetes analytiques rapides et paralleles. Centralise les donnees pour le moteur PGX d'analyse graphique.

## Declencheur

- Creation d'un nouveau node M3-Tree par m3-omni-notebook-bridge (nouvelle conversation NotebookLM).
- Mise a jour d'une conversation existante (titre, tags, liens).
- Demande de requete analytique sur les conversations (nombre par semaine, par auteur, par tag).
- Synchronisation periodique entre le graphe M3-Tree et l'entrepot BigQuery.

## Entrees

- Identifiant de la conversation NotebookLM (conversationId).
- Titre de la conversation.
- Horodatage de creation et de derniere modification.
- Auteur et tags declares.
- Vecteur d'empreinte semantique (embedding vector).
- Identifiants des conversations liees (linkedConversationIds).
- Identifiant du workspace cible.

## Sorties

- Ligne inserie ou mise a jour dans la table BigQuery `conversations`.
- Rapport d'insertion (nombre de lignes, taille, horodatage).
- Code retour 0 si insertion reussi, 1 si doublon, 2 si echec d'insertion.

## Regles Operationnelles

### 1. Schema de la table BigQuery
La table `conversations` contient les colonnes suivantes :
- conversationId (STRING, cle primaire)
- title (STRING)
- createdAt (TIMESTAMP)
- updatedAt (TIMESTAMP)
- author (STRING)
- tags (ARRAY<STRING>)
- embeddingVector (ARRAY<FLOAT64>)
- linkedConversationIds (ARRAY<STRING>)
- workspaceId (STRING)
- m3TreeNodeId (STRING)

### 2. Insertion ou mise a jour (upsert)
Si le conversationId existe deja, mettre a jour les champs modifies. Sinon, inserer une nouvelle ligne.

### 3. Synchronisation periodique
Periodiquement, synchroniser toutes les conversations du graphe M3-Tree vers BigQuery pour detecter les divergences.

### 4. Journalisation
Chaque insertion ou mise a jour est consignee avec le conversationId, le type d'operation et l'horodatage.
