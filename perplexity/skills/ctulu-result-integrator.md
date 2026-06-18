---
type: skill
version: "1.0.0"
date: "2026-06-18"
intent_hash: 0xCTULU_RESULT_INTEGRATOR_φ1.000
status: active
trit_primitive: TritNormalizeOutput
tags: [ctulu, output-normalization, anything-suite, pass-integration, stash]
layer: "L3_TOOLING"
nexusTags: ["CONFORME_NEXUS", "CTULU", "OUTPUT_NORMALIZATION"]
slotWeight: 1
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 ECOS-CLI — gap normalisation output CTULU dans séquence de passes"}
---

# ctulu-result-integrator

## Purpose

Normalise les sorties d'outils CTULU/Anything Suite pour les rendre **consommables par la passe LLM suivante**. Distingue les formats de sortie (JSON, YAML, markdown, diff, texte brut) et applique le protocole d'intégration adapté : inline dans le contexte, stash différé, ou sérialisation fichier.

## Trigger

Utiliser quand :
- un outil CTULU/Anything Suite vient de répondre
- la sortie dépasse ~2k tokens
- la sortie doit être passée à la passe N+1
- le format de sortie ne correspond pas au format attendu par la passe suivante
- besoin de normaliser un diff, un rapport JSON ou un YAML pour l'intégrer dans un rapport markdown

## Formats de sortie CTULU reconnus

| Format | Source typique | Traitement |
|---|---|---|
| JSON plat | `audit-anything`, `scan-anything`, `drift-detect` | Extraire les champs clés, formater en table markdown |
| YAML frontmatter | `frontmatter-guard`, `conform-anything` | Valider les champs requis, émettre diff si écart |
| Diff unifié | `diff-anything`, `patch-anything` | Résumer : N fichiers, +X/-Y lignes, lister les écarts critiques |
| Markdown rapport | `plan-anything`, `adr-anything` | Passer inline si < 2k tokens, sinon stash + référence |
| Liste brute | `branch-cleaner`, `batch-anything` | Convertir en tableau markdown avec statut par item |
| Graphe JSON | `intent-graph-builder`, `graph-builder` | Résumer : N nœuds, M arêtes, clusters détectés |
| Code / script | `scaffold-anything`, `workflow-anything` | Vérifier syntaxe, extraire structure, ne pas inclure inline |

## Protocole d'intégration

### Étape 1 — Mesurer la sortie

```
[CTULU_INTEGRATOR] Outil source: {outil}
[CTULU_INTEGRATOR] Format détecté: {JSON|YAML|diff|markdown|liste|graphe|code}
[CTULU_INTEGRATOR] Taille estimée: {N} tokens
[CTULU_INTEGRATOR] Destination: passe {N+1} — {objectif}
```

### Étape 2 — Appliquer la stratégie

```
Si taille ≤ 500 tokens:
  → INTÉGRATION INLINE — inclure directement dans le contexte de passe N+1

Si 500 < taille ≤ 2000 tokens:
  → INTÉGRATION RÉSUMÉE — résumer en ≤ 200 tokens + conserver référence complète

Si taille > 2000 tokens:
  → STASH CONTEXTUEL
     1. Appeler skill contextual-stash-manager
     2. Émettre référence stash: [STASH:{id}]
     3. Passe N+1 reçoit uniquement: stash_id + résumé 100 tokens
```

### Étape 3 — Normaliser selon le format cible

**JSON → Markdown table :**
```
[à partir de]
{"repos": [{"name": "ECOS-CLI", "score": 0.87}, ...]}

[émettre]
| Repo | Score | Statut |
|---|---|---|
| ECOS-CLI | 0.87 | ✅ OK |
```

**Diff → Résumé :**
```
[à partir de]
--- a/file.py +++ b/file.py @@ -12,4 +12,6 @@...

[émettre]
[DIFF_SUMMARY] 1 fichier modifié | +6 / -4 lignes | section: init_config
```

**Liste brute → Tableau statut :**
```
[à partir de]
branch-1 deleted
branch-2 deleted
branch-3 error: not found

[émettre]
| Branche | Statut |
|---|---|
| branch-1 | ✅ Supprimée |
| branch-2 | ✅ Supprimée |
| branch-3 | ❌ Erreur: not found |
```

### Étape 4 — Émettre le bloc d'intégration

```
[CTULU_INTEGRATOR] ✅ Sortie normalisée
[CTULU_INTEGRATOR] Format émis: {markdown_table|inline|stash_ref}
[CTULU_INTEGRATOR] Prêt pour: passe {N+1} — {objectif}
[CTULU_INTEGRATOR] Données perdues: {aucune|{liste des champs écartés}}
```

## Cas d'erreur

| Situation | Action |
|---|---|
| Sortie vide ou `null` | Émettre `[CTULU_INTEGRATOR] ⚠️ SORTIE VIDE` + vérifier si l'outil a échoué silencieusement |
| Format non reconnu | Traiter comme texte brut, stasher si > 1k tokens |
| Sortie JSON malformé | Tenter parsing partiel + signaler les champs manquants |
| Sortie contient des secrets | Déclencher `run_secret_scanning` avant intégration |

## Intégration écosystème

- **Précédé par** : `ctulu-tool-selector` (sélection de l'outil)
- **Complémente** : `contextual-stash-manager` (stash si sortie volumineuse)
- **Complémente** : `adaptive-passe-sequencer` (passe N+1 reçoit la sortie normalisée)
- **Déclenche si nécessaire** : `run_secret_scanning` (secrets potentiels dans la sortie)
- **Source CTULU** : [gerivdb/CTULU/tools](https://github.com/gerivdb/CTULU/tree/main/tools)
