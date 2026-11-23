---
type: STD
status: proposed
date: "2026-11-23"
intent_hash: 0xSTD_M3_TREE_ADR_SKILLS_20261123
repo: SKILLS
stratum: L4-TOOLS
topos_node: L4-TOOLS
---

# M3 TREE ADR — Dépôt SKILLS (L4-TOOLS)

## Objectif
Indexer tous les ADR du dépôt SKILLS dans une structure arborescente topologique (M3 TREE) à 5 niveaux, permettant de détecter les contradictions, dépendances et conflits entre ADR avant validation.

TOPOS (L1-INFRA) est la cartographie de référence. Ce M3 TREE s'appuie sur TOPOS comme fondement topologique et ne crée pas de carte parallèle.

## Structure topologique

```
M3 TREE ADR — SKILLS (L4-TOOLS)
│
├─ NIVEAU 1 — REPO : SKILLS
│  └─ Strate : L4-TOOLS
│  └─ Nœud TOPOS : L4-TOOLS / SKILLS
│
├─ NIVEAU 2 — STRATE : L4-TOOLS
│  └─ Dépendance : GOVERNANCE-HUB (L0-CANON, SOT known_repositories.yaml)
│
├─ NIVEAU 3 — ÉCOSYSTÈME LOCAL (ENV2 global)
│  └─ M3-BRANCH central : GOVERNANCE-HUB
│
├─ NIVEAU 4 — MULTI ENV2-ENV3 (hybride ENV2 ↔ ENV3)
│  └─ Aucun ADR transverse identifié à ce stade
│
└─ NIVEAU 5 — MULTI-ENV (ENV6 et autres ENV)
   └─ Aucun ADR transverse identifié à ce stade

## Index des ADR (niveau 1 — dépôt SKILLS)

| ID | Fichier | Titre | Statut | Date | IntentHash | Dépendances | Conflits |
|----|---------|-------|--------|------|------------|-------------|----------|
| ADR-001 | ADR-001-lazy-skill-menu.md | Lazy Loading du Skill Menu via menu.yaml | proposed | 2026-06-27 | 0xSKILLS_MANIFEST_LAZY_LOAD_20260627 | À auditer | Aucun |
| ADR-CBM-SKILLS-BRIDGE-GAPS | ADR-CBM-SKILLS-BRIDGE-GAPS.md | INTENT-CBM-N2-SKILLS - BRIDGE-GAPS | proposed | 2026-07-04 | 0xADR_CBM_SKILLS_BRIDGE-GAPS_20260704 | INTENT-CBM-N2-SKILLS | Aucun |
| ADR-CBM-SKILLS-DEDUPLICATE | ADR-CBM-SKILLS-DEDUPLICATE.md | INTENT-CBM-N2-SKILLS - DEDUPLICATE | proposed | 2026-07-04 | 0xADR_CBM_SKILLS_DEDUPLICATE_20260704 | INTENT-CBM-N2-SKILLS | Aucun |
| ADR-CBM-SKILLS-MODULARIZE | ADR-CBM-SKILLS-MODULARIZE.md | INTENT-CBM-N2-SKILLS - MODULARIZE | proposed | 2026-07-04 | 0xADR_CBM_SKILLS_MODULARIZE_20260704 | INTENT-CBM-N2-SKILLS | Aucun |
| ADR-CBM-SKILLS-PURIFY | ADR-CBM-SKILLS-PURIFY.md | INTENT-CBM-N2-SKILLS - PURIFY | proposed | 2026-07-04 | 0xADR_CBM_SKILLS_PURIFY_20260704 | INTENT-CBM-N2-SKILLS | Aucun |
| ADR-CBM-SKILLS-REUSE | ADR-CBM-SKILLS-REUSE.md | INTENT-CBM-N2-SKILLS - REUSE | proposed | 2026-07-04 | 0xADR_CBM_SKILLS_REUSE_20260704 | INTENT-CBM-N2-SKILLS | Aucun |
| ADR-002 | ADR-002-*.md | À auditer | À auditer | À auditer | À auditer | À auditer | Aucun |
| ADR-003 | ADR-003-*.md | À auditer | À auditer | À auditer | À auditer | À auditer | Aucun |
| ADR-004 | ADR-004-*.md | À auditer | À auditer | À auditer | À auditer | À auditer | Aucun |
| ADR-005 | ADR-005-*.md | À auditer | À auditer | À auditer | À auditer | À auditer | Aucun |

## Règles de cohérence (gardiens CHECK / G-PROOF)

1. **Fibrosité** : tout ADR doit être rattaché à un nœud TOPOS. SKILLS est indexé sous L4-TOOLS.
2. **Pas de doublon d'intent_hash** : avant création d'un nouvel ADR dans SKILLS, vérifier qu'aucun ADR des autres dépôts ne couvre le même intent_hash.
3. **Statut de propagation** : un ADR `accepted` dans GOVERNANCE-HUB (niveau 3) s'impose à SKILLS (niveau 1, strate L4-TOOLS) en cas de conflit.
4. **Vérification pré-commit** : tout nouveau ADR dans SKILLS doit être indexé dans ce M3 TREE avant commit.

## Statut
proposed — en attente de validation HITL architecte

## Référence
- **STD** : STD-M3-TREE-ADR-REPO (REPO-STANDARDS/standards/, accepté `d03f735`)
- **ADR** : ADR-M3-TREE-ADR-COHERENCE (GOVERNANCE-HUB/ADR/, accepté `f6e71055`)
- **Dépôt** : SKILLS (L4-TOOLS) / ADR/
- **IntentHash** : 0xSTD_M3_TREE_ADR_SKILLS_20261123
