---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_NDP_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/network-discovery-prober/SKILL.md
---

# Skill - network-discovery-prober

## Objectif

Optimise les sondes externes (SearXNG, ChatJimmy, AppFlowy) pour ne pas retarder le boot du gateway. Garantit que les sondes de decouverte reseau sont parallelisees et ne bloquent pas le demarrage.

## Declencheur

- Boot du gateway avec sondes de decouverte externe.
- Sondage de SearXNG, ChatJimmy ou AppFlowy.
- Latence excessive lors du boot due aux sondes sequentielles.

## Entrees

- Liste des endpoints de decouverte a sonder.
- Timeout par sonde (en secondes, par defaut 2).
- Nombre de sondes paralleles autorisees.

## Sorties

- Resultats de chaque sonde (actif / inactif / timeout).
- Latence totale du boot des sondes.
- Code retour 0 si toutes les sondes ont reussi, 1 si echec partiel, 2 si echec total.

## Regles Operationnelles

### 1. Parallelisation des sondes
Les sondes multiples sont parallelisees (ThreadPoolExecutor, workers <= nb sondes). Le cout total est approximativement celui de la sonde la plus lente, jamais la somme.

### 2. Timeout par sonde
Chaque sonde a un timeout individuel (par defaut : 2 secondes) pour eviter le blocage indefini.

### 3. Pas de boucle sequentielle au-dela de 3 sondes
Interdit d'utiliser une boucle for sequentielle au-dela de 3 cibles. Au-dela, la parallelisation est obligatoire.

### 4. Documentation de la latence p99
L'endpoint documente sa latence p99 mesuree dans sa docstring/doc.

### 5. Journalisation
Chaque resultat de sonde est consigne avec l'endpoint, le temps de reponse et le statut.
