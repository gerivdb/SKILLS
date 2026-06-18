---
type: skill
version: "1.0.0"
date: "2026-06-18"
intent_hash: 0xCTULU_TOOL_SELECTOR_φ1.000
status: active
trit_primitive: TritSelectTool
tags: [ctulu, tool-routing, anything-suite, decision-matrix, l3-tooling]
layer: "L3_TOOLING"
nexusTags: ["CONFORME_NEXUS", "CTULU", "TOOL_ROUTING"]
slotWeight: 1
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 ECOS-CLI — gap sélection outil CTULU vs mcp_github"}
---

# ctulu-tool-selector

## Purpose

Guide de sélection des outils [gerivdb/CTULU/tools](https://github.com/gerivdb/CTULU/tree/main/tools) selon le contexte de la tâche, l'ENV actif et le budget tool_calls. Fournit une **matrice de décision** `[tâche] × [ENV] × [budget]` pour choisir entre outil CTULU, mcp_github, fetch_url, ou shell local.

## Trigger

Utiliser quand :
- la question "quel outil utiliser pour X" se pose
- un outil CTULU/Anything Suite est mentionné (`*-anything`, `intent-*`, `drift-*`...)
- une tâche pourrait bénéficier d'un outil spécialisé CTULU
- besoin de décider entre mcp_github natif et CTULU pour une opération git/PR/issue

## Inventaire référencé (CTULU/tools — 2026-06-18)

### Famille `-anything` (opérations génériques)

| Outil | Usage typique |
|---|---|
| `git-anything` | Opérations git avancées hors mcp_github |
| `pr-anything` | Gestion PR (création, review, merge) |
| `issue-anything` | Gestion issues GitHub |
| `branch-cleaner` | Nettoyage branches orphelines (complément `branch-audit-cleanup`) |
| `audit-anything` | Audits génériques multi-repo |
| `scan-anything` | Scans de contenu/code |
| `patch-anything` | Application de patches batch |
| `conform-anything` | Vérification conformité NEXUS |
| `diff-anything` | Analyse de diffs |
| `plan-anything` | Génération de plans d'implémentation |
| `batch-anything` | Opérations batch multi-fichiers |
| `sync-anything` | Synchronisation cross-repo |
| `scaffold-anything` | Génération de scaffolds RSS-v1 |
| `skill-anything` | Opérations sur les skills SKILLS |
| `adr-anything` | Création/gestion ADR |
| `epic-anything` | Gestion EPICs NEXUS |
| `workflow-anything` | Automatisation workflows GitHub Actions |

### Famille `intent-*` (causalité / graphes)

| Outil | Usage typique |
|---|---|
| `intent-anything` | Dérivation d'intentions depuis texte |
| `intent-chain` | Chaînage causal intent-to-action |
| `intent-hash-injector` | Injection intent_hash dans frontmatter |
| `intent-graph-builder` | Construction graphe d'intentions |
| `causal-chain-orchestrator` | Orchestration chaînes causales complexes |

### Famille `drift-*` / `observe-*` (monitoring)

| Outil | Usage typique |
|---|---|
| `drift-anything` | Détection de drift entre états |
| `drift-detect` | Détection drift spécifique NEXUS |
| `observe-anything` | Observation d'événements système |
| `nexus-scope-guard` | Protection scope NEXUS |

### Outils spéciaux pertinents

| Outil | Usage typique |
|---|---|
| `slm-chain-runner` | Exécution chaînes sur SLM local (ENV2/ENV3) |
| `token-capital` | Gestion capital tokens LLM |
| `env-resolver` | Résolution ENV actif |
| `frontmatter-guard` | Validation frontmatter YAML |
| `batch-governor` | Gouvernance des batchs (taille, retry) |
| `registry-sync` | Synchro known_repositories.yaml |
| `citizen-anything` | Opérations sur CITIZENS |

## Matrice de décision

```
TÂCHE                     | ENV1 (Perplexity)      | ENV2 (Z600 local)      | Priorité
--------------------------|------------------------|------------------------|----------
Lecture fichier GitHub    | mcp_github (direct)    | shell git              | mcp_github > fetch_url
Suppression branches      | mcp_github natif       | branch-cleaner CTULU   | selon ENV
Création PR              | mcp_github natif       | pr-anything CTULU      | mcp_github > CTULU
Audit multi-repo          | audit-anything CTULU   | audit-anything CTULU   | CTULU ≡
Batch patch frontmatter   | patch-anything CTULU   | patch-anything CTULU   | CTULU ≡
Détection drift NEXUS     | drift-detect CTULU     | drift-detect CTULU     | CTULU ≡
Création ADR              | adr-anything CTULU     | adr-anything CTULU     | CTULU ≡
Opérations SLM chain     | N/A (pas de SLM)       | slm-chain-runner CTULU | ENV2 only
Gestion capital tokens    | token-capital CTULU    | token-capital CTULU    | CTULU ≡
```

**Règle générale** :
1. `mcp_github` en premier pour toute opération GitHub native (lectures, PRs, issues, branches)
2. `CTULU` pour les opérations multi-repo, batch, audit, ou absentes de mcp_github
3. `fetch_url` uniquement si mcp_github budget épuisé ET lecture seule
4. `shell local` uniquement sur ENV2/ENV3

## Protocole de sélection

```
[CTULU_SELECTOR] Tâche: {description}
[CTULU_SELECTOR] ENV actif: {ENV1|ENV2|ENV3}
[CTULU_SELECTOR] Budget tool_calls restants: {N}/3
[CTULU_SELECTOR] Outil sélectionné: {outil} (raison: {raison})
[CTULU_SELECTOR] Fallback si échec: {fallback}
```

## Cas d'usage de cette session (2026-06-18)

Durant la session ECOS-CLI branche-cleanup :
- Suppression des 5 branches : `mcp_github` natif ✅ (opération GitHub native, budget 3/tour suffisant)
- Audit des branches orphelines : aurait pu utiliser `branch-cleaner` CTULU pour automatiser la détection des branches > 30j sans PR
- Création des skills SKILLS : `mcp_github push_files` ✅ (opération natale)

Lesson : CTULU est pertinent quand l'opération est **répétitive, multi-repo, ou nécessite une logique métier** au-delà du CRUD GitHub de base.

## Intégration écosystème

- **Précède** : `ctulu-result-integrator` (normalisation de la sortie)
- **Complémente** : `ctulu-tool-factory` (si l'outil n'existe pas encore)
- **Référence** : `llm-tool-budget-guard` (budget disponible avant appel)
- **Source** : [gerivdb/CTULU/tools](https://github.com/gerivdb/CTULU/tree/main/tools)
- **Lien CITIZENS** : vérifier `gerivdb/CITIZENS` pour les citizens CTULU enregistrés (`citizen-anything`)
