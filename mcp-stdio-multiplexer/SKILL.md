---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_MSM_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/mcp-stdio-multiplexer/SKILL.md
---

# Skill - mcp-stdio-multiplexer

## Objectif

Pool et reutilise les processus stdio MCP persistants sans saturer la table des descripteurs sous Windows. Garantit une gestion efficace des connexions stdio entre le gateway et les backends MCP.

## Declencheur

- Ouverture d'un nouveau processus stdio MCP pour un backend.
- Saturation de la table des descripteurs de fichiers sous Windows.
- Processus stdio MCP orphelins qui consomment des ressources.

## Entrees

- Identifiant du backend MCP (ex: jupyter-ai, filesystem).
- Chemin vers l'executable stdio MCP.
- Parametres de lancement du processus.

## Sorties

- Processus stdio MCP reutilise depuis le pool, ou nouveau processus cree.
- Rapport d'utilisation des descripteurs de fichiers.
- Code retour 0 si processus disponible, 1 si echec de creation, 2 si pool plein.

## Regles Operationnelles

### 1. Pool de processus persistants
Les processus stdio MCP sont maintenus dans un pool et reutilises pour plusieurs requetes, evitant la surcharge de creation/destruction.

### 2. Limite de descripteurs sous Windows
Le nombre de processus simultanes est limite pour ne pas saturer la table des descripteurs de fichiers Windows (par defaut : 10 processus concurrents).

### 3. Nettoyage des processus orphelins
Les processus stdio MCP inactifs depuis plus de 5 minutes sont arretes pour liberer les ressources.

### 4. Refus si pool plein
Si le pool est plein et qu'aucun processus n'est disponible, la demande est refusee avec un message d'erreur indiquant d'attendre ou d'augmenter la limite.

### 5. Sante des processus
Avant de relayer une requete, le skill verifie que le processus stdio cible est toujours vivant (health check).
