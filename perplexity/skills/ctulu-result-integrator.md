---
type: skill
version: "1.0.1"
date: "2026-06-19"
intent_hash: 0xCTULU_RESULT_INTEGRATOR_phi1.000
status: active
trit_primitive: TritNormalizeOutput
tags: [ctulu, output-normalization, anything-suite, passe-integration, context]
layer: "L3_TOOLING"
nexusTags: ["CONFORME_NEXUS", "CTULU", "OUTPUT_NORMALIZATION"]
slotWeight: 1
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 — gap integration output CTULU detecte session ECOS-CLI"}
  - {v: "1.0.1", date: "2026-06-19", notes: "Harmonisation intent_hash phi convention (phi vs φ unicode)"}
---

# ctulu-result-integrator

## Purpose

Protocole d'**intégration des résultats** d'outils CTULU / Anything Suite dans la séquence de passes active. Normalise les sorties (JSON, Markdown, diff, YAML, logs) en format consommable par la passe suivante. Émet un stash contextuel si la sortie dépasse 2k tokens. Inclut une vérification secrets avant intégration.

## Trigger

Utiliser quand :
- résultat d'un outil CTULU/Anything Suite reçu
- besoin d'intégrer une sortie outil externe dans un rapport de passe
- normalisation d'une sortie JSON/diff/log vers Markdown structuré
- output > 2k tokens à condenser avant passage à la passe suivante

## Formats de sortie reconnus

| Format | Traitement | Sortie normalisée |
|---|---|---|
| JSON | Extraire clés pertinentes, flatten si profondeur > 3 | Table Markdown |
| YAML frontmatter | Valider champs requis, émettre diff si anomalie | Block code + delta |
| Unified diff | Parser hunks, identifier fichiers impactés | Table fichiers + résumé |
| Logs shell | Filtrer ERROR/WARN/INFO, éliminer verbosité | Bullet list niveaux |
| Markdown raw | Vérifier headers, extraire sections clés | Condensé ≤ 500 tokens |
| CSV/TSV | Convertir en table Markdown (max 20 lignes) | Table + note pagination |
| Binaire/opaque | Ne pas intégrer, émettre HITL gate | Alerte HITL |

## Protocole d'intégration

### Étape 1 — Réception et classification

```
[INTEGRATOR] Outil source: {outil CTULU}
[INTEGRATOR] Format détecté: JSON | YAML | DIFF | LOG | MD | CSV | BINAIRE
[INTEGRATOR] Taille estimée: {N} tokens
[INTEGRATOR] Scan secrets: REQUIS | SKIP (si pas de contenu sensible potentiel)
```

### Étape 2 — Scan secrets (si requis)

```
Si output contient : clés API, tokens, passwords, credentials potentiels
→ Déclencher run_secret_scanning avant toute intégration
→ Si secret détecté : STOP, émettre HITL gate, ne PAS inclure dans rapport
→ Si clean : continuer
[INTEGRATOR] Secret scan: CLEAN | DETECTED (HITL)
```

### Étape 3 — Normalisation

```
[INTEGRATOR] Normalisation: {format} → Markdown structuré
[INTEGRATOR] Condensation: {N tokens} → {M tokens} ({ratio}%)
```

Si output > 2k tokens :
```
[INTEGRATOR] STASH: output complet → contextual-stash-manager
[INTEGRATOR] Résumé injecté dans passe: ≤ 200 tokens
[INTEGRATOR] Référence stash: STASH_{timestamp}
```

### Étape 4 — Injection dans rapport de passe

```
[INTEGRATOR] Injection: section "Résultat {outil}" dans rapport passe N
[INTEGRATOR] Format final: {format choisi}
[INTEGRATOR] Statut: INTEGRE | STASHE | HITL_GATE
```

## Cas d'erreur

| Erreur | Action |
|---|---|
| Outil retourne code erreur | Logger, émettre WARN, continuer si non-bloquant |
| Output vide | Vérifier si outil a tourné, sinon retry 1x |
| Format non reconnu | Traiter comme opaque, émettre HITL si critique |
| Secret détecté | STOP + HITL gate obligatoire |
| Timeout outil | Marquer passe comme partielle, documenter état |

## Intégration écosystème

- **Précédé par** : `ctulu-tool-selector` (choix de l'outil)
- **Utilise** : `contextual-stash-manager` (si output > 2k tokens)
- **Déclenche** : `hitl-gate-emitter` (si secret ou format opaque critique)
- **Alimente** : `adaptive-passe-sequencer` (résumé normalisé pour état inter-passes)
- **Référence** : `run_secret_scanning` (MCP tool, scan avant intégration)
