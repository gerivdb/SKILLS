# Skill: skill-sequence-enforcer

## Description
Vérifie qu'un plan de séquence est respecté dans l'ordre spécifié.
Implémente le principe P14 (séquence imposée).
Refuse toute exécution hors ordre.

## Déclencheurs
- "vérifier séquence", "vérifier ordre", "sequence-enforcer"

## Règles
- Les tâches doivent être exécutées dans l'ordre déclaré
- Aucune tâche ne peut être exécutée avant ses dépendances
- Toute déviation de séquence nécessite une rectification (REF)

## Invariants
- Aucune tâche ne peut être marquée "faite" avant ses dépendances
- Aucun changement de séquence sans REF de rectification

## STATUT
- version: 1.0.0
- statut: active
- type: meta-skill
- déclencheurs: ["vérifier séquence", "vérifier ordre", "sequence-enforcer"]
- domaine: gouvernance
- phi_weight: 0.005
- assimilation_status: N/A