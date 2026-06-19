---
type: skill
version: "1.0.1"
date: "2026-06-19"
intent_hash: 0xCTULU_TOOL_SELECTOR_phi1.000
status: active
trit_primitive: TritSelectTool
tags: [ctulu, tool-routing, anything-suite, decision-matrix, l3-tooling]
layer: "L3_TOOLING"
nexusTags: ["CONFORME_NEXUS", "CTULU", "TOOL_ROUTING"]
slotWeight: 1
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 — gap ctulu tool routing detecte session ECOS-CLI"}
  - {v: "1.0.1", date: "2026-06-19", notes: "Harmonisation intent_hash phi convention (phi vs φ unicode)"}
---

# ctulu-tool-selector

## Purpose

Guide de sélection des outils **CTULU / Anything Suite** selon le contexte de la tâche, l'ENV actif et le budget tool_calls disponible. Fournit une matrice de décision `[tâche] × [ENV] × [budget]` → `[outil recommandé + fallback]`. Déclenche `ctulu-tool-factory` si l'outil manque.

## Trigger

Utiliser quand :
- décision "quel outil utiliser pour X ?"
- mention "Anything Suite", "CTULU disponible", "tool routing"
- tâche multi-repo dépassant le périmètre MCP natif
- opération batch, audit, drift, intent qui n'est pas un CRUD GitHub simple

## Inventaire CTULU — 17 familles (~120 outils)

| Famille | Périmètre | Exemples |
|---|---|---|
| `repo-*` | Opérations multi-repo | repo-scanner, repo-diff, repo-batch-clone |
| `audit-*` | Audits conformité | audit-structure, audit-drift, audit-strata |
| `intent-*` | Gestion intentions | intent-resolver, intent-hash-gen, intent-check |
| `kiva-*` | Pipeline KIVA | kiva-status, kiva-merge-check, kiva-wal-reader |
| `nexus-*` | Opérations NEXUS | nexus-sync, nexus-validate, nexus-map-gen |
| `citizen-*` | Gestion citoyens | citizen-register, citizen-phi-update |
| `branch-*` | Gestion branches | branch-list-orphan, branch-cleanup-batch |
| `prd-*` | PRD / EPIC | prd-validate, prd-intent-check |
| `adr-*` | ADR lifecycle | adr-create, adr-status-update |
| `diff-*` | Analyse diffs | diff-cross-repo, diff-semantic |
| `env-*` | Détection ENV | env-probe, env-capability-matrix |
| `phi-*` | Calcul φ-CPS | phi-compute, phi-aggregate-update |
| `strata-*` | Audit strates L | strata-align-check, strata-audit |
| `skill-*` | Gestion skills | skill-inventory, skill-gap-detect |
| `hook-*` | Hooks git | hook-status, hook-run-dry |
| `format-*` | Normalisation | format-yaml-frontmatter, format-intent-hash |
| `report-*` | Rapports | report-session, report-passe-summary |

## Matrice de décision

### Règle primaire

```
mcp_github   →  CRUD GitHub natif (branches, PR, fichiers, commits)
CTULU        →  logique métier, batch multi-repo, audit, drift, intent
fetch_url    →  fallback lecture seule si budget tool_calls épuisé
shell local  →  ENV2/ENV3 uniquement
```

### Matrice complète

| Tâche | ENV1 (Perplexity MCP) | ENV2 (Kilo local) | Fallback |
|---|---|---|---|
| Lire fichier repo | `mcp_github get_file_contents` | CTULU `repo-read` | `fetch_url` raw.githubusercontent |
| Lister branches | `mcp_github list_branches` | CTULU `branch-list-orphan` | — |
| Créer PR | `mcp_github create_pull_request` | CTULU `kiva-merge-check` + gh CLI | — |
| Audit drift multi-repo | CTULU `audit-drift` (via tool_call) | CTULU direct | — |
| Calculer φ-CPS | CTULU `phi-compute` | CTULU direct | lecture manuelle ARGUS |
| Valider conformité NEXUS | CTULU `nexus-validate` | CTULU direct | skill `nexus-compliance` |
| Détecter gap skills | CTULU `skill-gap-detect` | CTULU direct | analyse manuelle |
| Normaliser intent_hash | CTULU `format-intent-hash` | CTULU direct | édition manuelle |
| Inventaire repos | `known_repositories.yaml` (GATE-2) | idem | INTERDIT: scan API GitHub |
| Créer branche feature | `mcp_github create_branch` | gh CLI | — |

## Protocole de sélection

### Étape 1 — Identifier la tâche

```
[TOOL_SELECTOR] Tâche: {description}
[TOOL_SELECTOR] Type: CRUD_GITHUB | LOGIQUE_METIER | AUDIT | BATCH | INTENT
```

### Étape 2 — Vérifier ENV + budget

```
[TOOL_SELECTOR] ENV: ENV1 | ENV2 | ENV3
[TOOL_SELECTOR] Budget tool_calls restants: N
[TOOL_SELECTOR] CTULU disponible: OUI | NON (vérifier gerivdb/CTULU/tools)
```

### Étape 3 — Sélectionner + fallback

```
[TOOL_SELECTOR] Outil sélectionné: {outil} ({famille})
[TOOL_SELECTOR] Fallback si indisponible: {fallback}
[TOOL_SELECTOR] Si manquant: déclencher ctulu-tool-factory
```

## Intégration écosystème

- **Précède** : `ctulu-result-integrator` (normalise la sortie de l'outil choisi)
- **Déclenche** : `ctulu-tool-factory` si l'outil manque dans CTULU/tools
- **Complèmente** : `llm-tool-budget-guard` (contrainte budget avant sélection)
- **Référence** : `gerivdb/CTULU/tools` pour l'inventaire temps-réel
- **Lien CITIZENS** : un citoyen `tool-registry-reader` dans CITIZENS exposerait cet inventaire dynamiquement
