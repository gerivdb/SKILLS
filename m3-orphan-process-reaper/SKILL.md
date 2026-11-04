---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_OPF_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-orphan-process-reaper/SKILL.md
---

# Skill - m3-orphan-process-reaper

## Objectif

Nettoyer les processus orphelins (git fsmonitor--daemon, instances IDE abandonnees, navigateurs zombies) qui echappent au controle des moteurs KIX, VEX et TRIX. Garantit que le maillage ENV2 ne soit pas pollue par des processus residuels consommant inutilement CPU et memoire. Primitive M3-Tree de reaper de processus orphelins.

## Declencheur

- Detection de processus git fsmonitor--daemon sans worktree associe.
- Presence de processus Code/pwsh/node orphelins sans fenetre utilisateur liee.
- Demande de nettoyage periodique des processus residuels.
- Augmentation anormale du nombre de processus git.exe en attente.

## Entrees

- Liste des processus candidates au nettoyage (nom, PID, ligne de commande).
- Seuil d'inactivite (en minutes, par defaut : 30).
- Liste des processus proteges (ne jamais tuer : Zen, Chrome actif, pwsh de l'utilisateur).
- Facteur de securite (ne pas tuer plus de N processus par cycle).

## Sorties

- Rapport de nettoyage (processus arretes, PIDs, memoire liberee).
- Code retour 0 si nettoyage reussi, 1 si aucun processus orphelin, 2 si echec partiel.

## Regles Operationnelles

### 1. Identification des processus orphelins
Scanner les processus git fsmonitor--daemon, node.exe, pwsh.exe sans fenetre associee ni worktree actif.

### 2. Verification de securite
Ne jamais arreter un processus marque comme protege (Zen actif, Chrome avec onglets ouverts, pwsh de l'utilisateur en cours).

### 3. Arret propre
Arreter les processus identifies un par un, en commencant par les plus anciens.

### 4. Limite de securite
Ne pas arreter plus de 5 processus par cycle pour eviter une destabilisation brute du systeme.

### 5. Journalisation
Chaque arret est consigne avec le PID, le nom du processus, la ligne de commande et l'horodatage.
