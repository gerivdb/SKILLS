---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_NWR_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-notebook-workspace-registrar/SKILL.md
---

# Skill - m3-notebook-workspace-registrar

## Objectif

Ajouter automatiquement toute nouvelle conversation NotebookLM au workspace cible configure. Elimine l'ajout manuel necessaire actuellement pour integrer une conversation dans la workspace cible. Premier relais apres le m3-omni-notebook-bridge dans la chaine OMNI-INTER-NOTEBOOK-LM.

## Declencheur

- Creation d'une nouvelle conversation NotebookLM detectee par m3-omni-notebook-bridge.
- Demande d'association d'une conversation existante a un workspace cible.
- Demande de rattachement retroactif de conversations orphelines a leur workspace cible.
- Changement de configuration du workspace cible dans GERICODE 3.

## Entrees

- Identifiant de la conversation NotebookLM (notebookId).
- Identifiant du workspace cible (targetWorkspaceId).
- Metadata de la conversation (titre, date, auteur, tags).
- Lien vers le node M3-Tree associe (cree par m3-omni-notebook-bridge).
- Permissions d'acces au workspace cible (lecture, ecriture).

## Sorties

- Conversation ajoutee au workspace cible.
- Confirmation d'association (workspace_id, notebook_id, statut).
- Mise a jour du registre des liens conversation-workspace.
- Code retour 0 si ajout reussi, 1 si la conversation est deja dans le workspace, 2 si echec d'ajout.

## Regles Operationnelles

### 1. Verification de l'existence de la conversation
Avant tout ajout, verifier que la conversation NotebookLM existe et est accessible. Si la conversation n'est pas trouvee, arreter avec un message d'erreur.

### 2. Verification de l'appartenance au workspace
Verifier que la conversation n'est pas deja associee au workspace cible. Si elle est deja presente, retourner un code retour 1 sans doublon.

### 3. Ajout au workspace cible
Ajouter la conversation au workspace cible specifie. Cette operation doit etre atomique : soit la conversation est entierement ajoutee, soit elle ne l'est pas.

### 4. Mise a jour du registre des liens
Mettre a jour le registre qui lie chaque conversation a son workspace cible. Cette entree permet la traque des conversations par workspace.

### 5. Mise a jour du node M3-Tree
Lier le node M3-Tree de la conversation au workspace cible. Cela permet de retrouver toutes les conversations d'un workspace via le graphe M3-Tree.

### 6. Journalisation
Chaque ajout est consigne avec le notebookId, le workspaceId, le statut et l'horodatage.

### 7. Escalade
Si l'ajout echoue (permissions manquantes, workspace inexistant), signaler pour intervention HITL avec le message d'erreur detaille.
