---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_VCC_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/verse-context-coordinator/SKILL.md
---

# Skill - verse-context-coordinator

## Objectif

Resout l'Impense 4 : coordonne verse_context.py avec le lazy-load pour exclure les schemas de skills de la compaction. Garantit que le contexte verset ne compacte pas les schemas de skills.

## Declencheur

- Chargement de verse_context.py avec lazy-load.
- Compaction du contexte verset.
- Exclusion des schemas de skills de la compaction.

## Entrees

- Chemin vers verse_context.py.
- Liste des schemas de skills a exclure.
- Mode de lazy-load (actif / inactif).

## Sorties

- Rapport de coordination (schemas exclus / schemas compactes).
- Statut du contexte verset (coordonne / en erreur).
- Code retour 0 si coordination reussie, 1 si echec d'exclusion, 2 si lazy-load desactive.

## Regles Operationnelles

### 1. Coordination verse_context.py avec lazy-load
Le module verse_context.py doit etre coordonne avec le mecanisme de lazy-load pour eviter les doublons.

### 2. Exclusion des schemas de skills
Les schemas de skills ne doivent jamais etre compactes dans le contexte verset. Ils restent accessibles via le lazy-load.

### 3. Verification avant compaction
Avant toute compaction du contexte, verifier qu'aucun schema de skills n'est inclus dans le jeu a compacter.

### 4. Rappel des schemas exclus
Les schemas exclus sont enregistres pour pouvoir etre recharges a la demande via le lazy-load.

### 5. Journalisation
Chaque operation de coordination est consignee avec les schemas exclus, le statut du lazy-load et l'horodatage.
