---
type: INTENT
status: proposed
date: "2026-07-04"
intent_hash: 0xCBM_2_SKILLS_MASTER_20260704
id: INTENT-CBM-N2-SKILLS
title: "SKILLS N+2 - Skills index"
repo: gerivdb/SKILLS
author: gerivdb
created: "2026-07-04"
---

# INTENT-CBM-N2-SKILLS - SKILLS

## Identite

- **ID** : INTENT-CBM-N2-SKILLS
- **Nom** : SKILLS CBM Master
- **Famille** : META-ROADMAP-FRACTAL
- **Strate** : N+2
- **Statut** : proposed
- **Cree** : 2026-07-04
- **Auteur** : gerivdb
- **Depend de** : INTENT-MAGISTRAL-SYSTEM-20260626, ADR-2026-07-04-001-CBM-INTEGRATION
- **Produit** : nodes CBM pour Skills index
- **Meta-outil** : pipeline-anamorphique

## Intent Hash

```yaml
intent_hash: "0xCBM_2_SKILLS_MASTER_20260704"
```

## Intention

Integrer SKILLS dans le graphe CBM en tant que N+2 - Skills index.

## Probleme resolu

A documenter.

## Modele / Architecture

```yaml
pipeline_anamorphique:
  angle: N+2 (Skills index)
  passes:
    - PASSE-1-PURIFY: "Valider structure SKILLS"
    - PASSE-2-DEDUPLICATE: "Dedoublonner SKILLS vs CBM"
    - PASSE-3-MODULARIZE: "Mapper SKILLS -> nodes CBM"
    - PASSE-4-BRIDGE-GAPS: "Creer bridge SKILLS -> CBM"
    - PASSE-5-REUSE: "Reutiliser meta-outils existants"
```

## Pipeline d'execution

```
[SKILLS]
  -> PURIFY -> DEDUPLICATE -> MODULARIZE -> BRIDGE-GAPS -> REUSE
```

## Conditions HITL

```yaml
hitl_conditions:
  auto: ["PURIFY PASS"]
  suggest: []
  block: []
```

## KEEL Conformance

```yaml
keel_gates:
  R3: "intent_hash declare : OUI"
  R5: "noms [NOM] valides ONTOLOGY : NA"
  R6: "META-LOOPs via flux_gate : NON"
  R8: "HARNESS via flux_gate : NON"
  R9: "foncteurs declares : OUI"
```

## Module cible

A definir

## Contraintes NEXUS

- Tag [CONFORME_NEXUS]
- Logs dans field-journal/

## References

- ADR-2026-07-04-001-CBM-INTEGRATION
- PRD-139-v1-pipeline-anamorphique
