---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_MHE_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/merge-hygiene-enforcer/SKILL.md
---

# Skill - merge-hygiene-enforcer

## Objectif

Bloquer les merges pollues par un nombre excessif de fichiers non desires (seuil : 700 fichiers). Synchronise avec la version de GeriCode pour garantir l'hygiene des merges dans tous les depots du meta-cluster.

## Declencheur

- Tentative de merge de branche feature vers main.
- Pull request avec plus de 700 fichiers modifies.
- Merge detecte comme pollue par des fichiers non lies a la fonctionnalite.

## Entrees

- Branche source de la merge.
- Branche cible de la merge.
- Nombre de fichiers modifies dans la branche source.
- Liste des chemins de fichiers modifies.

## Sorties

- Autorisation ou rejet de la merge.
- Rapport d'hygiene (conforme / pollue / bloque).
- Code retour 0 si merge autorise, 1 si rejete (trop de fichiers), 2 si en attente de revue.

## Regles Operationnelles

### 1. Seuil de 700 fichiers
Toute merge comportant plus de 700 fichiers modifies est automatiquement rejetee. Le seuil est derive de la version GeriCode de reference.

### 2. Verification de la pertinence des fichiers
Chaque fichier modifie doit etre lie a la fonctionnalite de la branche. Les fichiers de configuration, de verrouillage ou de build non lies sont signales.

### 3. Blocage automatique
Si le seuil est depasse, la merge est bloquee et un message d'erreur indique le nombre de fichiers et le seuil autorise.

### 4. Exception HITL
Une exception peut etre accordee par intervention HITL explicite, consignee dans un journal de gouvernance.

### 5. Synchronisation GeriCode
Le seuil et les regles sont synchronises avec la version de reference de GeriCode pour garantir l'homogeneite du meta-cluster.
