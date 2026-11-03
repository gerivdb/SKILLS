---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_LB_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-load-balancer/SKILL.md
---

# Skill - m3-load-balancer

## Objectif

Repartition de charge des requetes entre les 60 voutes NotebookLM du maillage M3-Tree. Certaines voutes peuvent etre sur-sollicitees tandis que d'autres sont sous-utilisees. Primitive M3-Tree d'equilibrage de charge.

## Declencheur

- Une voute recoit un nombre disproportionne de requetes.
- Latence anormale sur une voute surchargee.
- Demande de reequilibrage de charge sur le maillage.
- Detection d'une voute sous-utilisee pouvant absorber du trafic.

## Entrees

- Liste des 60 voutes avec leur charge actuelle (requetes par seconde).
- Requete entrante a router.
- Capacite maximale de chaque voute (requetes par seconde).
- Strategie de repartition (round-robin / moins-charge / pondere).

## Sorties

- Voute selectionnee pour traiter la requete.
- Rapport de charge avant/apres affectation.
- Code retour 0 si routage reussi, 1 si toutes les voutes sont saturees.

## Regles Operationnelles

### 1. Repartition dynamique
Repartir les requetes entrantes sur les voutes en fonction de leur charge actuelle, pas de maniere statique.

### 2. Strategie moins-charge
Privilegier la voute ayant le moins de requetes actives pour chaque nouvelle requete.

### 3. Detection de saturation
Si une voute atteint sa capacite maximale, la retirer temporairement du pool de routage jusqu'a ce que sa charge redescende.

### 4. Reequilibrage periodique
Reevaluer periodiquement la distribution de charge et deplacer certaines requetes programmees vers des voutes moins chargees.

### 5. Journalisation
Chaque affectation de requete est consignee avec la voute selectionnee, sa charge avant/affectation et l'horodatage.
