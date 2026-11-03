---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_EPS_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-epsilon-pruning/SKILL.md
---

# Skill - m3-epsilon-pruning

## Objectif

Utiliser les metriques de poids d'affinite et d'entropie pour elaguer en temps reel les branches de skills obsoletes ou sous-performantes dans le M3-Tree, garantissant une empreinte memorielle et cognitive toujours minimale (H = 0.0). Primitive M3-Tree d'elagage topologique automatise.

## Declencheur

- Entropie detectee au-dessus du seuil dans une branche du M3-Tree.
- Skill sous-performante ou non utilisee depuis une periode prolongee.
- Demande d'optimisation de l'empreinte memoire du M3-Tree.
- Revision periodique de l'arborescence de competences.

## Entrees

- Arbre de competences M3-Tree actuel.
- Metriques de poids d'affinite pour chaque skill.
- Metriques d'entropie par branche.
- Seuil d'entropie maximal acceptable (par defaut : 0.0).
- Seuil d'utilisation minimal (nombre d'appels minimum par periode).

## Sorties

- Rapport d'elagage (branches elagees / skills retirees / memoire liberee).
- M3-Tree mis a jour (sans les branches elagees).
- Code retour 0 si elagage reussi, 1 si aucune branche a elaguer, 2 si echec de modification.

## Regles Operationnelles

### 1. Mesure de l'entropie par branche
Calculer l'entropie de chaque branche du M3-Tree basee sur l'usage et la pertinence des skills.

### 2. Elagage des branches a haute entropie
Supprimer les branches dont l'entropie depasse le seuil maximal acceptable.

### 3. Retrait des skills inactives
Retirer les skills qui n'ont pas ete utilisees depuis la periode de reference definie.

### 4. Garantie d'entropie nulle
Veiller a ce que l'entropie globale du M3-Tree reste a 0.0 apres elagage.

### 5. Journalisation
Chaque operation d'elagage est consignee avec les branches retirees, les metriques d'entropie avant/apres et l'horodatage.
