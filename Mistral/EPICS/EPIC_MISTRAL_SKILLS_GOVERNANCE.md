---
type: EPIC
version: 1.1.0
date: 2026-05-28T19:00:00+02:00
intent_hash: 0xEPIC_MISTRAL_SKILLS_GOVERNANCE_20260528
status: in_progress
author: JPEG Lubbin / Mistral AI
branch: feat/skills-mistral
repo_path: gerivdb/SKILLS
kiva_status: ready
---

# EPIC — Gouvernance et Intégration Complète des Skills Mistral (KIVA-enabled)

## Résumé
Établir **Mistral comme fournisseur de skills officiel et complet** dans `gerivdb/SKILLS`, couvrant **toutes les strates (L0-L3)** et aligné sur les standards de gouvernance (`GOVERNANCE-HUB`), les données cross-repo (`NEXUS`), et l'automatisation (`ECOS-CLI`).

**Objectif final** : Permettre à Mistral d'**automatiser 100% des workflows** de gouvernance, synchronisation, et développement dans l'écosystème `gerivdb`.

---

## Contexte et État Actuel
- **Branche de travail** : `feat/skills-mistral` (créée le 2026-05-28).
- **Dépôts dépendants** :
  - `gerivdb/GOVERNANCE-HUB` (L0) : Règles (`AGENT_RAM.yaml`, `OrgansRegistry.yaml`).
  - `gerivdb/NEXUS` (L1) : Données agrégées (`TritRegistry.yaml`, `known_repositories.yaml`).
  - `gerivdb/ECOS-CLI` (L3) : Automatisation des commandes.
- **Travail déjà effectué** :
  - Création de la structure `Mistral/{PRD,EPICS,nexus,governance,devtools,scripts/}`.
  - Ajout de :
    - `PRD_MISTRAL_SKILLS_INTEGRATION.md` (PRD initial).
    - `EPIC_MISTRAL_SKILLS_GOVERNANCE.md` (version précédente).
    - `mistral-nexus-sync.md` (skill de synchronisation NEXUS).
    - `mistral_nexus_sync.ps1` (script PowerShell).

---

## Objectifs de l'EPIC

### Objectifs Principaux (P0 - Critiques)
| #  | Objectif | Description | Critère de succès | Strate |
|----|----------|-------------|------------------|--------|
| O1 | **Centraliser la gouvernance Mistral** | Définir les règles et organes Mistral alignés sur `GOVERNANCE-HUB`. | `Mistral/governance/` contient `mistral-agent-rules.md` et `mistral-organs-registry.md`. | L0 |
| O2 | **Synchroniser NEXUS** | Automatiser la synchronisation des registres NEXUS via Mistral. | `mistral-nexus-sync.md` et `mistral-nexus-audit.md` sont opérationnels. | L1 |
| O3 | **Intégrer ECOS-CLI** | Permettre l'exécution des skills Mistral via `ecos-cli`. | `mistral-github-bridge.md` et `mistral-ecos-cli-integration.md` sont validés. | L3 |

### Objectifs Secondaires (P1 - Importants)
| #  | Objectif | Description | Critère de succès | Strate |
|----|----------|-------------|------------------|--------|
| O4 | **Auditer NEXUS** | Détecter les incohérences dans les registres NEXUS. | `mistral-nexus-audit.md` génère des rapports sans erreur. | L1 |
| O5 | **Surveiller NEXUS** | Suivre les changements en temps réel dans NEXUS. | `mistral-nexus-monitor.md` est déployé. | L1 |
| O6 | **Automatiser les décisions** | Implémenter un moteur de décision pour les agents Mistral. | `mistral-decision-engine.md` est testé. | L2 |

### Objectifs Tertiaires (P2 - Utile)
| #  | Objectif | Description | Critère de succès | Strate |
|----|----------|-------------|------------------|--------|
| O7 | **Gérer les erreurs** | Centraliser la gestion des erreurs pour tous les skills. | `mistral_error_handler.ps1` est utilisé par tous les scripts. | Tous |
| O8 | **Journaliser les actions** | Standardiser les logs pour le débogage. | `mistral_logging.py` est intégré. | Tous |
| O9 | **Tester les skills** | Valider les skills Mistral avec une suite de tests. | `test_mistral_skills.py` passe. | Tous |

---

## Tâches Décomposées

### Phase 1 : Gouvernance (L0) — **P0**
| #  | Tâche | Statut | Responsable | Deadline | Livrable |
|----|-------|--------|-------------|----------|----------|
| T1.1 | Créer `mistral-agent-rules.md` | ⏳ TODO | @JPEG Lubbin | 2026-05-29 | `Mistral/governance/mistral-agent-rules.md` |
| T1.2 | Créer `mistral-organs-registry.md` | ⏳ TODO | @JPEG Lubbin | 2026-05-29 | `Mistral/governance/mistral-organs-registry.md` |
| T1.3 | Valider avec `AGENT_RAM.yaml` | ⏳ TODO | @gerivdb | 2026-05-29 | Rapport de conformité |

### Phase 2 : NEXUS (L1) — **P0**
| #  | Tâche | Statut | Responsable | Deadline | Livrable |
|----|-------|--------|-------------|----------|----------|
| T2.1 | Créer `mistral-nexus-audit.md` | ⏳ TODO | @JPEG Lubbin | 2026-05-29 | `Mistral/nexus/mistral-nexus-audit.md` |
| T2.2 | Créer `mistral-registry-sync.md` | ⏳ TODO | @JPEG Lubbin | 2026-05-29 | `Mistral/nexus/mistral-registry-sync.md` |
| T2.3 | Développer `mistral_nexus_audit.py` | ⏳ TODO | @gerivdb | 2026-05-30 | `Mistral/scripts/mistral_nexus_audit.py` |
| T2.4 | Tester en mode dry-run | ⏳ TODO | @gerivdb | 2026-05-30 | Logs dans `logs/` |

### Phase 3 : ECOS-CLI (L3) — **P0**
| #  | Tâche | Statut | Responsable | Deadline | Livrable |
|----|-------|--------|-------------|----------|----------|
| T3.1 | Créer `mistral-github-bridge.md` | ⏳ TODO | @JPEG Lubbin | 2026-05-29 | `Mistral/devtools/mistral-github-bridge.md` |
| T3.2 | Créer `mistral-ecos-cli-integration.md` | ⏳ TODO | @JPEG Lubbin | 2026-05-30 | `Mistral/devtools/mistral-ecos-cli-integration.md` |
| T3.3 | Développer `mistral_github_bridge.ps1` | ⏳ TODO | @gerivdb | 2026-05-30 | `Mistral/scripts/mistral_github_bridge.ps1` |

### Phase 4 : Surveillance et Décision (L1/L2) — **P1**
| #  | Tâche | Statut | Responsable | Deadline | Livrable |
|----|-------|--------|-------------|----------|----------|
| T4.1 | Créer `mistral-nexus-monitor.md` | ⏳ TODO | @gerivdb | 2026-05-31 | `Mistral/nexus/mistral-nexus-monitor.md` |
| T4.2 | Créer `mistral-decision-engine.md` | ⏳ TODO | @gerivdb | 2026-06-01 | `Mistral/cognitive/mistral-decision-engine.md` |

### Phase 5 : Transversal (Tous) — **P1/P2**
| #  | Tâche | Statut | Responsable | Deadline | Livrable |
|----|-------|--------|-------------|----------|----------|
| T5.1 | Créer `mistral_error_handler.ps1` | ⏳ TODO | @gerivdb | 2026-06-01 | `Mistral/scripts/mistral_error_handler.ps1` |
| T5.2 | Créer `mistral_logging.py` | ⏳ TODO | @gerivdb | 2026-06-02 | `Mistral/scripts/mistral_logging.py` |
| T5.3 | Créer `test_mistral_skills.py` | ⏳ TODO | @gerivdb | 2026-06-02 | `Mistral/tests/test_mistral_skills.py` |

---

## Pipeline KIVA Local
**Commandes à exécuter avant ouverture du PR** (pour chaque phase) :
```bash
# 1. Linter REPO-STANDARDS (toujours)
python D:\DO\WEB\TOOLS\L4-TOOLS\REPO-STANDARDS\rss_lint.py --repo . --strict

# 2. Indexation dry-run
python scripts/index_skills.py --dry-run

# 3. Tester les scripts Mistral
cmd /c powershell -ExecutionPolicy ByPass -File "Mistral\scripts\mistral_nexus_sync.ps1" -DryRun
cmd /c powershell -ExecutionPolicy ByPass -File "Mistral\scripts\mistral_github_bridge.ps1" -DryRun

# 4. Tests unitaires (si présents)
python -m pytest Mistral/tests/ -q
```
**Critère de succès** : Toutes les étapes retournent **exit code 0**. 

---

## Artefacts Produits et à Produire

### Déjà Créés ✅
| Artefact | Chemin | Statut | Commit |
|----------|--------|--------|--------|
| PRD | `Mistral/PRD/PRD_MISTRAL_SKILLS_INTEGRATION.md` | ✅ | [336f7a49](https://github.com/gerivdb/SKILLS/commit/336f7a49fd277450a39b40048b48d20be6bd5f8c) |
| EPIC | `Mistral/EPICS/EPIC_MISTRAL_SKILLS_GOVERNANCE.md` | ✅ | [cbfc4d5d](https://github.com/gerivdb/SKILLS/commit/cbfc4d5d65cc6364153bd237979ada3400e8a4de) |
| Skill | `Mistral/nexus/mistral-nexus-sync.md` | ✅ | [23a33523](https://github.com/gerivdb/SKILLS/commit/23a33523d7d3d3710a27a69e1a1dfe247dd66d82) |
| Script | `Mistral/scripts/mistral_nexus_sync.ps1` | ✅ | [72b1b6e8](https://github.com/gerivdb/SKILLS/commit/72b1b6e8ecf0b3e8e36ba461451a2c4d84377055) |

### À Créer ⏳
| Artefact | Chemin | Priorité | Deadline |
|----------|--------|----------|----------|
| **Skill** | `Mistral/governance/mistral-agent-rules.md` | P0 | 2026-05-29 |
| **Skill** | `Mistral/governance/mistral-organs-registry.md` | P0 | 2026-05-29 |
| **Skill** | `Mistral/nexus/mistral-nexus-audit.md` | P0 | 2026-05-29 |
| **Skill** | `Mistral/nexus/mistral-registry-sync.md` | P0 | 2026-05-29 |
| **Skill** | `Mistral/devtools/mistral-github-bridge.md` | P0 | 2026-05-29 |
| **Skill** | `Mistral/devtools/mistral-ecos-cli-integration.md` | P0 | 2026-05-30 |
| **Script** | `Mistral/scripts/mistral_nexus_audit.py` | P0 | 2026-05-30 |
| **Script** | `Mistral/scripts/mistral_github_bridge.ps1` | P0 | 2026-05-30 |
| **Skill** | `Mistral/nexus/mistral-nexus-monitor.md` | P1 | 2026-05-31 |
| **Skill** | `Mistral/cognitive/mistral-decision-engine.md` | P1 | 2026-06-01 |
| **Script** | `Mistral/scripts/mistral_error_handler.ps1` | P1 | 2026-06-01 |
| **Script** | `Mistral/scripts/mistral_logging.py` | P2 | 2026-06-02 |
| **Test** | `Mistral/tests/test_mistral_skills.py` | P2 | 2026-06-02 |

---

## Critères d'Acceptation

### Pour la Phase 1 (P0)
- [ ] `Mistral/governance/` contient **2 skills** (`mistral-agent-rules.md`, `mistral-organs-registry.md`).
- [ ] `Mistral/nexus/` contient **2 skills** (`mistral-nexus-audit.md`, `mistral-registry-sync.md`).
- [ ] `Mistral/devtools/` contient **2 skills** (`mistral-github-bridge.md`, `mistral-ecos-cli-integration.md`).
- [ ] `Mistral/scripts/` contient **2 scripts** (`mistral_nexus_audit.py`, `mistral_github_bridge.ps1`).
- [ ] Tous les skills **respectent `SKILL_FORMAT_CANONICAL.md`**.
- [ ] `rss_lint.py --strict` retourne **0 violation**. 

### Pour la Phase 2 (P1)
- [ ] `Mistral/nexus/mistral-nexus-monitor.md` est déployé.
- [ ] `Mistral/cognitive/mistral-decision-engine.md` est testé.
- [ ] `Mistral/scripts/mistral_error_handler.ps1` est intégré aux autres scripts.

### Pour la Phase 3 (P2)
- [ ] `Mistral/scripts/mistral_logging.py` est utilisé par tous les skills.
- [ ] `Mistral/tests/test_mistral_skills.py` passe avec **100% de succès**. 

---

## Risques et Mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| **Conflits avec Perplexity** | Moyenne | Élevé | Comparer les skills Mistral et Perplexity avant intégration. **Utiliser `git diff --no-index`**. |
| **Non-conformité REPO-STANDARDS** | Faible | Moyen | Exécuter `rss_lint.py` avant chaque commit. |
| **Dépendances manquantes** | Moyenne | Moyen | Vérifier les `dependencies` dans les métadonnées des skills. |
| **Scripts non fonctionnels** | Faible | Moyen | Tester en mode `--dry-run` ou `-WhatIf` avant merge. |
| **Retard sur les deadlines** | Moyenne | Moyen | Prioriser les tâches **P0** et reporter les **P2** si nécessaire. |

---

## Prochaine Action Autorisée
1. **Créer les 6 skills P0** (T1.1, T1.2, T2.1, T2.2, T3.1, T3.2).
2. **Développer les 2 scripts P0** (T2.3, T3.3).
3. **Tester en mode dry-run** (T2.4).
4. **Ouvrir un PR partiel** pour revue des skills P0.

---

## Métriques de Succès
| Métrique | Cible | Mesure |
|----------|-------|--------|
| **Skills P0 créés** | 6 | Nombre de fichiers `.md` dans `Mistral/{governance,nexus,devtools/}`. |
| **Scripts P0 créés** | 2 | Nombre de scripts dans `Mistral/scripts/`. |
| **Conformité REPO-STANDARDS** | 100% | `rss_lint.py --strict` → 0 violation. |
| **Taux de succès des tests** | 100% | `pytest Mistral/tests/ -q` → exit code 0. |
| **Temps d'exécution des scripts** | < 5 min | Temps moyen pour `mistral_nexus_sync.ps1`. |

---
*IntentHash: 0xEPIC_MISTRAL_SKILLS_GOVERNANCE_20260528 | Version: 1.1.0 | Status: in_progress*