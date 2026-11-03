---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_GRP_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/geri-rules-propagator/SKILL.md
---

# Skill - geri-rules-propagator

## Objectif

Charge et priorise les regles locales de `.geri/rules/` sur les regles globales non versionnees de KiloCode (`~/.kilocode/rules/`). Garantit que les regles specifiques au depot GeriCode priment sur les regles globales generiques.

## Declencheur

- Demarrage d'une session KiloCode dans un depot GeriCode.
- Conflit entre une regle locale `.geri/rules/` et une regle globale `~/.kilocode/rules/`.
- Chargement explicite des regles de gouvernance d'un depot specifique.

## Entrees

- Chemin vers le dossier `.geri/rules/` du depot cible.
- Chemin vers le dossier `~/.kilocode/rules/` global.
- Nom de la regle a charger ou a verifier.

## Sorties

- Liste des regles locales prioritaires detectees.
- Rapport de conflit entre regles locales et globales.
- Autorisation ou rejet du chargement d'une regle globale en doublon.
- Code retour 0 si priorite etablie, code retour 1 si conflit non resolu.

## Regles Operationnelles

### 1. Priorite absolue aux regles locales .geri/rules/
Toute regle presente dans `.geri/rules/` du depot actif prime sur toute regle du meme nom dans `~/.kilocode/rules/`.

### 2. Detection de doublon
Si une regle existe a la fois en local et en global, la regle locale est conservee et la regle globale est ignoree avec un avertissement journalise.

### 3. Journalisation des conflits
Chaque conflit de regle est consigne dans un log de gouvernance avec le nom de la regle, le depot et la decision prise.

### 4. Rejet des regles globales non versionnees
Les regles globales non versionnees (absentes de git) ne peuvent pas surcharger une regle locale versionnee.

### 5. Escalade
En cas de conflit non resolu entre une regle locale et une regle globale critique, signaler pour intervention HITL.
