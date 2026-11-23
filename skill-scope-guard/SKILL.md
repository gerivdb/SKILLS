# Skill: skill-scope-guard

## Description
Vérifie qu'un livrable respecte le périmètre écrit du mandat.
Refuse tout ajout de fonctionnalité non listé dans le périmètre initial.
Implémente le principe P7 (périmètre verrouillé).

## Déclencheurs
- "vérifier périmètre", "vérifier scope", "scope-guard"

## Règles
- Tout fichier ajouté hors périmètre déclaré est refusé
- Tout champ WAL hors périmètre est rejeté
- Tout changement de périmètre nécessite un REF de rectification

## Invariants
- Aucun fichier ne peut être ajouté sans être listé dans le périmètre écrit
- Aucun WAL ne peut contenir un champ hors périmètre sans REF de rectification

## STATUT
- version: 1.0.0
- statut: active
- type: meta-skill
- déclencheurs: ["vérifier périmètre", "vérifier scope", "scope-guard"]
- domaine: gouvernance
- phi_weight: 0.005
- assimilation_status: N/A