---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_CSB_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/citizen-skill-binder/SKILL.md
---

# Skill - citizen-skill-binder

## Objectif

Resout l'Impense 3 : lie les default_skills de chaque citizen a son instanciation sans charger le catalogue global. Garantit que chaque citizen ne charge que ses competences par defaut.

## Declencheur

- Instanciation d'un citizen dans le systeme L3.
- Chargement des competences par defaut d'un citizen.
- Verification que seules les default_skills sont chargees.

## Entrees

- Nom du citizen a instancier.
- Liste des default_skills declarees pour ce citizen.
- Chemin vers le catalogue global des skills (a eviter).

## Sorties

- Liste des competences liees au citizen.
- Confirmation que le catalogue global n'a pas ete charge.
- Code retour 0 si liaison reussie, 1 si citizen non trouve, 2 si default_skills manquantes.

## Regles Operationnelles

### 1. Liaison des default_skills uniquement
Chaque citizen ne charge que ses competences par defaut declarees dans default_skills, jamais le catalogue global.

### 2. Pas de chargement du catalogue global
Le catalogue global des skills n'est jamais charge lors de l'instanciation d'un citizen, pour eviter la consommation inutile de memoire.

### 3. Verification des default_skills
Si un citizen ne possede pas de default_skills declarees, l'instanciation est bloquee avec un message d'erreur.

### 4. Isolation des citizens
Chaque citizen possede son propre ensemble de competences, isole des autres citizens.

### 5. Journalisation
Chaque liaison citizen-competences est consignee avec le nom du citizen, les competences liees et l'horodatage.
