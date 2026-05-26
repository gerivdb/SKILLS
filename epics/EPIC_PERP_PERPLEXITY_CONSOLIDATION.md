---
type: EPIC
version: 1.0.0
date: 2026-05-26
intent_hash: 0xEPIC_PERP_PERPLEXITY_CONSOLIDATION_20260526
status: planned
---

# EPIC — Consolidation /perp → /perplexity

## Métadonnées

| Champ | Valeur |
|---|---|
| **IntentHash** | `0xEPIC_PERP_PERPLEXITY_CONSOLIDATION_20260526` |
| **Dépôt Hôte** | `gerivdb/SKILLS` |
| **Statut** | PLANNED |
| **Version** | 1.0.0 |
| **Priorité** | P1 — Haute |
| **PRD lié** | `PRD/PRD_CONSOLIDATION_PERP_TO_PERPLEXITY.md` |

---

## Résumé

Consolider le répertoire historique `perp/` dans le répertoire `perplexity/` pour éliminer la redondance des skills Perplexity SaaS (ENV1), en conservant tous les fichiers uniques, réconciliant les doublons, et en mettant le dépôt en conformité avec REPO-STANDARDS.

---

## Contexte

Le dépôt SKILLS est le registry central de l'écosystème `gerivdb`. Lors de la migration récente (commit `fe89b02`, 2026-05-26), 53 skills Perplexity ont été ajoutés dans `/perplexity`. Cependant, un répertoire historique `/perp` (créé 2026-04-24) persiste avec :

- 14 fichiers uniques (non présents dans `/perplexity`)
- 2 fichiers en doublon (`comet-browser.md`, `data-vector.md`)
- 1 fichier temporaire obsolète

Cette situation viole le standard **REPO-STANDARDS** (pas de répertoires redondants, source de vérité unique).

---

## Problème

1. **Source de doute** : deux chemins pour le même usage → confusion pour les agents et les scripts
2. **Violation REPO-STANDARDS** : structure non conforme (redondance)
3. **Risque d'oubli** : fichiers uniques dans `perp/` risquent d'être ignorés par les indexeurs/consommateurs
4. **Migration inachevée** : le commit `fe89b02` a copié sans consolider (workflow interrompu, rebase aborté)

---

## Objectifs Stratégiques

| # | Objectif | KPI | Cible |
|---|---|---|---|
| O1 | Source de vérité unique pour skills Perplexity | Nombre de répertoires Perplexity actifs | = 1 (`perplexity/`) |
| O2 | Conservation intégrale du contenu | Fichiers perdus | = 0 |
| O3 | Conformité REPO-STANDARDS | Violations rss_lint.py | = 0 |
| O4 | Traçabilité des déplacements | Commits atomiques | ≥ 15 commits sur branche |
| O5 | Zéro référence orpheline | Matches `grep -r "perp/"` dans code actif | = 0 |

---

## Structure Cible

```
SKILLS/
├── perplexity/              ← Source de vérité unique pour skills Perplexity ENV1
│   ├── README.md
│   ├── SKILL_FORMAT_CANONICAL.md
│   ├── comet-browser.md     (version réconciliée)
│   ├── data-vector.md       (version réconciliée)
│   ├── examples/
│   │   ├── brain-cortex.md
│   │   └── ecosystem-maestro.md
│   └── scripts/
│       ├── generate-skills.ps1
│       └── [6 outils existants]
├── archive/
│   └── perp-archive/        ← Artefacts obsolètes archivés
├── native/                  ← inchangé
├── cognitive/               ← inchangé
├── skills/                  ← inchangé
└── [autres dossiers]        ← inchangés
```

---

## Traces d'Exécution (Tasks)

### T1 — Analyse préalable (phase 0-1)

| Task | Fichier(s) | Action | Commit type |
|---|---|---|---|
| T1.1 | — | Créer branche `skills/consolidate-perp-to-perplexity` | — |
| T1.2 | `perp/comet-browser.md` vs `perplexity/comet-browser.md` | Diff + décision version à garder | — |
| T1.3 | `perp/data-vector.md` vs `perplexity/data-vector.md` | Diff + décision version à garder | — |
| T1.4 | tous fichiers `perp/` | Inventaire et classification (keep/archive/discard) | — |

### T2 — Rapatriements atomiques (phase 2)

| Task | Source → Destination | Commit message |
|---|---|---|
| T2.1 | `perp/examples/*.md` → `perplexity/examples/` | `chore(skills): mv examples from /perp to /perplexity` |
| T2.2 | `perp/SKILL_FORMAT_CANONICAL.md` → `perplexity/` | `chore(skills): mv SKILL_FORMAT_CANONICAL to /perplexity` |
| T2.3 | `perp/{analyse-repo-deepwiki,deepwiki_repo_enricher}.md` → `perplexity/` | `chore(skills): mv deepwiki skills from /perp to /perplexity` |
| T2.4 | `perp/{fermi-legacy,hitl-ops,media-culture}.md` → `perplexity/` | `chore(skills): mv 3 Perplexity skills from /perp to /perplexity` |
| T2.5 | `perp/{new-pillars,nexus-map,pulse-infra}.md` → `perplexity/` | `chore(skills): mv 3 Perplexity skills from /perp to /perplexity` |
| T2.6 | `perp/{swarm-cli,triade-mind}.md` → `perplexity/` | `chore(skills): mv 2 Perplexity skills from /perp to /perplexity` |
| T2.7 | `perp/scripts/generate-skills.ps1` → `perplexity/scripts/` | `chore(skills): mv generate-skills.ps1 to /perplexity/scripts` |
| T2.8 | `perp/Nouveau document texte (2).txt` → `archive/perp-archive/` | `chore(skills): archive orphaned temp file from /perp` |

### T3 — Réconciliation des doublons (phase 2)

| Task | Fichier | Action | Commit message |
|---|---|---|---|
| T3.1 | `comet-browser.md` | Fusionner ou choisir version ; garder dans `perplexity/` ; supprimer `perp/` | `fix(skills): reconcile comet-browser.md between /perp and /perplexity` |
| T3.2 | `data-vector.md` | Fusionner ou choisir version ; garder dans `perplexity/` ; supprimer `perp/` | `fix(skills): reconcile data-vector.md between /perp and /perplexity` |

### T4 — Nettoyage final (phase 2-3)

| Task | Action | Commit message |
|---|---|---|
| T4.1 | Supprimer `perp/` (vide après rapatriements) | `chore(skills): remove /perp after full consolidation into /perplexity` |
| T4.2 | Exécuter `rss_lint.py --fix` et committer corrections | `chore(skills): apply rss_lint fixes for REPO-STANDARDS compliance` |
| T4.3 | Mettre à jour références dans REGISTRY.yaml / scripts si nécessaire | `chore(skills): update references from /perp to /perplexity in registry+scripts` |

### T5 — Validation et PR (phase 4)

| Task | Action |
|---|---|
| T5.1 | Vérifier `git ls-files perplexity/` = ~79 fichiers |
| T5.2 | Exécuter `rss_lint.py --strict` → 0 violation |
| T5.3 | Push branche + ouverture PR |
| T5.4 | Review + merge |

---

## Métriques de Suivi

| Métrique | Mesure | Outil | Fréquence |
|---|---|---|---|
| Fichiers `perp/` restants | `git ls-files perp/ | wc -l` | Terminal | Après chaque task |
| Fichiers `perplexity/` totaux | `git ls-files perplexity/ | wc -l` | Terminal | Après consolidation |
| Violations REPO-STANDARDS | `rss_lint.py --strict` exit code | Linter | Phase 3 |
| Références orphelines | `grep -r "perp/" --include="*.yaml" --include="*.ps1" --include="*.py" .` | grep | Phase 3 |
| Commits atomiques | `git log --oneline <branch> ⊣ wc -l` | git | Phase 4 |

---

## Risques et Garde-fous

| Risque | Mitigation |
|---|---|
| Perte de contenu unique | Sauvegarde bundle avant toute opération ; inventaire signé |
| Fusion incorrecte de doublons | Revue humaine obligatoire des diffs avant commit |
| Push sur main par erreur | Push protégé ; PR obligatoire + 1 reviewer |
| Interférence avec worktree `fire-omelet` | Examiner et sauvegarder le worktree avant de supprimer `perp/` |

---

## Décisions Requises

| # | Question | Options | Décideur |
|---|---|---|---|
| D1 | Version de `comper-browser.md` | `perplexity/` (nouveau) / `perp/` (ancien) / fusion | Reviewer |
| D2 | Version de `data-vector.md` | `perplexity/` (nouveau) / `perp/` (ancien) / fusion | Reviewer |
| D3 | Conservation de `perp/` comme README pointeur | Oui (README + redirect) / Non (suppression totale) | Maintainer |

---

## Livrables

| Livrable | Chemin | Statut |
|---|---|---|
| PRD détaillé | `PRD/PRD_CONSOLIDATION_PERP_TO_PERPLEXITY.md` | ✅ Écrit |
| EPIC ce document | `epics/EPIC_PERP_PERPLEXITY_CONSOLIDATION.md` | ✅ Écrit |
| Branche de consolidation | `skills/consolidate-perp-to-perplexity` | ⏳ À créer |
| PR GitHub | — | ⏳ À ouvrir |
| Merge sur main | — | ⏳ Après review |

---

## Références

- **REPO-STANDARDS** : `D:\DO\WEB\TOOLS\L4-TOOLS\REPO-STANDARDS\rss_lint.py`
- **Commit de migration initial** : `fe89b02` — `chore(skills): migrate 53 Perplexity skills and helper scripts to /perplexity`
- **SLM Rule** : `C:\Users\GG\.kilocode\rules\slm-fragmented-approach.md`

---

*IntentHash: 0xEPIC_PERP_PERPLEXITY_CONSOLIDATION_20260526 | Version: 1.0.0 | Statut: PLANNED*
