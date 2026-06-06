---
type: prd
version: 1.0
status: draft
date: 2026-06-07
author: HITL (Perplexity / ENV1)
owner: gerivdb
repo: SKILLS
nexus_tag: À_VALIDER_NEXUS
φ-CPS: "= 4.559 (ADR constitutionnel)"
do_not_delete: true
strate: L2-L3
intent_hash: 0xSKILLS_UAE_KEEL_METAMORPHIC_V1_20260607

supersedes: null

repos_impliqués:
  - gerivdb/SKILLS
  - gerivdb/UAE
  - gerivdb/KEEL
  - gerivdb/GOVERNANCE-HUB
  - gerivdb/BRAIN
  - gerivdb/NEXUS

souveraine_refs:
  - PRD_METACLUSTER_CHESSBOARD_COORDINATE_SYSTEM_V3.md
  - PRD_SKILLS_AGENTIC_RAG.md
  - TAXONOMY.md (v1.0.0 — supercédé par ce PRD)
---

# PRD — SKILLS UAE+KEEL METAMORPHIC v1
## Restructuration taxonomique du repo SKILLS via coordonnées UAE et foncteurs KEEL

---

## CHANGELOG

| Version | Date | Auteur | Description |
|---|---|---|---|
| 1.0 | 2026-06-07 | HITL (Perplexity) | Initial draft |

---

## 1. PROBLÈME FORMEL

### 1.1 État actuel
Le repo SKILLS organise ses 64 skills par **agent consommateur** (`perplexity/`, `Mistral/`, `native/`, `cognitive/`) plutot que par domaine fonctionnel. La taxonomie (`TAXONOMY.md`) est un document statique non interopérable avec UAE ou KEEL.

Conséquences :
- Le DELEGATOR (Agent 0 de `skills-agentic v2`) ne peut pas router dynamiquement sans règles codées en dur
- Aucune métrique de distance inter-skills (UAE)
- Aucun graphe de dépendances composables (KEEL)
- Ajout d'un skill = mise à jour manuelle de MANIFEST.json + REGISTRY.yaml

### 1.2 État cible
Chaque skill possède **5 coordonnées UAE** (strate / domaine / env / phase / urgence) et des **foncteurs KEEL** vers ses dépendances. Le MANIFEST est généré automatiquement. Le DELEGATOR route via UAE score sans règles en dur.

---

## 2. SOURCES DE VÉRITÉ

| Source | Rôle dans ce PRD |
|---|---|
| `PRD_METACLUSTER_CHESSBOARD_COORDINATE_SYSTEM_V3.md` | Définit les 5 axes UAE et l’encodage pentaédique |
| `PRD_SKILLS_AGENTIC_RAG.md` | Définit le DELEGATOR et les 9 agents consommateurs |
| `TAXONOMY.md` v1.0.0 | Taxonomie actuelle — supercédée par `TAXONOMY/domains.yaml` |
| `gerivdb/UAE` | Scoring scalaire 1/√d et zones LADYBIRD-243 |
| `gerivdb/KEEL` | Foncteurs, adjonctions, coût énergétique Branch⊣Merge |

---

## 3. ARCHITECTURE CIBLE

### 3.1 Structure de répertoires

```
SKILLS/
├── TAXONOMY/
│   ├── domains.yaml       ← arbre des domaines fonctionnels
│   ├── coords.yaml        ← coordonnées UAE de chaque skill
│   └── graph.yaml         ← foncteurs KEEL (adjacences)
├── skills/
│   ├── L0-governance/
│   ├── L1-sot/
│   ├── L2-cognition/
│   ├── L3-automation/
│   ├── L3-git/
│   └── Lx-agentic/
├── agents/                ← adaptateurs par consommateur (wrappers)
│   ├── perplexity/
│   ├── kilo/
│   └── mistral/
└── MANIFEST.json          ← généré depuis coords.yaml (plus manuel)
```

### 3.2 Coordonnées UAE d’un skill (format canonique)

```yaml
# TAXONOMY/coords.yaml
skills:
  git-lock-resolver:
    strate:   L3
    domaine:  automation
    env:      ENV2
    phase:    fix
    urgence:  P1
    uae_score: 87        # 1/√d depuis le centre du plateau
    zone:     LADYBIRD   # zone UAE (score ≥ 80)

  prd-frontmatter-validator:
    strate:   L0
    domaine:  governance
    env:      ENV1
    phase:    audit
    urgence:  P2
    uae_score: 62
    zone:     STANDARD
```

### 3.3 Foncteurs KEEL entre skills

```yaml
# TAXONOMY/graph.yaml
adjunctions:
  git-workflow-automator:
    adjoints:
      - skill: git-lock-resolver
        condition: "conflict_type == lock_file"
        cost: 0.1        # coût énergétique KEEL
      - skill: contextual-stash-manager
        condition: "unstaged_changes == true"
        cost: 0.2

  prd-frontmatter-validator:
    adjoints:
      - skill: governance-doc-writer
        condition: "invalid_fields > 0"
        cost: 0.3
```

### 3.4 Applications métamorphiques

Un skill métamorphique se reconfigure selon ses coordonnées UAE d’entrée :

```
auto-responder(input_coord) →

  si {strate:L3, phase:fix, env:ENV2} :
    instancie git-lock-resolver + git-workflow-automator

  si {strate:L0, phase:audit, env:ENV1} :
    instancie prd-frontmatter-validator + frontmatter-guardian

  si {strate:L2, phase:create, env:*} :
    instancie governance-doc-writer + skills-rewriter
```

Formellement : `metamorph(s, c) = π₀(KEEL.adjoint(UAE.nearest(c)))`
où `c` est le vecteur de coordonnées, `π₀` est la projection sur le skill racine.

---

## 4. AXES UAE APPLIQUÉS AUX SKILLS

| Axe | Valeurs possibles | Description |
|---|---|---|
| strate | L0, L1, L2, L3, L4… | Strate écosystème (L0=gouvernance, L3=automation) |
| domaine | governance, sot, cognition, automation, git, agentic, domain, external | Domaine fonctionnel |
| env | ENV1, ENV2, BOTH | Environnement cible |
| phase | create, audit, fix, close, route | Phase du cycle de vie |
| urgence | P0, P1, P2, P3 | Priorité opérationnelle |

---

## 5. MIGRATION TAXONOMY v1 → v2

| Étape | Action | Outil |
|---|---|---|
| 1 | Générer `TAXONOMY/coords.yaml` depuis MANIFEST.json existant | script Python |
| 2 | Migrer `perplexity/skills/` → `skills/L3-automation/` etc. | script Python |
| 3 | Créer `TAXONOMY/graph.yaml` — foncteurs KEEL manuels d’abord | HITL |
| 4 | Mettre à jour MANIFEST.json — générateur depuis coords.yaml | script Python |
| 5 | Créer skill `skill-router` — DELEGATOR navigue via UAE+KEEL | HITL + Kilo |
| 6 | Archiver `TAXONOMY.md` v1.0.0, créer `TAXONOMY/domains.yaml` | HITL |

**Aucune rupture de compatibilité** : les wrappers `agents/perplexity/` maintiennent les anciens chemins pendant la migration.

---

## 6. INTÉGRATION AVEC PRDs ADJACENTS

| PRD | Relation |
|---|---|
| `PRD_METACLUSTER_CHESSBOARD_COORDINATE_SYSTEM_V3.md` | **Source** des 5 axes UAE et de l’encodage 3⁵=243 |
| `PRD_SKILLS_AGENTIC_RAG.md` | **Consommateur** — DELEGATOR route via UAE score |
| `PRD-03-COGNITION-SOUVERAINE.md` | BRAIN fournit les modèles de raisonnement aux skills L2 |
| `PRD-07-MULTIREPOS-AGENTIQUE.md` | Le graphe KEEL traverse les repos (cross-repo adjacences) |
| `PRD-06-TRIADE-VIGILANCE.md` | IRIS consomme les skills phase:audit pour la détection DRIFT |

---

## 7. LIVRAISONS PRIORITAIRES

| Livrable | Repo | Priorité | Aspect |
|---|---|---|---|
| `scripts/generate_coords.py` | SKILLS | P1 | UAE — génère coords.yaml depuis MANIFEST |
| `TAXONOMY/coords.yaml` | SKILLS | P1 | UAE — 64 skills coordés |
| `TAXONOMY/graph.yaml` | SKILLS | P1 | KEEL — foncteurs inter-skills |
| `skill-router` skill | SKILLS | P1 | Agentic — routing UAE dynamique |
| `scripts/generate_manifest.py` | SKILLS | P2 | Automation — MANIFEST depuis coords |
| Migration `perplexity/` → `skills/L*/` | SKILLS | P2 | Restructuration |
| `agents/perplexity/` wrappers compat | SKILLS | P2 | Compatibilité ascendante |

---

## 8. CRITÈRES D’ACCEPTATION

| Critère | Test |
|---|---|
| Chaque skill a 5 coordonnées UAE valides | `validate_coords.py --strict` → 0 erreur |
| MANIFEST.json généré sans intervention manuelle | `generate_manifest.py` idempotent |
| DELEGATOR route via UAE sans règles codées en dur | test agentic : 10 requêtes, 10 routages corrects |
| Foncteurs KEEL valides (pas de cycle) | `validate_graph.py --acyclic` → 0 cycle détecté |
| Zéro rupture des wrappers `agents/perplexity/` | régression : 30 requêtes skills-agentic-test.md → 100% |
| φ-CPS ≥ 4.559 maintenu | calcul post-migration |
