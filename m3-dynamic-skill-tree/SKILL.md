---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_DST_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-dynamic-skill-tree/SKILL.md
---

# Skill - m3-dynamic-skill-tree

## Objectif

Remplacer la liste lineaire ou le catalogue statique des skills par un M3-Tree decisionnel. Lorsqu'un probleme complexe est soumis, l'agent ne cherche plus un skill isole : il navigue dans le M3-Tree pour composer un pipeline d'execution sur-mesure combinant plusieurs competences de differents quadrants. Primitive M3-Tree de composition dynamique de skills.

## Declencheur

- Probleme complexe soumis necessitant plusieurs competences de quadrants differents.
- Absence de skill unique couvrant l'ensemble du besoin.
- Demande de composition a la volee de sous-competences.
- Entropie detectee dans le prompt necessitant une decomposition multi-etapes.

## Entrees

- Enonce du probleme complexe.
- Liste des skills disponibles avec leurs quadrants et triggers.
- Budget d'etapes maximum pour le pipeline d'execution.
- Contraintes de dependance entre competences (si applicables).

## Sorties

- Pipeline d'execution compose (sequence de skills et leurs parametres).
- Arbre de decision M3-Tree traverse (noeuds visites, edges empruntes).
- Code retour 0 si pipeline construit, 1 si aucune combinaison possible, 2 si budget d'etapes depasse.

## Regles Operationnelles

### 1. Navigation dans le M3-Tree
A partir du probleme soumis, traverser l'arbre decisionnel pour identifier les competences pertinentes a chaque etape.

### 2. Composition a la volee
Un skill principal peut phagocyter ou instancier des sous-competences en fonction de l'entropie detectee dans le prompt.

### 3. Respect du budget d'etapes
Limitez le nombre de competences sequentielles dans le pipeline pour eviter l'emballement cognitif.

### 4. Validation des dependances
Verifier que chaque competence appelee dans le pipeline a ses prerequis satisfaits avant execution.

### 5. Journalisation
Chaque composition de pipeline est consignee avec le M3-Tree traverse, les competences selectionnees et l'horodatage.
