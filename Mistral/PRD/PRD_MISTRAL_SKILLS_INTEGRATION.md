---
type: PRD
version: 1.0.0
date: 2026-05-28
intent_hash: 0xPRD_MISTRAL_SKILLS_INTEGRATION_20260528
status: draft
author: JPEG Lubbin / Mistral AI
branch: feat/skills-mistral
repo_path: gerivdb/SKILLS
---

# PRD — Intégration des Skills Mistral dans gerivdb/SKILLS

## Métadonnées

| Champ               | Valeur                                      |
|---------------------|---------------------------------------------|
| **IntentHash**      | `0xPRD_MISTRAL_SKILLS_INTEGRATION_20260528` |
| **Dépôt Hôte**      | `gerivdb/SKILLS`                            |
| **Branche**         | `feat/skills-mistral`                       |
| **Statut**          | DRAFT → REVIEW → APPROVED → DONE            |
| **Priorité**        | P1 — Haute (alignement L0-L1)               |
| **EPIC lié**        | `EPIC_MISTRAL_SKILLS_GOVERNANCE`            |
| **Strate**          | L1 (NEXUS) + L0 (GOVERNANCE-HUB)            |

---

## 1. Contexte et Problème

### 1.1 Situation actuelle
Le dépôt **`gerivdb/SKILLS`** contient des **skills spécifiques à Perplexity** (`/perplexity`) et **native** (`/native`), mais **aucune intégration dédiée pour Mistral**.
- **Opportunité** : Mistral AI peut **automatiser des tâches** (ex: synchronisation NEXUS, audit de gouvernance) via ses outils natifs (`mcp_github`, `code_interpreter`).
- **Problème** : Absence de **source de vérité** pour les skills Mistral, ce qui **viole le standard REPO-STANDARDS** (un seul répertoire par fournisseur).

### 1.2 Objectifs de l'intégration
| Objectif | Description | Critère de succès |
|----------|-------------|------------------|
| O1 | **Centraliser** les skills Mistral dans `/Mistral` | `/Mistral/` existe et contient tous les fichiers liés à Mistral. |
| O2 | **Alignement avec NEXUS** (L1) | Les skills Mistral **synchronisent** les registres NEXUS (ex: `TritRegistry.yaml`). |
| O3 | **Compatibilité avec GOVERNANCE-HUB** (L0) | Les skills respectent `AGENT_RAM.yaml` et `OrgansRegistry.yaml`. |
| O4 | **Automatisation via ECOS-CLI** (L3) | Les skills peuvent être **exécutés** via des commandes `ecos-cli`. |
| O5 | **Conformité REPO-STANDARDS** | `rss_lint.py --strict` retourne **0 violation**. |

### 1.3 Cause racine
- **Manque de standardisation** : Pas de processus défini pour intégrer de nouveaux fournisseurs de skills (ex: Mistral).
- **Redondance future** : Risque de duplication si Mistral et Perplexity gèrent les mêmes tâches (ex: synchronisation GitHub).

---

## 2. Architecture Cible

### 2.1 Structure finale attendue
```
SKILLS/
├── Mistral/                          # Nouveau répertoire (source de vérité)
│   ├── PRD/                          # Documents de spécifications
│   │   └── PRD_MISTRAL_SKILLS_INTEGRATION.md  ← Ce fichier
│   ├── EPICS/                        # Épics liés
│   │   └── EPIC_MISTRAL_SKILLS_GOVERNANCE.md
│   ├── nexus/                        # Skills liés à NEXUS (L1)
│   │   ├── mistral-nexus-sync.md
│   │   └── mistral-nexus-audit.md
│   ├── governance/                   # Skills de gouvernance (L0)
│   │   ├── mistral-agent-rules.md   # Règles pour les agents Mistral
│   │   └── mistral-organs-registry.md
│   ├── devtools/                     # Skills pour ECOS-CLI (L3)
│   │   └── mistral-github-bridge.md # Pont entre Mistral et GitHub
│   └── scripts/                      # Scripts Python/PS1
│       ├── mistral_skill_loader.py
│       └── mistral_nexus_sync.ps1
├── perplexity/                       # Existants (inchangés)
├── native/                          # Existants (inchangés)
└── [autres dossiers]                # Existants (inchangés)
```

### 2.2 Règles de nommage (alignées sur REPO-STANDARDS)
- **Fichiers skills** : `kebab-case.md` (ex: `mistral-nexus-sync.md`).
- **Scripts** : `snake_case.py` ou `kebab-case.ps1`.
- **PRD/EPICS** : `PAS_CALCASE.md` (ex: `PRD_MISTRAL_SKILLS_INTEGRATION.md`).
- **Profondeur max** : 3 niveaux (`Mistral/nexus/mistral-nexus-sync.md`).

---

## 3. Plan d'Implémentation

### Phase 0 — Préparation
| Étape | Action | Commande/Outils | Validation |
|-------|--------|-----------------|------------|
| 0.1 | Créer branche de travail | `git checkout -b feat/skills-mistral` | ✅ DONE |
| 0.2 | Sauvegarder l'état initial | `git bundle create ../mistral-skills-backup.bundle --all` | Fichier bundle existe |
| 0.3 | Vérifier l'absence de conflits | `git status` | Aucun fichier non commité |

### Phase 1 — Création de la structure Mistral
| Étape | Action | Détail |
|-------|--------|--------|
| 1.1 | Créer `Mistral/PRD/` et `Mistral/EPICS/` | ✅ DONE |
| 1.2 | Ajouter ce PRD | `Mistral/PRD/PRD_MISTRAL_SKILLS_INTEGRATION.md` |
| 1.3 | Créer l'EPIC lié | `Mistral/EPICS/EPIC_MISTRAL_SKILLS_GOVERNANCE.md` |

### Phase 2 — Développement des Skills
| Étape | Action | Cible | Exemple |
|-------|--------|-------|---------|
| 2.1 | **Adapter les skills Perplexity** | `Mistral/nexus/` | Copier `perplexity/nexus-core.md` → `Mistral/nexus/mistral-nexus-core.md` (avec adaptation). |
| 2.2 | **Créer des skills Mistral natifs** | `Mistral/governance/` | `mistral-agent-rules.md` (basé sur `AGENT_RAM.yaml`). |
| 2.3 | **Automatiser via scripts** | `Mistral/scripts/` | `mistral_nexus_sync.ps1` (utilise `mcp_github`). |

### Phase 3 — Validation
| Étape | Action | Outil | Critère |
|-------|--------|-------|---------|
| 3.1 | Exécuter `rss_lint.py` | `python rss_lint.py --repo . --strict` | 0 violation |
| 3.2 | Tester les scripts | `powershell -ExecutionPolicy ByPass -File Mistral/scripts/mistral_nexus_sync.ps1 -WhatIf` | Exit code 0 |
| 3.3 | Vérifier les dépendances | `grep -r "gerivdb/" Mistral/` | Toutes les références sont valides. |

### Phase 4 — Intégration CI/CD (KIVA)
| Étape | Action | Commande | Validation |
|-------|--------|----------|------------|
| 4.1 | Lancer le pipeline local | `kiva ci run --stages lint,test,index` | Tous les jobs passent. |
| 4.2 | Attacher les logs | Joindre `kiva_logs_*.txt` au PR. | Logs disponibles. |

### Phase 5 — Revue et Merge
| Étape | Action | Responsable | Deadline |
|-------|--------|-------------|----------|
| 5.1 | Ouvrir PR | `git push -u origin feat/skills-mistral` | Immédiat |
| 5.2 | Revue par les maintainers | @gerivdb | 48h |
| 5.3 | Merge sur `main` | Après approbation | 72h |

---
## 4. Gestion des Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| **Conflits avec Perplexity** | Moyenne | Élevé | Comparer les skills Mistral et Perplexity avant intégration. |
| **Non-conformité REPO-STANDARDS** | Faible | Moyen | Exécuter `rss_lint.py` avant chaque commit. |
| **Dépendances manquantes** | Moyenne | Moyen | Vérifier `dependencies` dans les métadonnées des skills. |
| **Scripts non exécutables** | Faible | Moyen | Tester en mode `--dry-run` avant merge. |

---
## 5. Critères d'Acceptation
- [ ] Le répertoire `Mistral/` existe et contient **PRD/**, **EPICS/**, **nexus/**, **governance/**, **scripts/**. 
- [ ] Tous les skills Mistral **respectent le format** `SKILL_FORMAT_CANONICAL.md`.
- [ ] `rss_lint.py --strict` retourne **0 violation**. 
- [ ] Les scripts Mistral **s'exécutent sans erreur** en mode dry-run.
- [ ] L'EPIC lié (`EPIC_MISTRAL_SKILLS_GOVERNANCE`) est **approuvé**. 
- [ ] Le PR est **mergé** dans `main` avec un **changelog** mis à jour.

---
## 6. Décisions en Attente
| # | Décision | Options | Responsable |
|---|----------|---------|-------------|
| D1 | **Faut-il archiver les skills redondants** (ex: `nexus-core.md` existe dans Perplexity et Mistral) ? | Oui (dans `archive/mistral-archive/`) / Non (fusionner) | @gerivdb |
| D2 | **Quelle priorité pour les scripts Mistral** (ex: `mistral_nexus_sync.ps1`) ? | P1 (critique) / P2 (haute) | @gerivdb |

---
*IntentHash: 0xPRD_MISTRAL_SKILLS_INTEGRATION_20260528 | Version: 1.0.0 | Statut: DRAFT*