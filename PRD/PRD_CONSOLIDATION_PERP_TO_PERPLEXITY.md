---
type: PRD
version: 1.0.0
date: 2026-05-26
intent_hash: 0xPRD_PERP_PERPLEXITY_CONSOLIDATION_20260526
status: draft
author: owl/kilo
---

# PRD — Consolidation /perp → /perplexity

## Métadonnées

| Champ | Valeur |
|---|---|
| **IntentHash** | `0xPRD_PERP_PERPLEXITY_CONSOLIDATION_20260526` |
| **Dépôt Hôte** | `gerivdb/SKILLS` |
| **Branche de travail** | `skills/consolidate-perp-to-perplexity` |
| **Statut** | DRAFT → REVIEW → APPROVED → DONE |
| **Priorité** | P1 — Haute (conformité REPO-STANDARDS) |
| **EPIC lié** | EPIC_PERP_PERPLEXITY_CONSOLIDATION |

---

## 1. Contexte et Problème

### 1.1 Situation actuelle

Le dépôt SKILLS contient **deux réskills** pour le même usage (skills Perplexity SaaS / ENV1) :

| Répertoire | Fichiers | Rôle historique |
|---|---|---|
| `perp/` | 17 | Créé le 2026-04-24 comme premier espace Perplexity ; contient exemples, format canonical, fragments |
| `perplexity/` | 63 | Créé le 2026-05-26 via migration de 53 skills + scripts depuis commit `fe89b02` |

**Résultat** : duplication partielle, confusion sur la source de vérité, violation du standard REPO-STANDARDS (pas de répertoires redondants).

### 1.2 Redondances identifiées

**Fichiers en doublon (même nom, contenu à comparer)** :

| Fichier | Dans `perp/` | Dans `perplexity/` | Action requise |
|---|---|---|---|
| `comet-browser.md` | ✅ | ✅ | Diff + fusion ou choix version |
| `data-vector.md` | ✅ | ✅ | Diff + fusion ou choix version |

**Fichiers uniques à `perp/` (à rapatrier ou archiver)** :

| Fichier | Recommandation | Justification |
|---|---|---|
| `SKILL_FORMAT_CANONICAL.md` | **RAPATRIER** → `perplexity/` | Référence de format canonical, utile pour tous les skills |
| `generate-skills.ps1` | **RAPATRIER** → `perplexity/scripts/` | Script générateur, complément aux scripts existants |
| `analyse-repo-deepwiki.md` | **RAPATRIER** → `perplexity/` | Fonctionnalité manquante dans perplexity |
| `deepwiki_repo_enricher.md` | **RAPATRIER** → `perplexity/` | Fonctionnalité manquante |
| `examples/brain-cortex.md` | **RAPATRIER** → `perplexity/examples/` | Exemple de référence |
| `examples/ecosystem-maestro.md` | **RAPATRIER** → `perplexity/examples/` | Exemple de référence |
| `fermi-legacy.md` | **RAPATRIER** → `perplexity/` | Fonctionnalité manquante |
| `hitl-ops.md` | **RAPATRIER** → `perplexity/` | Fonctionnalité manquante |
| `media-culture.md` | **RAPATRIER** → `perplexity/` | Fonctionnalité manquante |
| `new-pillars.md` | **RAPATRIER** → `perplexity/` | Fonctionnalité manquante |
| `nexus-map.md` | **RAPATRIER** → `perplexity/` | Fonctionnalité manquante |
| `pulse-infra.md` | **RAPATRIER** → `perplexity/` | Fonctionnalité manquante |
| `swarm-cli.md` | **RAPATRIER** → `perplexity/` | Fonctionnalité manquante |
| `triade-mind.md` | **RAPATRIER** → `perplexity/` | Fonctionnalité manquante |
| `Nouveau document texte (2).txt` | **ARCHIVER** | Nom temporaire, non fonctionnel |

**Fichiers uniques à `perplexity/` (déjà au bon endroit, à conserver)** :

| Fichier/Prefix | Statut |
|---|---|
| Tous les `*.md` skills (adr-manager, nexus-*, triade-*, etc.) | ✅ Conserver |
| `scripts/*.ps1` | ✅ Conserver |
| `README.md` | ✅ Conserver |

### 1.3 Cause racine

La migration du commit `fe89b02` a copié les assets vers `perplexity/` sans nettoyer/consolider `perp/`. Un workflow de rebase interrompu (reflog: `HEAD@{23}: rebase (abort)`) a laissé l'opération incomplète.

---

## 2. Objectifs

| # | Objectif | Critère de succès | Mesure |
|---|---|---|---|
| O1 | Éliminer la redondance `/perp` → `/perplexity` | `perp/` n'existe plus dans main (ou contient uniquement `README.md` pointeur) | `ls perp/` ou `test -d perp` → exit 0 |
| O2 | Conserver **tous** les fichiers uniques de `perp/` dans `perplexity/` | Nombre de fichiers perdus = 0 | Inventaire avant/après avec `git ls-files` |
| O3 | Réconcilier les 2 doublons (`comet-browser.md`, `data-vector.md`) | 0 fichier dupliqué entre les deux chemins | `git diff --no-index` → identique ou fusionné |
| O4 | Conformité REPO-STANDARDS | `rss_lint.py --strict` → 0 violation | Exécution du linter |
| O5 | Mettre à jour les références croisées | REGISTRY.yaml, scripts indexation pointent sur `perplexity/` | `grep -r "perp/" REGISTRY.yaml scripts/` → 0 match |
| O6 | Traçabilité complète | Chaque déplacement = 1 commit atomique avec message normé | `git log --oneline` vérifiable |

---

## 3. Hors-périmètre

- **Ne PAS toucher** aux skills `native/` (domaines booking, finance, etc.)
- **Ne PAS toucher** aux skills `skills/` (patterns logiciels)
- **Ne PAS toucher** aux skills `cognitive/` (YAML patterns)
- **Ne PAS modifier** le contenu des fichiers uniquement dans `perplexity/` (sauf si fusion de doublon)
- **Ne PAS supprimer** le répertoire `perp/` avant d'avoir archivé le contenu unique
- **Ne PAS push directement sur main** — branche de travail + PR obligatoire

---

## 4. Architecture Cible

### 4.1 Structure finale attendue

```
SKILLS/
├── PRD/
│   └── PRD_CONSOLIDATION_PERP_TO_PERPLEXITY.md    ← ce PRD
├── epics/
│   └── EPIC_PERP_PERPLEXITY_CONSOLIDATION.md      ← EPIC lié
├── perplexity/                                      ← Source de vérité unique
│   ├── README.md
│   ├── SKILL_FORMAT_CANONICAL.md                    ← rapatrié de perp/
│   ├── comet-browser.md                             ← version réconciliée
│   ├── data-vector.md                               ← version réconciliée
│   ├── [53 autres .md skills]                       ← existant
│   ├── examples/
│   │   ├── brain-cortex.md                          ← rapatrié de perp/
│   │   └── ecosystem-maestro.md                     ← rapatrié de perp/
│   └── scripts/
│       ├── generate-skills.ps1                      ← rapatrié de perp/
│       └── [autres scripts existants]
├── native/                                          ← intact
├── cognitive/                                       ← intact
├── skills/                                          ← intact
├── archive/                                         ← uniquement si archivage
│   └── perp-archive/
│       └── [fichiers obsolètes archivés le cas échéant]
└── [autres dossiers racine]                         ← intacts
```

### 4.2 Règles de nommage (REPO-STANDARDS)

- Fichier canonical : `SKILL_FORMAT_CANONICAL.md` (PascalCase pour fichiers de référence)
- Scripts : `kebab-case.ps1`
- Skills : `kebab-case.md`
- Aucun fichier avec espaces ou parenthèses dans le nom
- Max 2 niveaux de profondeur

---

## 5. Plan d'Implémentation

### Phase 0 — Préparation (non-destructive)

| Étape | Action | Commande | Validation |
|---|---|---|---|
| 0.1 | Créer branche de travail | `git checkout -b skills/consolidate-perp-to-perplexity` | `git branch --show-current` → branche correcte |
| 0.2 | Sauvegarde bundle | `git bundle create ../skills-backup.bundle --all` | Fichier bundle existe |
| 0.3 | État initial | `git status --porcelain=2 --branch` | Note des fichiers untracked |
| 0.4 | Lister worktrees | `git worktree list` | Examiner fire-omelet |

### Phase 1 — Analyse ciblée

| Étape | Action | Commande | Validation |
|---|---|---|---|
| 1.1 | Diff doublon #1 | `git diff --no-index perp/comet-browser.md perplexity/comet-browser.md > diffs/comet-browser.patch` | Lire le patch, décider action |
| 1.2 | Diff doublon #2 | `git diff --no-index perp/data-vector.md perplexity/data-vector.md > diffs/data-vector.patch` | Lire le patch, décider action |
| 1.3 | Créer table de décision | Remplir `PRD/decisions_mapping.csv` | Fichier CSV complet |

### Phase 2 — Exécution atomique (par commits petits et traçables) (par fichier/groupe ; total estimé 1–3h selon volume)

Règles :
- Un commit = une action logique (p.ex. déplacer 1 à 5 fichiers liés).
- Eviter git add . ; utiliser git add <fichiers> explicite.
- Messages de commit conviviaux et explicites.

Opérations types :
1. Déplacer fichier(s) pertinents de perp → perplexity (git mv)
   - git mv "perp/SKILL_FORMAT_CANONICAL.md" "perplexity/SKILL_FORMAT_CANONICAL.md"
   - git add perplexity/SKILL_FORMAT_CANONICAL.md
   - git commit -m "chore(skills): move SKILL_FORMAT_CANONICAL from /perp to /perplexity — consolidation"
2. Fusionner doublons (manuellement)
   - Ouvrir les deux fichiers, produire version canonical dans perplexity/, puis :
     - git add perplexity/comet-browser.md
     - git rm perp/comet-browser.md
     - git commit -m "fix(skills): reconcile comet-browser.md — merged Perp & Perplexity versions"
3. Archiver fichiers obsolètes (ne pas supprimer immédiatement)
   - Créer dossier archive/perp-archive/ et y déplacer :
     - mkdir archive\perp-archive
     - git mv perp\Nouveau\ document\ texte\ \(2\).txt archive\perp-archive\
     - git commit -m "chore(skills): archive leftover perp artifacts to archive/perp-archive"
   - Rationnel : garde historique accessible pour review.
4. Supprimer fichiers non pertinents seulement après validation (commit séparé)
   - git rm <file>
   - git commit -m "chore(skills): remove obsolete file <file> after consolidation and approval"
5. Pour scripts qui doivent être centralisés, déplacer et vérifier shebang/paths :
   - git mv perp/scripts/generate-skills.ps1 perplexity/scripts/generate-skills.ps1
   - Corriger références internes (chemins relatifs) avant commit.

### Phase 3 — Validation locale et linting (15–30 min)

1. Re-exécuter REPO-STANDARDS linter et corriger
   - python "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\REPO-STANDARDS\\rss_lint.py" --repo . --fix
   - Commit des corrections suggérées (un commit par correctif groupé logique).
2. Exécuter tout script d'intégrité disponible :
   - python scripts/index_skills.py --dry-run
   - Vérifier que les nouveaux chemins sont indexés correctement (perplexity/*)
3. Vérifier que REGISTRY.yaml / scripts d'upload pointent vers perplexity
   - grep/local search pour occurrences de "/perp/" et corriger en "/perplexity/" si besoin.

### Phase 4 — PR et Merge

| Étape | Action | Détail |
|---|---|---|
| 4.1 | Push branche | `git push -u origin skills/consolidate-perp-to-perplexity` |
| 4.2 | Ouvrir PR | Titre : `chore(skills): consolidate /perp into /perplexity — move, reconcile, archive` |
| 4.3 | Description PR | Inclure table des fichiers déplacés, diffs des doublons, résultats linter |
| 4.4 | Review + Approve | Minimum 1 reviewer |
| 4.5 | Merge sur main | Squash ou merge commit selon convention repo |

### Phase 5 — Post-merge et nettoyage (15–45 min)

1. Après approbation et merge : supprimer dossier perp si convenu (opération PR finale ou commit post-merge)
   - git rm -r perp
   - git commit -m "chore(skills): remove /perp after consolidation into /perplexity — archived content retained in archive/perp-archive"
2. Nettoyer worktree si prunable et confirmé
   - git worktree list
   - Si safe : git worktree remove "D:/DO/WEB/SKILLS/.kilo/worktrees/fire-omelet"
3. Lancer le linter sur main et vérifier CI local :
   - python "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\REPO-STANDARDS\\rss_lint.py" --repo . --strict
4. Mettre à jour REGISTRY.yaml / docs README si nécessaire et committer.

---

## 6. Gestion des Risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Perte de contenu unique de `perp/` | Moyenne | Élevé | Inventaire complet avant tout mv ; bundle de sauvegarde |
| Fusion incorrecte des doublons | Moyenne | Moyen | Diff manuel + revue humaine avant commit |
| Références cassées après déplacement | Faible | Moyen | `grep -r "perp/"` après consolidation + correction |
| Conflit avec branches feature | Faible | Moyen | Rebase de la branche consolidation avant merge |
| Worktree fire-omelet dépend de perp/ | Inconnue | Faible | Examiner le worktree avant de supprimer perp/ |

---

## 7. Critères d'Acceptation

- [ ] Le répertoire `perp/` n'existe plus dans `main` (post-merge)
- [ ] Tous les 14 fichiers uniques de `perp/` ont été rapatriés vers `perplexity/` ou archivés
- [ ] Les 2 doublons (`comet-browser.md`, `data-vector.md`) sont réconciliés
- [ ] `rss_lint.py --strict` retourne 0 violation
- [ ] Aucune référence à `perp/` dans REGISTRY.yaml ou scripts
- [ ] 0 fichier perdu (comptage `git ls-files` avant = après)
- [ ] Changelog mis à jour
- [ ] PR mergée et branche supprimée

---

## 8. Décisions En Attente

| # | Décision | Options | Responsable | Deadline |
|---|---|---|---|---|
| D1 | Version à garder pour `comet-browser.md` | perplexity / perp / fusion | Reviewer | Avant merge PR |
| D2 | Version à garder pour `data-vector.md` | perplexity / perp / fusion | Reviewer | Avant merge PR |
| D3 | Archiver ou supprimer `perp/` définitivement | archive/perp-archive / suppression | Maintainer | Phase 5 |

---

## 9. Intégration KIVA CLI (CI local)

Le PRD précédent ne mentionnait pas explicitement l'utilisation du CI local fourni par KIVA CLI. Le workflow cible doit privilégier l'exécution locale (KIVA CLI / équivalent) plutôt que les GitHub Actions pour :

- exécuter le linter REPO-STANDARDS (rss_lint.py)
- lancer les scripts d'intégrité et d'indexation (scripts/index_skills.py)
- exécuter les scripts PowerShell en mode dry-run (perplexity/scripts/organize_perplexity.ps1)
- lancer les suites de tests locales (pytest) si présentes

Tâches KIVA CLI à ajouter dans le pipeline local :

1. Exécuter lint strict :
   - python "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\REPO-STANDARDS\\rss_lint.py" --repo . --strict
2. Exécuter indexation dry-run :
   - python scripts/index_skills.py --dry-run
3. Tester scripts Perplexity en mode safe :
   - cmd /c powershell -ExecutionPolicy ByPass -File "perplexity\\scripts\\organize_perplexity.ps1" -WhatIf
4. Lancer tests unitaires (si présents) :
   - python -m pytest tests -q

Validation KIVA CLI :
- Le job local devra retourner code 0 pour toutes les étapes ci-dessus avant ouverture de PR.
- Si KIVA CLI expose une commande globale, elle devrait invoquer ces Etapes (ex: `kiva ci run --stages lint,test,index`). En absence d'une CLI globale, exécuter les commandes directes ci-dessus dans le runner local.

Remarque opérationnelle : respecter la règle "CMD wrapper for PowerShell" — utiliser `cmd /c powershell -ExecutionPolicy ByPass -File <script.ps1>` pour lancer les PS1 dans le runner local.

---

## 10. Critères d'acceptation supplémentaires (KIVA)

- [ ] Le pipeline local (KIVA) exécute lint, index, scripts dry-run et tests sans erreur
- [ ] Les logs KIVA sont attachés au PR pour audit
- [ ] Aucune différence entre résultats locaux et CI attendu

---

*IntentHash: 0xPRD_PERP_PERPLEXITY_CONSOLIDATION_20260526 | Version: 1.0.1 | Statut: DRAFT — KIVA-ENABLED*
