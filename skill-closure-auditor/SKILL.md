# Skill: skill-closure-auditor

## Description
Vérifie qu'un mandat est clos selon tous ses critères d'acceptation.
Vérifie que le WAL de clôture est fourni (pas seulement décrit), que chaque
critère est marqué PROUVÉ/ATTESTÉ/DÉCRIT/ABSENT, et que les gaps sont documentés.

## Déclencheurs
- "auditer clôture", "vérifier clôture", "closure-auditor"

## Règles
- Aucun mandat ne peut être clos sans WAL de clôture JSON brut
- Chaque critère d'acceptation doit avoir un statut explicite (PROUVÉ/ATTESTÉ/DÉCRIT/ABSENT)
- Tout écart doit être documenté dans `verification_gaps`

## Invariants
- Aucun mandat ne peut être clos sans WAL de clôture JSON brut
- Aucun critère ne peut être marqué "satisfait" sans preuve correspondante

## STATUT
- version: 1.0.0
- statut: active
- type: meta-skill
- déclencheurs: ["auditer clôture", "vérifier clôture", "closure-auditor"]
- domaine: gouvernance
- phi_weight: 0.005
- assimilation_status: N/A