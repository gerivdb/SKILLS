---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_VSR_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-vault-session-reaper/SKILL.md
---

# Skill - m3-vault-session-reaper

## Objectif

Nettoyer les sessions de voutes NotebookLM abandonnees dans le maillage des ~60 voutes. Empeche l'accumulation de sessions orphelines qui consomment des ressources et compliquent les requetes inter-voutes. Primitive M3-Tree de moissonneur de sessions de voutes.

## Declencheur

- Detection d'une session de voute inactive depuis plus du seuil configure.
- Demande de nettoyage periodique des sessions de voutes.
- Augmentation du nombre de sessions actives sans utilisation reelle.
- Detection d'une voute avec trop de sessions ouvertes simultanement.

## Entrees

- Liste des voutes du maillage (~60).
- Seuil d'inactivite d'une session (en minutes, par defaut : 60).
- Liste des sessions actives par voute.
- Nombre maximal de sessions simultanees par voute.

## Sorties

- Rapport de nettoyage (sessions fermees, voutes concernees, ressources liberees).
- Code retour 0 si nettoyage reussi, 1 si aucune session a fermer, 2 si echec partiel.

## Regles Operationnelles

### 1. Detection des sessions orphelines
Identifier les sessions de voutes sans activite depuis le seuil d'inactivite configure.

### 2. Fermeture des sessions abandonnees
Fermer les sessions identifiees une par une, en commencant par les plus anciennes.

### 3. Limite de securite
Ne pas fermer plus de 10 sessions par cycle pour eviter une desstabilisation du maillage.

### 4. Protection des sessions actives
Ne jamais fermer une session avec une activite recente ou marquee comme critique.

### 5. Journalisation
Chaque fermeture de session est consignee avec l'identifiant de la voute, l'identifiant de la session et l'horodatage.
