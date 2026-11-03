---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_SLU_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/skill-lazy-unloader/SKILL.md
---

# Skill - skill-lazy-unloader

## Objectif

Resout l'Impense 1 : implemente unload_skill(name) pour liberer la memoire token apres utilisation. Garantit que les skills chargees ne restent pas en memoire indefiniment.

## Declencheur

- Fin d'utilisation d'une skill chargee en memoire.
- Demande de liberation explicite d'une skill.
- Surveillance de la memoire token pendant une session longue.

## Entrees

- Nom de la skill a decharger (name).
- Reference vers l'instance de la skill en memoire.
- Timeout de dechargement (en secondes, par defaut 5).

## Sorties

- Confirmation de dechargement (skill liberee / non trouvee).
- Quantite de memoire liberee (en tokens).
- Code retour 0 si dechargement reussi, 1 si skill non trouvee.

## Regles Operationnelles

### 1. Fonction unload_skill(name)
Implemente une fonction qui supprime la skill du cache de chargement et libere sa memoire associee.

### 2. Verification de dependances
Avant de decharger, verifier qu'aucune autre skill active ne depend de cette skill.

### 3. Nettoyage des references
Supprimer toutes les references a la skill dans les registres actifs pour eviter les fuites de memoire.

### 4. Confirmation de liberation
Retourner la quantite de memoire liberee pour audit de performance.

### 5. Journalisation
Chaque dechargement est consigne avec le nom de la skill, la memoire liberee et l'horodatage.
