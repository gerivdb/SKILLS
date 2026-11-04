---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_ONB_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-omni-notebook-bridge/SKILL.md
---

# Skill - m3-omni-notebook-bridge

## Objectif

Point d'entree du pont GAS (Google Apps Script) pour le maillage OMNI-INTER-NOTEBOOK-LM. Detecte les nouvelles conversations NotebookLM via les webhooks GAS, valide leur frontmatter, et cree le noeud correspondant dans le M3-Tree (graphe causal des conversations). Premier maillon de la chaine OMNI-INTER-NOTEBOOK-LM.

## Declencheur

- Reception d'un webhook GAS provenant d'une nouvelle conversation NotebookLM (evenement onCreate).
- Modification d'une conversation existante (evenement onEdit) requiring une mise a jour du noeud M3-Tree.
- Suppression d'une conversation (evenement onDelete) requiring une marque de suppression dans le graphe.
- Demande manuelle de rattachement d'une conversation existante au maillage M3-Tree.

## Entrees

- Identifiant de la conversation NotebookLM (notebookId).
- Titre de la conversation (title).
- Horodatage de creation (createdAt).
- Tags et categories declarees dans la conversation.
- Identifiant du workspace cible (targetWorkspaceId).
- Empreinte semantique (embedding vector) de la conversation, si disponible.
- Liste des conversations liees (referencedConversationIds), si disponible.

## Sorties

- Creation d'un noeud M3-Tree avec un intent_hash unique.
- Lien vers les conversations liees (edges de type reference, suite, contradiction, approfondissement).
- Enregistrement dans le registre des conversations (MANIFEST ou base dediee).
- Code retour 0 si le noeud est cree, 1 si la conversation existe deja, 2 si echec de validation.

## Regles Operationnelles

### 1. Verification de l'integrite de l'entree
Toute entree provenant du webhook GAS doit contenir un notebookId valide et un titre non vide. Si l'un de ces champs est manquant, le processus est arrete avec un message d'erreur explicite.

### 2. Verification de l'unicite
Avant de creer un noeud, verifier que le notebookId n'existe pas deja dans le registre des conversations. Si le noeud existe deja, retourner un code retour 1 sans creation de doublon.

### 3. Creation du noeud M3-Tree
Creer un noeud dans le M3-Tree avec l'intent_hash derive du notebookId et de l'horodatage. Le noeud contient tous les metadonnees extraits : titre, date, auteur, tags, empreinte semantique.

### 4. Liaison aux conversations liees
Si des conversations liees sont declarees (referencedConversationIds), creer des aretes de type "reference" ou "suite" entre le nouveau noeud et chacun des noeuds cibles dans le M3-Tree.

### 5. Journalisation
Chaque creation de noeud est consignee avec le notebookId, l'intent_hash, le nombre d'aretes creees et l'horodatage.

### 6. Escalade
Si le notebookId est invalide ou si la creation du noeud echoue, signaler pour intervention HITL avec le message d'erreur detaille.
