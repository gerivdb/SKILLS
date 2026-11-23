# Skill: skill-rectification-writer

## Description
Écrit un REF de rectification (ADR de correction) lorsqu'une erreur factuelle
est détectée dans un document, un WAL ou un commit précédent.
Implémente le principe P10 (ordre des consignations : REF avant commit).

## Déclencheurs
- "rectifier ADR", "corriger erreur", "rectification-writer"

## Règles
- Un REF de rectification doit précéder tout commit qui modifie un document erroné
- Le REF doit citer l'erreur factuelle et la décision (inchangée ou corrigée)
- Aucun nouveau commit ne peut modifier un document erroné sans REF préalable

## Invariants
- Aucun commit ne modifie un document erroné sans REF de rectification préalable
- Un REF de rectification ne peut pas être appliqué rétroactivement à un commit déjà fait

## STATUT
- version: 1.0.0
- statut: active
- type: meta-skill
- déclencheurs: ["rectifier ADR", "corriger erreur", "rectification-writer"]
- domaine: gouvernance
- phi_weight: 0.005
- assimilation_status: N/A