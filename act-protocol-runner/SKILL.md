---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_APR_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/act-protocol-runner/SKILL.md
---

# Skill - act-protocol-runner

## Objectif

Executer les transitions d'etat du protocole ACT (ACT-V19.2.1-FINALLY-PROPOSED.md) et valider les checkpoints HITL. Garantit que chaque transition d'etat est precedee d'une validation HITL lorsque requise.

## Declencheur

- Demande de transition d'etat du protocole ACT.
- Validation d'un checkpoint HITL avant passage a l'etat suivant.
- Execution d'une sequence d'etats ACT dans un flux de travail.

## Entrees

- Fichier de protocole ACT (ex: ACT-V19.2.1-FINALLY-PROPOSED.md).
- Etat actuel du protocole.
- Etat cible souhaite.
- Identifiant du checkpoint HITL a valider.

## Sorties

- Rapport de transition d'etat (reussi / echec / en attente HITL).
- Validation HITL (approuvee / rejetee / en attente).
- Code retour 0 si transition reussie, 1 si echec, 2 si en attente HITL.

## Regles Operationnelles

### 1. Validation HITL obligatoire avant transition
Aucune transition d'etat ne peut etre executee sans validation prealable du checkpoint HITL associe, si le protocole l'exige.

### 2. Execution sequentielle des etats
Les transitions d'etat doivent etre executees dans l'ordre defini par le protocole ACT. Sauter un etat est interdit.

### 3. Journalisation des transitions
Chaque transition est consignee avec l'etat source, l'etat cible, l'horodatage et l'identifiant HITL.

### 4. Rejet en cas d'etat invalide
Si l'etat cible n'est pas une transition valide depuis l'etat actuel, la transition est rejetee avec un message d'erreur.

### 5. Escalade HITL
Si le checkpoint HITL est en attente ou rejete, le protocole s'arrete et attend l'intervention humaine.
