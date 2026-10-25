---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xCITIZEN_WORKLOAD_DISPATCHER_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/citizen-workload-dispatcher/SKILL.md
---

# Skill: citizen-workload-dispatcher

## Purpose
Analyse une intention utilisateur et la dispatche vers le Citoyen le plus qualifie selon ses competences declarees.

## Context
Recevoir une intention (texte libre), la comparer aux domaines de responsabilite des citoyens L3 presentes dans CITIZENS.yaml, et retourner le citoyen cible ainsi que la score de correspondance.

## Inputs
- texte d'intention utilisateur
- chemin vers CITIZENS.yaml (optionnel)
- seuil de correspondance minimum (default 0.5)

## Outputs
- citoyen cible (id)
- score de confiance (0.0 a 1.0)
- liste des citoyens classes par pertinence
- statut ROUTE ou NO_MATCH

## Script
dispatch.ps1

## WAL NEXUS
- 2026-10-25 | creation skill citizen-workload-dispatcher | kilo | feat/citizen-skills-cluster-a
- routage intention -> citizen L3 | source: CITIZENS.yaml LORX | statut: active
