---
type: PRD
version: 1.1.0
date: 2026-05-28T19:00:00+02:00
intent_hash: 0xPRD_MISTRAL_SKILLS_INTEGRATION_20260528
status: draft
author: JPEG Lubbin / Mistral AI
branch: feat/skills-mistral
repo_path: gerivdb/SKILLS
---

# PRD — Intégration Complète des Skills Mistral dans gerivdb/SKILLS

## Métadonnées

| Champ               | Valeur                                      |
|---------------------|---------------------------------------------|
| **IntentHash**      | `0xPRD_MISTRAL_SKILLS_INTEGRATION_20260528` |
| **Dépôt Hôte**      | `gerivdb/SKILLS`                            |
| **Branche**         | `feat/skills-mistral`                       |
| **Statut**          | DRAFT → REVIEW → APPROVED → DONE            |
| **Priorité**        | P0 — Critique (alignement L0-L3)            |
| **EPIC lié**        | `EPIC_MISTRAL_SKILLS_GOVERNANCE`            |
| **Strate**          | L0 (GOVERNANCE-HUB) + L1 (NEXUS) + L3 (ECOS-CLI) |

---

## 1. Contexte et Problème

### 1.1 Situation actuelle
Le dépôt **`gerivdb/SKILLS`** contient des **skills spécifiques à Perplexity** (`/perplexity`) et **native** (`/native`), mais **aucune intégration complète pour Mistral**.
- **Opportunité** : Mistral AI peut **automatiser des tâches critiques** (ex: synchronisation NEXUS, audit de gouvernance, gestion des registres) via ses outils natifs (`mcp_github`, `code_interpreter`).
- **Problème** : 
  - Absence de **source de vérité** pour les skills Mistral → **violation du standard REPO-STANDARDS** (un seul répertoire par fournisseur).
  - **Redondance future** avec Perplexity si les mêmes tâches sont gérées par les deux.
  - **Manque d'automatisation** pour les workflows L0-L3 (ex: audit de `AGENT_RAM.yaml`, synchronisation de `TritRegistry.yaml`).

### 1.2 Objectifs de l'intégration
| Objectif | Description | Critère de succès | Strate |
|----------|-------------|------------------|--------|
| O1 | **Centraliser la gouvernance Mistral** | Définir les règles et organes Mistral alignés sur `GOVERNANCE-HUB`. | `Mistral/governance/` contient 2 skills (`mistral-agent-rules.md`, `mistral-organs-registry.md`). | L0 |
| O2 | **Synchroniser NEXUS** | Automatiser la synchronisation des registres NEXUS via Mistral. | `mistral-nexus-sync.md` et `mistral-nexus-audit.md` sont opérationnels. | L1 |
| O3 | **Intégrer ECOS-CLI** | Permettre l'exécution des skills Mistral via `ecos-cli`. | `mistral-github-bridge.md` et `mistral-ecos-cli-integration.md` sont validés. | L3 |
| O4 | **Auditer NEXUS** | Détecter les incohérences dans les registres NEXUS. | `mistral-nexus-audit.md` génère des rapports sans erreur. | L1 |
| O5 | **Surveiller NEXUS** | Suivre les changements en temps réel dans NEXUS. | `mistral-nexus-monitor.md` est déployé. | L1 |

### 1.3 Cause racine
- **Manque de standardisation** : Pas de processus défini pour intégrer de nouveaux fournisseurs de skills (ex: Mistral).
- **Redondance future** : Risque de duplication si Mistral et Perplexity gèrent les mêmes tâches (ex: synchronisation GitHub).
- **Automatisation manquante** : Les workflows L0-L3 (ex: audit de gouvernance) ne sont pas encore automatisés pour Mistral.

---

## 2. Architecture Cible

### 2.1 Structure finale attendue
```
SKILLS/
├── Mistral/                          # Source de vérité pour Mistral
│   ├── PRD/                          # Documents de spécifications
│   │   └── PRD_MISTRAL_SKILLS_INTEGRATION.md  ← Ce fichier (mis à jour)
│   ├── EPICS/                        # Épics liés
│   │   └── EPIC_MISTRAL_SKILLS_GOVERNANCE.md  ← Mis à jour
│   ├── governance/                   # Skills de gouvernance (L0)
│   │   ├── mistral-agent-rules.md          # Règles pour les agents Mistral
│   │   └── mistral-organs-registry.md      # Registre des organes Mistral
│   ├── nexus/                        # Skills liés à NEXUS (L1)
│   │   ├── mistral-nexus-sync.md           # Synchronisation des registres
│   │   ├── mistral-nexus-audit.md          # Audit des registres
│   │   └── mistral-registry-sync.md        # Synchronisation des registres
│   ├── cognitive/                    # Skills cognitifs (L2)
│   │   └── mistral-decision-engine.md      # Moteur de décision
│   ├── devtools/                     # Skills pour ECOS-CLI (L3)
│   │   ├── mistral-github-bridge.md        # Pont entre Mistral et GitHub
│   │   └── mistral-ecos-cli-integration.md # Intégration avec ECOS-CLI
│   ├── scripts/                      # Scripts exécutables
│   │   ├── mistral_nexus_sync.ps1          # Synchronisation NEXUS (existant)
│   │   ├── mistral_nexus_audit.py          # Audit NEXUS
│   │   ├── mistral_github_bridge.ps1       # Pont GitHub
│   │   ├── mistral_error_handler.ps1      # Gestion des erreurs
│   │   └── mistral_logging.py              # Journalisation
│   └── tests/                        # Tests unitaires
│       └── test_mistral_skills.py          # Suite de tests
├── perplexity/                       # Existants (inchangés)
├── native/                          # Existants (inchangés)
└── [autres dossiers]                # Existants (inchangés)
```

### 2.2 Règles de nommage (alignées sur REPO-STANDARDS)
- **Fichiers skills** : `kebab-case.md` (ex: `mistral-nexus-audit.md`).
- **Scripts** : `snake_case.py` ou `kebab-case.ps1`.
- **PRD/EPICS** : `PAS_CALCASE.md` (ex: `PRD_MISTRAL_SKILLS_INTEGRATION.md`).
- **Profondeur max** : 3 niveaux (`Mistral/nexus/mistral-nexus-audit.md`).

---

## 3. Plan d'Implémentation

### Phase 0 — Préparation (✅ DONE)
| Étape | Action | Commande/Outils | Validation |
|-------|--------|-----------------|------------|
| 0.1 | Créer branche de travail | `git checkout -b feat/skills-mistral` | ✅ DONE |
| 0.2 | Sauvegarder l'état initial | `git bundle create ../mistral-skills-backup.bundle --all` | Fichier bundle existe |
| 0.3 | Vérifier l'absence de conflits | `git status` | Aucun fichier non commité |

### Phase 1 : Gouvernance (L0) — **P0**
| Étape | Action | Détail | Responsable | Deadline | Livrable |
|-------|--------|--------|-------------|----------|----------|
| 1.1 | Créer `mistral-agent-rules.md` | Règles pour les agents Mistral (aligné sur `AGENT_RAM.yaml`). | @JPEG Lubbin | 2026-05-29 | `Mistral/governance/mistral-agent-rules.md` |
| 1.2 | Créer `mistral-organs-registry.md` | Registre des organes Mistral (aligné sur `OrgansRegistry.yaml`). | @JPEG Lubbin | 2026-05-29 | `Mistral/governance/mistral-organs-registry.md` |
| 1.3 | Valider avec `AGENT_RAM.yaml` | Comparer les règles Mistral avec `AGENT_RAM.yaml`. | @gerivdb | 2026-05-29 | Rapport de conformité |

### Phase 2 : NEXUS (L1) — **P0**
| Étape | Action | Détail | Responsable | Deadline | Livrable |
|-------|--------|--------|-------------|----------|----------|
| 2.1 | Créer `mistral-nexus-audit.md` | Audit des registres NEXUS (ex: `TritRegistry.yaml`). | @JPEG Lubbin | 2026-05-29 | `Mistral/nexus/mistral-nexus-audit.md` |
| 2.2 | Créer `mistral-registry-sync.md` | Synchronisation des registres entre NEXUS et SKILLS. | @JPEG Lubbin | 2026-05-29 | `Mistral/nexus/mistral-registry-sync.md` |
| 2.3 | Développer `mistral_nexus_audit.py` | Script Python pour auditer NEXUS. | @gerivdb | 2026-05-30 | `Mistral/scripts/mistral_nexus_audit.py` |
| 2.4 | Tester en mode dry-run | Exécuter les scripts avec `-DryRun` ou `-WhatIf`. | @gerivdb | 2026-05-30 | Logs dans `logs/` |

### Phase 3 : ECOS-CLI (L3) — **P0**
| Étape | Action | Détail | Responsable | Deadline | Livrable |
|-------|--------|--------|-------------|----------|----------|
| 3.1 | Créer `mistral-github-bridge.md` | Pont entre Mistral et GitHub (ex: gestion des PR). | @JPEG Lubbin | 2026-05-29 | `Mistral/devtools/mistral-github-bridge.md` |
| 3.2 | Créer `mistral-ecos-cli-integration.md` | Intégration des skills Mistral avec `ecos-cli`. | @JPEG Lubbin | 2026-05-30 | `Mistral/devtools/mistral-ecos-cli-integration.md` |
| 3.3 | Développer `mistral_github_bridge.ps1` | Script PowerShell pour interagir avec GitHub. | @gerivdb | 2026-05-30 | `Mistral/scripts/mistral_github_bridge.ps1` |

### Phase 4 : Surveillance et Décision (L1/L2) — **P1**
| Étape | Action | Détail | Responsable | Deadline | Livrable |
|-------|--------|--------|-------------|----------|----------|
| 4.1 | Créer `mistral-nexus-monitor.md` | Surveillance des changements dans NEXUS. | @gerivdb | 2026-05-31 | `Mistral/nexus/mistral-nexus-monitor.md` |
| 4.2 | Créer `mistral-decision-engine.md` | Moteur de décision pour les agents Mistral. | @gerivdb | 2026-06-01 | `Mistral/cognitive/mistral-decision-engine.md` |

### Phase 5 : Transversal (Tous) — **P1/P2**
| Étape | Action | Détail | Responsable | Deadline | Livrable |
|-------|--------|--------|-------------|----------|----------|
| 5.1 | Créer `mistral_error_handler.ps1` | Gestion centralisée des erreurs. | @gerivdb | 2026-06-01 | `Mistral/scripts/mistral_error_handler.ps1` |
| 5.2 | Créer `mistral_logging.py` | Journalisation standardisée. | @gerivdb | 2026-06-02 | `Mistral/scripts/mistral_logging.py` |
| 5.3 | Créer `test_mistral_skills.py` | Suite de tests pour les skills Mistral. | @gerivdb | 2026-06-02 | `Mistral/tests/test_mistral_skills.py` |

---

## 4. Gestion des Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| **Conflits avec Perplexity** | Moyenne | Élevé | Comparer les skills Mistral et Perplexity avec `git diff --no-index`. |
| **Non-conformité REPO-STANDARDS** | Faible | Moyen | Exécuter `rss_lint.py --strict` avant chaque commit. |
| **Dépendances manquantes** | Moyenne | Moyen | Vérifier les `dependencies` dans les métadonnées des skills. |
| **Scripts non fonctionnels** | Faible | Moyen | Tester en mode `--dry-run` ou `-WhatIf` avant merge. |
| **Retard sur les deadlines** | Moyenne | Moyen | Prioriser les tâches **P0** et reporter les **P2** si nécessaire. |

---

## 5. Critères d'Acceptation

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

## 6. Décisions en Attente
| # | Décision | Options | Responsable |
|---|----------|---------|-------------|
| D1 | **Faut-il archiver les skills redondants** (ex: `nexus-core.md` existe dans Perplexity et Mistral) ? | Oui (dans `archive/mistral-archive/`) / Non (fusionner) | @gerivdb |
| D2 | **Quelle priorité pour les scripts Python vs PowerShell** ? | Python (portabilité) / PowerShell (intégration Windows) | @gerivdb |
| D3 | **Faut-il ajouter un dossier `Mistral/cognitive/`** pour les skills L2 ? | Oui / Non (intégrer dans `nexus/`) | @gerivdb |

---

## 7. Intégration KIVA CLI
Le workflow cible doit privilégier l'exécution locale (KIVA CLI) pour :
- Exécuter le linter REPO-STANDARDS (`rss_lint.py --strict`).
- Lancer les scripts d'indexation (`scripts/index_skills.py --dry-run`).
- Tester les scripts Mistral en mode safe (`-WhatIf` ou `--dry-run`).
- Exécuter les tests unitaires (`pytest Mistral/tests/ -q`).

**Commandes KIVA** :
```bash
# Pipeline complet
kiva ci run --stages lint,test,index

# Ou étape par étape
python D:\DO\WEB\TOOLS\L4-TOOLS\REPO-STANDARDS\rss_lint.py --repo . --strict
python scripts/index_skills.py --dry-run
cmd /c powershell -ExecutionPolicy ByPass -File "Mistral\scripts\mistral_nexus_sync.ps1" -WhatIf
python -m pytest Mistral/tests/ -q
```

---

## 8. Métriques de Succès
| Métrique | Cible | Mesure |
|----------|-------|--------|
| **Skills P0 créés** | 6 | Nombre de fichiers `.md` dans `Mistral/{governance,nexus,devtools/}`. |
| **Scripts P0 créés** | 2 | Nombre de scripts dans `Mistral/scripts/`. |
| **Conformité REPO-STANDARDS** | 100% | `rss_lint.py --strict` → 0 violation. |
| **Taux de succès des tests** | 100% | `pytest Mistral/tests/ -q` → exit code 0. |
| **Temps d'exécution des scripts** | < 5 min | Temps moyen pour `mistral_nexus_sync.ps1`. |

---
*IntentHash: 0xPRD_MISTRAL_SKILLS_INTEGRATION_20260528 | Version: 1.1.0 | Statut: DRAFT*