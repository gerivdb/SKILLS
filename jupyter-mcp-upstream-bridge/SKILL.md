---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_JUB_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/jupyter-mcp-upstream-bridge/SKILL.md
---

# Skill - jupyter-mcp-upstream-bridge

## Objectif

Verifie et etablit la liaison entre le proxy stdio MCP et le serveur Jupyter actif (port 3001/8888). Garantit que le backend Jupyter-MCP est accessible via le gateway unifie.

## Declencheur

- Declaration d'un nouveau backend Jupyter-MCP dans la configuration.
- Verification de la liaison proxy stdio MCP vers le serveur Jupyter.
- Echec de connexion au serveur Jupyter sur le port configure.

## Entrees

- Identifiant du backend Jupyter-MCP.
- Port du serveur Jupyter (3001 ou 8888).
- Chemin vers le proxy stdio MCP.

## Sorties

- Liaison etablie / echec.
- Rapport de statut du serveur Jupyter (actif / inactif / injoignable).
- Code retour 0 si liaison etablie, 1 si echec, 2 si serveur Jupyter inactif.

## Regles Operationnelles

### 1. Verification du serveur Jupyter
Avant d'etablir la liaison, verifier que le serveur Jupyter repond sur le port configure (3001 ou 8888).

### 2. Etablissement du pont stdio MCP
Si le serveur Jupyter est actif, creer le pont entre le proxy stdio MCP et le serveur Jupyter upstream.

### 3. Gestion gracieuse des erreurs
Si le serveur Jupyter est inactif, le gateway retourne une liste d'outils configures sans crasher et signale l'etat dans les logs.

### 4. Surveillance continue
Le statut de la liaison est verifie periodiquement pour detecter toute degradation du serveur Jupyter.

### 5. Escalade
Si le serveur Jupyter reste inactif pendant une periode prolongee, signaler pour intervention HITL.
