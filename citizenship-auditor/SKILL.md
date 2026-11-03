---
type: SKILL
version: "1.1.0"
status: active
date: "2026-08-14"
intent_hash: 0xSKILL_CITIZENSHIP_AUDITOR_20260814
citizen: L2-PLATFORM
layer: L4
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/citizenship-auditor/SKILL.md
---

# Skill - citizenship-auditor

Valider citizens.yaml <-> known_repositories.yaml <-> VERSES.

## Validations
- P-801 : Tous les repos actifs sont des citoyens declares
- P-802 : Tous les citoyens ont un verse dans VERSES/verses/
- P-803 : MOX peut consulter les plans de tous les repos citoyens
- P-804 : MOX peut creer des PRD/MOC pour tous les repos citoyens
- P-805 : Aucun gap de citoyennisation detecte par ARGUS

## Regles de validation MOX

### R-MOX-001 : Section 7 et 8 obligatoires

Tout PRD/MOC/ADR/INTENT doit contenir :
- `## 7. Implementation` avec tableau des livrables
- `## 8. Glossaire des statuts` avec la taxonomy a 8 statuts

### R-MOX-002 : Statuts autorises

Seuls les 8 statuts suivants sont autorises :
- ? Documente
- ? Implemente
- ? Teste
- ? Operationnel
- ? Actif
- ? Passif
- ?? Pending
- [KO] Bloque

### R-MOX-003 : Interdiction `[OK] FAIT`

`[OK] FAIT` est strictement interdit dans les sections `## 7. Implementation`.
Tout livrable declare avec `[OK] FAIT` doit etre remplace par un statut autorise.

### R-MOX-004 : Coherence statut/preuves

| Statut declare | Preuve requise |
|----------------|----------------|
| ? Documente | Fichier present, frontmatter valide |
| ? Implemente | Git log + build reussi (compile/test) |
| ? Teste | Tests unitaires + integration passants |
| ? Operationnel | Health-check OK, endpoint 200 |
| ? Actif | Dependants actifs verifies |
| ? Passif | Artefact present, aucun dependant actif |
| ?? Pending | Blocage governance/HITL/ADR documente |
| [KO] Bloque | Dependance manquante ou ADR refuse documente |

## Commandes
- `citizenship-auditor audit`
- `citizenship-auditor gaps`
- `citizenship-auditor report`
- `citizenship-auditor validate --path <prd_moc_path>`

## Validation MOX

L'audit de citoyennete inclut maintenant la validation des statuts MOX :
1. Verifier la presence des sections `## 7. Implementation` et `## 8. Glossaire des statuts`
2. Verifier l'absence de `[OK] FAIT`
3. Verifier que tous les livrables utilisent un statut autorise
4. Verifier la coherence statut/preuves

## Anti-patterns
- Accepter `[OK] FAIT` comme statut valide
- Omettre la section `## 8. Glossaire des statuts`
- Declarer `? Operationnel` sans health-check documente

## Reference ADR
- **ADR** : ADR-2026-08-13-001-PRD-MOC-IMPLEMENTATION-STATUS-TAXONOMY
- **IntentHash** : `0xADR_PRD_MOC_IMPLEMENTATION_STATUS_TAXONOMY_20260813`
- **Depot** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Maj requise si** : statut ADR passe a deprecated ou superseded
