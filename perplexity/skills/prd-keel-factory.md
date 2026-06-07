---
name: prd-keel-factory
version: "1.0.0"
description: "Template MADR pour les PRDs KEEL. Format standard v0.6/v0.7 avec IntentHash 0xKEEL_*, sections contexte/grammaire/API/tests/estimations. Utiliser quand l'utilisateur mentionne 'rédige PRD KEEL', 'PRD parser', 'PRD KEEL', 'nouveau PRD KEEL'."
triggers:
  - "rédige PRD KEEL"
  - "PRD parser"
  - "PRD KEEL"
  - "nouveau PRD KEEL"
  - "template PRD KEEL"
layer: "L0_GOVERNANCE"
nexusTags: ["CONFORME_NEXUS", "KEEL"]
prerequisites:
  - "gerivdb/GOVERNANCE-HUB/PRD/ (template reference)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Version initiale — template MADR KEEL"}
---

# PRD-KEEL-FACTORY — Template MADR pour PRDs KEEL

## Domaine et périmètre

Ce skill définit le **format standard** pour les PRDs KEEL. Chaque PRD KEEL suit la structure MADR (Markdown Architectural Decision Record) adaptée au langage KEEL.

## Format du frontmatter

```yaml
---
type: PRD
version: "1.0"
date: YYYY-MM-DD
intent_hash: 0xKEEL_<NOM>_<VERSION>_<DATE>
status: draft
author: OPS-ENGINE
owner: gerivdb
repo: gerivdb/GOVERNANCE-HUB
nexus_tag: À_VALIDER_NEXUS
phi-CPS: "= 4.559 (ADR constitutionnel)"
do_not_create: true
strate: L1b
---
```

## Structure du PRD

### 1. Contexte et Justification
- **Problème** : Quel problème ce PRD résout-il ?
- **Objectif** : Que doit implémenter ce PRD ?
- **Lien avec l'existant** : Tableau des sources (KEEL spec, BRAIN, NEXUS, etc.)

### 2. Grammaire / Spécification
- Règles PEG (si parser)
- Syntaxe supportée
- Exemples valides et invalides

### 3. Architecture
- Structure des fichiers
- Pipeline de compilation
- API publique

### 4. Exigences fonctionnelles
- Tableau ID/Exigence/Priorité (P0-P2)

### 5. Exigences non fonctionnelles
- Tableau ID/Exigence/Cible

### 6. Critères d'acceptation
- Tableau Critère/Test

### 7. Dépendances
- Tableau Dépendance/Statut/Notes

### 8. Risques
- Tableau Risque/Probabilité/Impact/Mitigation

### 9. Roadmap d'implémentation
- Tableau Étape/Action/Durée

## IntentHash de référence

| PRD | IntentHash |
|-----|------------|
| v0.6 PEG Parser | `0xKEEL_PEG_PARSER_V06_20260607` |
| v0.7 VDB Indexation | `0xKEEL_VDB_INDEXATION_V07_20260607` |
| Roadmap v0.5-v0.7 | `0xKEEL_ROADMAP_V05_V07_20260607` |

## Intégration

- **Dépôts** : GOVERNANCE-HUB/PRD/
- **Couche EECS** : L0_GOVERNANCE
- **Skills dépendants** : keel-peg-parser, keel-vdb-tql
