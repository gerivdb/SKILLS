---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xCITIZEN_CREDENTIAL_ATTESTOR_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/citizen-credential-attestor/SKILL.md
---

# Skill: citizen-credential-attestor

## Purpose
Verifie que le Citoyen appelant dispose des droits cryptographiques (signature GPG, tokens BDCP) avant autorisation d'action.

## Context
Avant toute operation sensible, ce skill L4-TOOLS atteste l'identite cryptographique du citizen appelant : cle GPG publique, token BDCP valide, et statut de habilitation.

## Inputs
- identifiant du citizen
- chemin vers le magasin de credentials (optionnel)
- type de preuve requise (gpg|bdcp|both)

## Outputs
- statut ATTESTE ou REVOKE
- empreinte GPG validee (si applicable)
- statut token BDCP (valide/expire/absent)
- horodatage de l'attestation

## Script
attest.ps1

## WAL NEXUS
- 2026-10-25 | creation skill citizen-credential-attestor | kilo | feat/citizen-skills-cluster-a
- verification credentials GPG + BDCP citizen | source: CITIZENS.yaml LORX | statut: active
