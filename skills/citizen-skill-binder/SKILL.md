---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xCITIZEN_SKILL_BINDER_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/citizen-skill-binder/SKILL.md
---

# Skill: citizen-skill-binder

## Purpose
Liaison formelle d'un Citoyen L3 a un trousseau de Skills autorises (RBAC agentique) selon son mandat dans CITIZENS.yaml.

## Context
L3-CITIZENS definit les citoyens et leurs mandats (roles, responsabilites, goals). Ce skill L4-TOOLS lie un citizen a un ensemble de skills L4 dont il est habilite a invoquer, via une matrice RBAC derivee de son mandat.

## Inputs
- chemin vers CITIZENS.yaml (default: D:\DO\WEB\TOOLS\L3-CITIZENS\LORX\citizens.yaml)
- identifiant du citizen cible (ex: LORX)
- identifiant du skill a verifier (optionnel)

## Outputs
- rapport de liaison citizen <-> skills autorises
- statut OK/REJETE pour chaque skill demande
- liste des skills manquantes si le mandat ne couvre pas la demande

## Script
bind.ps1

## WAL NEXUS
- 2026-10-25 | creation skill citizen-skill-binder | kilo | feat/citizen-skills-cluster-a
- liaison RBAC citizen L3 -> skills L4 | source: CITIZENS.yaml LORX | statut: active
