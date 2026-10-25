---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xCITIZEN_PERSONA_RECONCILER_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/citizen-persona-reconciler/SKILL.md
---

# Skill: citizen-persona-reconciler

## Purpose
Reconcilie le prompt systeme de l'agent (kilo.json) avec la definition de son Citoyen en L3 (CITIZENS.yaml).

## Context
Comparer le prompt systeme declare dans kilo.json (persona, ton, interdits) avec la definition du citizen L3 (role, communication_style, forbidden) et produire un rapport d'alignement avec ecarts.

## Inputs
- chemin vers kilo.json
- chemin vers CITIZENS.yaml
- identifiant du citizen

## Outputs
- statut ALIGNE ou ECARTE
- liste des ecarts (role, ton, interdits)
- prompt systeme corrige propose
- score d'alignement (0.0 a 1.0)

## Script
reconcile.ps1

## WAL NEXUS
- 2026-10-25 | creation skill citizen-persona-reconciler | kilo | feat/citizen-skills-cluster-a
- alignement prompt agent kilo.json avec definition citizen L3 | source: CITIZENS.yaml LORX | statut: active
