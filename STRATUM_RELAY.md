---
relay_version: 5
repo: gerivdb/SKILLS
strate: L6
lifecycle: ACTIVE
vague: 5
synchro: '2026-05-30'
hub: gerivdb/GOVERNANCE-HUB
intent_hash: '0x41071D70366123F8'
phi_cps:
  value: null
  source: NOT_MEASURED
  valid: false
  note: 3.697 was a mass placeholder — replaced by null
rules:
- id: R1
  assertion: MIMIR est la SOT visuelle — roadmaps et diagrammes uniquement.
  eval_cmd: null
  status: UNVERIFIED
  severity: MEDIUM
- id: R2
  assertion: BRAIN-DOCS documente BRAIN uniquement — pas d'autres repos.
  eval_cmd: null
  status: UNVERIFIED
  severity: MEDIUM
- id: R3
  assertion: SKILLS = registry tripartite natifs/assimiles/externes.
  eval_cmd: null
  status: UNVERIFIED
  severity: LOW
---

# STRATUM RELAY — SKILLS (L6)

**VAGUE**: 5 | **Synchro**: 2026-05-30 | **Hub**: gerivdb/GOVERNANCE-HUB

---

## Identite stratique

- **Strate** : `L6` — Memoire & Documentation
- **Role canonique** : SOT capacites Ã”Ã‡Ã¶ registre des skills Ã”Ã‡Ã¶ structure tripartite
- **Parent** : L5
- **Enfants** : L7
- **phi-CPS** : null (NOT_MEASURED)

## Navigation rapide

- PRD canonique : `GOVERNANCE-HUB/PRD/PRD_ECOSYSTEM_SUPERSTRUCTURE_L0-L9_V1.md`
- Substrat cognitif : `gerivdb/LLM-REPO` (L1b — prive)
- Standards repo : `REPO-STANDARDS` (RSS-v1)
- Transit map : `VERSUS/urban_ontology_verse/TRANSIT/transit_map.yaml`
- Cadastre : `VERSUS/urban_ontology_verse/CADASTRE/cadastre_full.yaml`

## Regles locales

- **R1** — MIMIR est la SOT visuelle — roadmaps et diagrammes uniquement.  [UNVERIFIED]
- **R2** — BRAIN-DOCS documente BRAIN uniquement — pas d'autres repos.  [UNVERIFIED]
- **R3** — SKILLS = registry tripartite natifs/assimiles/externes.  [UNVERIFIED]

## Karpathy-Recall etendu (Vague 5 — 10Q)

> Reponds mentalement a ces questions avant d'agir dans ce repo.

1. Q: MIMIR est decrire comme 'Wiki Atomique Diamond' — qu'est-ce que cela signifie ?
2. Q: BRAIN-DOCS documente uniquement BRAIN — ou va la doc des autres repos ?
3. Q: SKILLS contient 28 skills actifs — quelle est leur structure tripartite ?
4. Q: DOC-UNIV-DEV est une 'base de connaissances R&D' — en quoi differe-t-il de MIMIR ?
5. Q: Quel repo visualise l'architecture L0->L4.5 sous forme diagrammatique ?
6. Q: Quels repos dependent directement de L6 ?
7. Q: Quel est le role de la memoire dans l'ecosysteme gerivdb ?
8. Q: Pourquoi MIMIR ne doit pas contenir de documentation de repos individuels ?
9. Q: Quelle est la difference entre MIMIR et BRAIN-DOCS ?
10. Q: Dans quelle phase UrbanVerse le STRATUM_RELAY de ce repo a-t-il ete deploye ?

## Dependances directes

**Parents (amont) :**
- vsix-ai-orchestrator
- vscode-lm-proxy
- PLIX

**Enfants (aval) :**
- BRAIN-DOCS
- MIMIR
- DOC-UNIV-DEV

## Vague de mise a jour

| Vague | Contenu | Statut |
|-------|---------|--------|
| **5 (courante)** | Frontmatter YAML + regles structurees + phi_cps null honnete | Deploye |
| 6 (suivante) | Eval cmd sandbox + HMAC + hardware constraints | Planifie |

---

*Genere par `VERSUS/urban_ontology_verse/TOOLS/relay_propagator.py` v4.0*
*UrbanVerse v1.0.0 — gerivdb/VERSUS (L8)*
