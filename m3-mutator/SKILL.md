---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_MUTATOR_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-mutator/SKILL.md
---

# Skill - m3-mutator

## Objectif

Scanner le code source produit, identifier les redondances ou les frictions non detectees, et generer de maniere autonome de nouveaux sous-skills pour combler les angles morts sans intervention humaine (HOTL elargie). Primitive M3-Tree d'auto-mutation et de refactoring fractal.

## Declencheur

- Detection d'une friction recurrence dans un module ou un skill existant.
- Redondance de code identique entre plusieurs skills du meme quadrant.
- Demande de refactoring fractal sur une branche de competence du M3-Tree.
- Entropie detectee au-dessus du seuil tolere (H > 0.0) sur un pipeline d'execution.

## Entrees

- Chemin vers le code source ou le skill a analyser.
- Seuil d'entropie maximal acceptable (par defaut : 0.0).
- Niveau de mutation autorise (conservateur / modere / agressif).

## Sorties

- Rapport de mutation (skills generes / skills refactores / redondances eliminees).
- Liste des sous-skills crees avec leurs intent_hash respectifs.
- Code retour 0 si mutation reussie, 1 si aucune friction detectee, 2 si echec de generation.

## Regles Operationnelles

### 1. Scan de friction automatique
Analyser le code source pour detecter les motifs repeats, les boucles passives ou les frictions non couvertes par un skill existant.

### 2. Generation de sous-skills
Pour chaque angle mort identifie, generer un skill minimal specialise qui resout le probleme sans dupliquer une competence existante.

### 3. Refactoring fractal
Appliquer le refactoring de maniere recursive sur les branches du M3-Tree concernées, en preservant la retro-compatibilite des intent_hash.

### 4. HOTL elargie
Toute mutation generant un nouveau skill doit etre validee par un checkpoint HOTL avant integration dans le M3-Tree.

### 5. Journalisation
Chaque mutation est consignee dans le WAL avec le sceau Merkle, l'intent_hash du skill muté et l'horodatage.
