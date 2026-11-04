---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_CTG_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-cpu-throttle-governor/SKILL.md
---

# Skill - m3-cpu-throttle-governor

## Objectif

Surveiller la charge CPU de la station ENV2 (HP Z600, Dual Xeon E5620) et appliquer une regulation dynamique (throttling) des competences non critiques lorsque la charge depasse un seuil critique. Garantit que les sous-arbres M3-Tree ne saturent pas le materiel. Primitive M3-Tree de gouvernance thermique et CPU.

## Declencheur

- Charge CPU moyenne depassant 60 pour cent sur la station ENV2.
- Detection d'une surcharge thermique imminente sur les Dual Xeon E5620.
- Demande de mise en pause temporaire des competences peu prioritaires.
- Surveillance periodique de la charge processeur.

## Entrees

- Seuil de charge CPU maximale acceptable (en pour cent, par defaut : 60).
- Intervalle de mesure (en secondes, par defaut : 30).
- Liste des competences prioritaires a proteger (ne jamais throttler).
- Liste des competences throttleables (pouvant etre mises en pause).

## Sorties

- Etat de la charge CPU (normale / elevee / critique).
- Decision de throttling (actif / inactif).
- Liste des competences suspendues ou reprisees.
- Code retour 0 si charge normale, 1 si throttling actif, 2 si charge critique.

## Regles Operationnelles

### 1. Mesure periodique de la charge CPU
Effectuer une mesure de la charge CPU moyenne a intervalles reguliers (par defaut : 30 secondes).

### 2. Application du throttling
Si la charge depasse le seuil (60 pour cent), mettre en pause les competences throttleables une par une jusqu'a ce que la charge redescende sous le seuil.

### 3. Reprise automatique
Lorsque la charge CPU redescend sous le seuil, reprendre les competences suspendues dans l'ordre inverse de leur mise en pause.

### 4. Protection des competences prioritaires
Les competences marquees comme prioritaires ne sont jamais throttlees, meme en cas de surcharge.

### 5. Journalisation
Chaque mesure de charge et chaque decision de throttling sont consignees avec le pourcentage CPU, la liste des competences affectees et l'horodatage.
