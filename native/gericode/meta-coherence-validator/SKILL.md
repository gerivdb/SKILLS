---
name: meta-coherence-validator
description: "Valide la meta-coherence entre tous les PRD MOC de l'ecosysteme. Verifie que les references (designs, concepts ONTOLOGY, skills, citizens, boot sequences) sont coherentes et detecte les contradictions. Utilise comme gate BOOT-5C avant toute session multi-repo."
version: "1.0.0"
status: active
intent_hash: 0xSKILL_META_COHERENCE_VALIDATOR_20260807
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/native/gericode/meta-coherence-validator/SKILL.md
triggers:
  - "valider meta coherence PRD MOC"
  - "BOOT-5C"
  - "verifier coherence des PRD MOC"
  - "meta coherence validator"
tools:
  - read
  - grep
  - bash
citizen: "ECOSYSTEM-BRAIN"
layer: "L4"
---

# Skill - Meta Coherence Validator

> **Verdict** : **SKILL D'EXECUTION** - Validation de la coherence entre PRD MOC.

## Objectif

Verifier que tous les PRD MOC de l'ecosysteme referencent des designs, concepts,
skills, citizens et boot sequences coherents et existants. Detecter les contradictions
entre PRD MOC. Bloque l'execution si le score de coherence est inferieur a 0.8.

## Declencheur

- Boot de session multi-repo (`BOOT-5C`)
- Creation ou modification d'un PRD MOC
- Demande utilisateur "verifie la coherence des PRD MOC"

## Entrees

| Entree | Type | Description |
|--------|------|-------------|
| `prd_moc_paths` | list | Chemins des PRD MOC a valider |
| `unified_design_path` | Path | Chemin vers `unified-design/designs/` |
| `ontology_path` | Path | Chemin vers `ONTOLOGY/` |
| `skills_registry` | Path | Chemin vers `SKILLS/REGISTRY.yaml` |
| `boot_sequence_path` | Path | Chemin vers `session-boot-sequence.md` |

## Sorties

| Sortie | Type | Description |
|--------|------|-------------|
| `coherence_report` | object | Rapport de coherence global et par PRD MOC |
| `global_score` | float | Score de coherence global (0.0 a 1.0) |
| `blocked` | bool | True si score < 0.8 |

## Algorithme

### Etape 1 - Collecter les PRD MOC

- Recuperer tous les fichiers PRD MOC specifies
- Parser le frontmatter YAML de chaque fichier
- Extraire la section `## References` de chaque PRD MOC

### Etape 2 - Valider les references

Pour chaque PRD MOC, verifier chaque reference :

#### 2a. References de designs
- Verifier que le fichier `unified-design/designs/<chemin>` existe
- Signaler les designs manquants

#### 2b. References de concepts ONTOLOGY
- Verifier que le concept existe dans `ONTOLOGY/ONTOLOGY.yaml` ou `ONTOLOGY/ONTOLOGY_DECLARATION.yaml`
- Signaler les concepts manquants

#### 2c. References de skills
- Verifier que le repertoire du skill existe dans `SKILLS/`
- Verifier que le skill est declare dans `SKILLS/REGISTRY.yaml`
- Signaler les skills manquants

#### 2d. References de citizens
- Verifier que le citizen existe dans `ONTOLOGY/ONTOLOGY_DECLARATION.yaml`
- Signaler les citizens manquants

#### 2e. References de boot sequences
- Verifier que l'etape boot existe dans `session-boot-sequence.md`
- Signaler les etapes boot manquantes

#### 2f. References de PRD MOC
- Verifier que le fichier PRD MOC reference existe
- Signaler les PRD MOC manquants

#### 2g. References de ADR
- Verifier que l'ADR existe dans `GOVERNANCE-HUB/ADR/`
- Signaler les ADR manquants

#### 2h. References d'ontologie
- Verifier que le fichier YAML d'ontologie existe
- Signaler les fichiers d'ontologie manquants

### Etape 3 - Detecter les contradictions

- Comparer les definitions de meme concept across PRD MOC
- Detecter les designs references avec versions differentes
- Detecter les skills references avec chemins differents
- Detecter les boot steps referencees mais inexistantes

### Etape 4 - Calculer le score

```
score = (references_valides / total_references) - (contradictions * 0.1)
```

- Score >= 0.8 : PASS
- Score < 0.8 : BLOCKED

### Etape 5 - Generer le rapport

Generer un rapport avec :
- Score global
- Nombre de PRD MOC valides
- Nombre de contradictions detectees
- Liste des references manquantes
- Liste des references orphelines
- Liste des definitions inconstantes
- Recommandations de correction

## Format de reference canonique

Toute reference dans un PRD MOC DOIT utiliser le format :

```
[Type]:[Chemin]
```

**Types autorises** :

| Type | Format | Exemple |
|------|--------|---------|
| Design | `design:[chemin]` | `design:unified-design/designs/prd-moc-progress-sync.yaml` |
| Concept ONTOLOGY | `concept:[id]` | `concept:prd-moc-progress-sync` |
| Skill | `skill:[chemin]` | `skill:D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/native/gericode/progress-sync/` |
| Citizen | `citizen:[id]` | `citizen:ECOSYSTEM-BRAIN` |
| Boot | `boot:[step]` | `boot:BOOT-5B` |
| PRD MOC | `prd-moc:[chemin]` | `prd-moc:PRD-MOC-ACTPROTOCOL-HARNESS-ENGINEERING-2026-08-07.md` |
| ADR | `adr:[id]` | `adr:ADR-2026-08-07-M5-PRODUCTION-ONTOLOGIQUE` |
| Ontologie | `ontology:[chemin]` | `ontology:ONTOLOGY/ONTOLOGY.yaml` |

## Contraintes

- Validation **bloquante** : si score < 0.8, aucun PRD MOC ne peut etre execute
- Validation **automatique** : `BOOT-5C` invoque systematiquement
- Validation **atomique** : un seul commit par PRD MOC corrige
- Rapport stocke dans `act-protocol/reports/meta-coherence/`

## Anti-patterns

- Ne pas valider les chemins absolus vs relatifs
- Ne pas ignorer les contradictions de definition
- Ne pas accepter un score < 0.8
- Ne pas modifier les PRD MOC pendant la validation (read-only)

## Reference ADR

- **ADR** : PRD-MOC-META-COHERENCE-VALIDATION-2026-08-07.md
- **IntentHash** : 0xPRD_MOC_META_COHERENCE_VALIDATION_20260807
- **Statut ADR** : proposed
