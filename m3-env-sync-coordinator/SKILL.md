---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_ESC_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-env-sync-coordinator/SKILL.md
---

# Skill - m3-env-sync-coordinator

## Objectif

Assurer la synchronisation isomorphique entre la station physique ENV2 (HP Z600) et le maillage cloud ENV3 (NotebookLM, orchestration semantique). Garantit que chaque modification ou test valide sur ENV2 est packagee et transmise vers le depot central ENV0, et que ENV3 met a jour les graphes M3-Tree pour notifier ENV2 via les vecteurs synaptiques. Primitive M3-Tree de synchronisation inter-strates.

## Declencheur

- Modification ou test valide sur ENV2 a publier vers ENV0.
- Mise a jour des graphes M3-Tree sur ENV3 a notifier vers ENV2.
- Demande de synchronisation manuelle entre ENV2 et ENV3.
- Detection d'une divergence entre l'etat local et l'etat distant.

## Entrees

- Chemin vers le repertoire de staging local (ex: D:\DO\WEB\GAS_STAGING).
- Chemin vers le depot distant ENV0 (gerivdb/SKILLS).
- Liste des fichiers a pousser.
- Vecteur synaptique s associe a la modification.

## Sorties

- Rapport de synchronisation (fichiers pousses, fichiers recuperes, etat de synchronisation).
- Code retour 0 si synchronisation reussie, 1 si divergence non resolue, 2 si echec de poussee.

## Regles Operationnelles

### 1. Poussee staging (ENV2 vers ENV3)
Tout changement valide sur ENV2 est package sous forme de manifeste serialise et transmis vers le depot central ENV0.

### 2. Diffusion et retroaction (ENV3 vers ENV2)
ENV3 met a jour les graphes M3-Tree et notifie ENV2 via les vecteurs synaptiques, garantissant que la station physique et le cloud mesh partagent le meme arbre decisionnel.

### 3. Verification de coherence
Avant chaque synchronisation, verifier que l'etat local et l'etat distant sont coherents. En cas de divergence, arreter et signaler.

### 4. Journalisation
Chaque operation de synchronisation est consignee avec les fichiers pousses, les fichiers recuperes et l'horodatage.
