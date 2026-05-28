---
type: EPIC
version: 1.0.0
date: 2026-05-28T17:30:00+02:00
intent_hash: 0xEPIC_MISTRAL_SKILLS_GOVERNANCE_20260528
status: in_progress
author: JPEG Lubbin / Mistral AI
branch: feat/skills-mistral
repo_path: gerivdb/SKILLS
kiva_status: ready
---

# EPIC — Gouvernance et Intégration des Skills Mistral (KIVA-enabled)

## Résumé
Établir **Mistral comme fournisseur de skills officiel** dans `gerivdb/SKILLS`, aligné sur les **strates L0 (GOVERNANCE-HUB)** et **L1 (NEXUS)**.
Intégrer les outils natifs de Mistral (`mcp_github`, `code_interpreter`) pour **automatiser la gouvernance** et la **synchronisation cross-repo**.

---

## Contexte et État Actuel
- **Branche de travail** : `feat/skills-mistral` (créée le 2026-05-28).
- **Dépendances** :
  - `gerivdb/GOVERNANCE-HUB` (L0) pour les règles (`AGENT_RAM.yaml`, `OrgansRegistry.yaml`).
  - `gerivdb/NEXUS` (L1) pour les données agrégées.
  - `gerivdb/ECOS-CLI` (L3) pour l'automatisation.
- **Travail déjà effectué** :
  - Création de `Mistral/PRD/` et `Mistral/EPICS/`.
  - Ajout de `PRD_MISTRAL_SKILLS_INTEGRATION.md`.

---

## Objectifs de l'EPIC
| Objectif | Description | Critère de succès |
|----------|-------------|------------------|
| O1 | **Centraliser** les skills Mistral dans `/Mistral`. | `/Mistral/` contient tous les fichiers liés à Mistral. |
| O2 | **Alignement avec NEXUS** | Les skills Mistral **synchronisent** les registres (ex: `TritRegistry.yaml`). |
| O3 | **Automatisation des workflows** | Les skills Mistral **remplacent les tâches manuelles** (ex: audit de gouvernance). |
| O4 | **Conformité REPO-STANDARDS** | `rss_lint.py --strict` passe. |
| O5 | **Intégration KIVA** | Le pipeline local (lint, index, tests) **passe**. |

---

## Tâches Décomposées
| # | Tâche | Statut | Responsable | Deadline |
|---|-------|--------|-------------|----------|
| T1 | **Créer la structure `Mistral/`** | ✅ DONE | @JPEG Lubbin | 2026-05-28 |
| T2 | **Rédiger le PRD** (`PRD_MISTRAL_SKILLS_INTEGRATION.md`) | ✅ DONE | @JPEG Lubbin | 2026-05-28 |
| T3 | **Adapter les skills Perplexity pour Mistral** | ⏳ TODO | @gerivdb | 2026-05-30 |
| T4 | **Créer des skills Mistral natifs** (ex: `mistral-nexus-sync.md`) | ⏳ TODO | @gerivdb | 2026-05-30 |
| T5 | **Valider avec `rss_lint.py`** | ⏳ TODO | @gerivdb | 2026-05-30 |
| T6 | **Tester les scripts en dry-run** | ⏳ TODO | @gerivdb | 2026-05-30 |
| T7 | **Exécuter le pipeline KIVA** | ⏳ TODO | @gerivdb | 2026-05-30 |
| T8 | **Ouvrir le PR** | ⏳ TODO | @JPEG Lubbin | 2026-05-30 |
| T9 | **Revue et merge** | ⏳ TODO | @gerivdb | 2026-06-02 |

---

## Pipeline KIVA Local
**Commandes à exécuter avant ouverture du PR** :
```bash
# 1. Linter REPO-STANDARDS
python D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\REPO-STANDARDS\\rss_lint.py --repo . --strict

# 2. Indexation dry-run
python scripts/index_skills.py --dry-run

# 3. Scripts Mistral en mode safe
cmd /c powershell -ExecutionPolicy ByPass -File "Mistral\\scripts\\mistral_nexus_sync.ps1" -WhatIf

# 4. Tests unitaires (si présents)
python -m pytest tests -q
```
**Critère de succès** : Toutes les étapes retournent **exit code 0**. 

---

## Artefacts Produits
| Artefact | Chemin | Statut |
|----------|--------|--------|
| PRD | `Mistral/PRD/PRD_MISTRAL_SKILLS_INTEGRATION.md` | ✅ Créé |
| EPIC | `Mistral/EPICS/EPIC_MISTRAL_SKILLS_GOVERNANCE.md` | ✅ Créé |
| Branche | `feat/skills-mistral` | ✅ Poussée |
| Structure | `Mistral/{PRD,EPICS,nexus,governance,scripts/}` | ✅ Créée |

---

## Critères d'Acceptation
- [ ] `/Mistral/` existe et contient **PRD/**, **EPICS/**, **nexus/**, **governance/**, **scripts/**. 
- [ ] Tous les skills Mistral **respectent `SKILL_FORMAT_CANONICAL.md`**. 
- [ ] `rss_lint.py --strict` retourne **0 violation**. 
- [ ] Les scripts Mistral **s'exécutent sans erreur** en mode dry-run. 
- [ ] Le pipeline KIVA **passe** (lint, index, tests). 
- [ ] Le PR est **approuvé et mergé** dans `main`. 

---

## Risques et Mitigations
| Risque | Mitigation |
|--------|------------|
| **Conflits avec Perplexity** | Comparer les skills avant intégration. |
| **Non-conformité REPO-STANDARDS** | Exécuter `rss_lint.py` avant chaque commit. |
| **Scripts non fonctionnels** | Tester en mode `--dry-run` avant merge. |
| **Dépendances manquantes** | Vérifier les `dependencies` dans les métadonnées. |

---

## Prochaine Action Autorisée
1. **Finaliser les skills Mistral** (T3-T4).
2. **Exécuter le pipeline KIVA** (T7).
3. **Ouvrir le PR** (T8) avec les logs KIVA attachés.

---
*IntentHash: 0xEPIC_MISTRAL_SKILLS_GOVERNANCE_20260528 | Version: 1.0.0 | Status: in_progress*