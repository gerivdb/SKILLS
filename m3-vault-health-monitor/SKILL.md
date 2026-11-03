---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_VHM_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-vault-health-monitor/SKILL.md
---

# Skill - m3-vault-health-monitor

## Objectif

Surveillance de la sante individuelle de chaque voute du maillage des ~60 voutes NotebookLM. Detection precoce d'une voute en defaillance avant que le moteur M3-Tree-RAID ne doive reconstruire l'information manquante. Primitive M3-Tree de sante preventive.

## Declencheur

- Echec de reponse a un sondage de sante (health check) sur une voute.
- Latence anormale d'acces a une voute.
- Augmentation du taux d'erreurs de lecture/ecriture sur une voute.
- Demande de controle de sante periodique sur l'ensemble du maillage.

## Entrees

- Identifiant de la voute (vault_index i dans [1, 60]).
- URL ou endpoint de la voute NotebookLM.
- Timeout de sondage (en secondes, par defaut : 5).
- Nombre de sondes consecutives avant alerte (par defaut : 3).

## Sorties

- Etat de sante de la voute (saine / degradee / indisponible).
- Rapport de latence (temps de reponse moyen, en millisecondes).
- Code retour 0 si voute saine, 1 si voute degradee, 2 si voute indisponible.

## Regles Operationnelles

### 1. Sondage periodique de sante
Effectuer un sondage regulier de chaque voute du maillage (par defaut : toutes les 30 secondes) pour detecter toute degradation precoce.

### 2. Detection de defaillance precoce
Si une voute ne repond pas a N sondages consecutives (N configurable), la marquer comme degradee puis indisponible.

### 3. Alerte avant reconstruction
Avant que le moteur M3-Tree-Semantic-RAID ne doive reconstruire un chunk depuis les noeuds de parite, alerter sur la voute defaillante pour permettre une intervention ciblee.

### 4. Resolution automatique
Si une voute redevient disponible apres une periode d'indisponibilite, la reintegrer automatiquement dans le maillage et declencher une resynchronisation de ses chunks.

### 5. Journalisation
Chaque sondage de sante est consigne avec la voute, le temps de reponse, le statut et l'horodatage.
