---
name: triade-hub
description: "Cognitive Triade orchestration, end-to-end test, coordination IRIS/KRONOS/FLUX. Use when user mentions 'triade cognitive', 'orchestration', 'end‑to‑end'."
---
|
# Triade Hub

## Domaine et périmètre

Ce skill couvre l'**orchestration de la Triade Cognitive** (IRIS, KRONOS, FLUX) :
- Coordination des trois composants (capteur → digesteur → review)
- Tests end-to-end (E2E) de la pipeline complète
- Monitoring de chaque étape (logs, métriques, alertes)
- Diagnostic des pannes (startup_failure, rate-limits, permissions)

## Méthodologie

### Phase 1 : Diagnostic
- Vérifier l'état de chaque composant (IRIS, KRONOS, FLUX).
- Contrôler les permissions Settings Actions du dépôt cible.
- Inspecter les logs des derniers runs.

### Phase 2 : Orchestration
- Lancer le test E2E via `Invoke-TriadeE2ETest.ps1 -Target <cible>.yaml`.
- Surveiller les workflows sur GitHub Actions.
- Attendre la complétion des trois étapes (IRIS → KRONOS → FLUX).

### Phase 3 : Revue et promotion
- Ouvrir la session HITL dans FLUX (`python src/reviewer.py --review`).
- Approuver ou rejeter les signaux.
- Vérifier l'assimilation dans NEXUS/intelligence/signals/assimilated/.

## Règles de décision
- **Règle 1** : Un startup_failure en < 2s = problème de permissions Settings.
- **Règle 2** : Ne jamais approuver un signal sans avoir lu le diff.
- **Règle 3** : Les signaux HIGH doivent être traités en priorité.

## Format de sortie

```markdown
## Statut Triade
| Composant | Statut | Run ID |
|-----------|--------|--------|
| IRIS      | ✅/❌  | [ID]   |
| KRONOS    | ✅/❌  | [ID]   |
| FLUX      | ✅/❌  | [ID]   |
```

## Exemples d'utilisation
- "Lance un test E2E sur Bun" → Orchestrer les 3 étapes.
- "Diagnostique un startup_failure sur IRIS" → Vérifier les permissions.
- "Fais la revue HITL des signaux en attente" → Ouvrir FLUX.

## Intégration avec l'écosystème
- Dépôts concernés : IRIS, KRONOS, FLUX, NEXUS, Gitnote
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS], [HYPOTHÈSE_NON_CONFIRMÉE]
