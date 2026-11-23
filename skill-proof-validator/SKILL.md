# Skill: skill-proof-validator

## Description
Vérifie qu'une affirmation (claim) est accompagnée d'artefacts bruts vérifiables.
Implémente le principe P2 (trois niveaux de preuve) et P1 (zéro fausse fin).

## Déclencheurs
- "valider preuve", "vérifier preuve", "proof-validator", "artefact brut"

## Règles
- Un claim sans artefact brut (JSON, log, sortie console, git show) est classé `DÉCRIT`, pas `PROUVÉ`
- Un claim avec artefact brut mais sans recoupement est `ATTESTÉ`
- Un claim avec artefact brut + recoupement indépendant est `PROUVÉ`

## Invariants
- Aucun fichier ne peut être marqué `PROUVÉ` sans son artefact brut associé
- Le WAL de clôture ne peut pas référencer des artefacts non fournis

## STATUT
- version: 1.0.0
- statut: active
- type: meta-skill
- déclencheurs: ["valider preuve", "vérifier preuve", "proof-validator"]
- domaine: gouvernance
- phi_weight: 0.005
- statut_assimilation: N/A