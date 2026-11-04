---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_WOA_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-worktree-orphan-auditor/SKILL.md
---

# Skill - m3-worktree-orphan-auditor

## Objectif

Auditer et nettoyer les worktrees orphelins non gerees par les moteurs KIX, VEX et TRIX. Garantit que chaque worktree dans le repertoire de travail est lie a une branche active et ne consomme pas d'espace disque inutilement. Primitive M3-Tree d'audit des worktrees orphelins.

## Declencheur

- Detection de worktrees sans branche associee dans le repertoire de travail.
- Presence de dossiers de travail residuels apres suppression d'une branche.
- Demande d'audit periodique des worktrees actifs.
- Augmentation de l'espace disque consomme par des worktrees inactifs.

## Entrees

- Chemin vers le repertoire de travail principal.
- Liste des branches actives dans le depot.
- Seuil d'inactivite (en jours, par defaut : 7).
- Liste des worktrees proteges (ne jamais supprimer).

## Sorties

- Rapport d'audit (worktrees orphelins detects, espace disque recuperable).
- Code retour 0 si aucun orphelin, 1 si nettoyage reussi, 2 si echec partiel.

## Regles Operationnelles

### 1. Scan des worktrees
Lister tous les worktrees enregistres dans le repertoire de travail.

### 2. Verification de la branche associee
Pour chaque worktree, verifier que sa branche associee existe encore dans le depot distant ou local.

### 3. Suppression des worktrees orphelins
Supprimer les worktrees dont la branche a ete supprimee ou qui ne sont plus lies a aucune branche active.

### 4. Protection des worktrees actifs
Ne jamais supprimer un worktree lie a une branche active ou marque comme protege.

### 5. Journalisation
Chaque suppression de worktree est consignee avec le nom du worktree, la branche associee et l'horodatage.
