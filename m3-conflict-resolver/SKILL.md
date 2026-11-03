---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_CR_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-conflict-resolver/SKILL.md
---

# Skill - m3-conflict-resolver

## Objectif

Resoudre les conflits de versions inter-voutes dans le maillage des ~60 voutes NotebookLM. Deux voutes peuvent modifier le meme chunk simultanement sans strategie de merge. Primitive M3-Tree de resolution de conflits semantiques.

## Declencheur

- Deux voutes modifient le meme chunk simultanement.
- Detection d'un conflit de version sur un chunk partage.
- Demande de resolution manuelle ou automatique d'un conflit de merge.
- Incoherence de version entre la copie source et ses replicats.

## Entrees

- Identifiant du chunk en conflit.
- Voutes impliquees dans la modification simultanee.
- Versions concurrentes du chunk (contenu et horodatage).
- Strategie de resolution preferee (timestamp / priorite / merge manuel).

## Sorties

- Version resolue du chunk (fusionnee ou selectionnee).
- Rapport de conflit (voutes impliquees, strategies evaluees, decision prise).
- Code retour 0 si conflit resolu, 1 si conflit non resolu, 2 si intervention HITL requise.

## Regles Operationnelles

### 1. Detection de conflit simultane
Detecter quand deux voutes modifient le meme chunk avec des versions differentes et des horodatages proches.

### 2. Strategie de resolution par defaut
Appliquer la strategie configuree : timestamp (version la plus recente gagne), priorite (voute prioritaire gagne), ou merge manuel.

### 3. Propagation de la resolution
Une fois le conflit resolu, propager la version gagnante vers toutes les voutes detentrices d'une copie du chunk.

### 4. Intervention HITL pour les conflits complexes
Si le conflit ne peut pas etre resolu automatiquement (contenus incompatibles), marquer pour intervention humaine et bloquer la propagation.

### 5. Journalisation
Chaque resolution de conflit est consignee avec le chunk ID, les voutes impliquees, la strategie appliquee et l'horodatage.
