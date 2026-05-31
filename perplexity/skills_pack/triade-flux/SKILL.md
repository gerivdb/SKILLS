---
name: triade-flux
description: "FLUX review, HITL promotion, assimilation into NEXUS. Use when user mentions 'FLUX', 'review', 'HITL', 'promotion'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
# Triade FLUX

## Domaine et périmètre

La Triade Cognitive est le pipeline de veille et d'assimilation. Ce skill couvre :
- FLUX : la review HITL (Human-In-The-Loop)
- La promotion des signaux validés vers NEXUS
- L'assimilation finale dans l'écosystème

## Méthodologie

### Phase 1 : Diagnostic
- Vérifier que les signaux ont bien été qualifiés par KRONOS.
- Lister les signaux en attente de review dans FLUX.
- Contrôler l'état du workflow flux-review.yml.

### Phase 2 : Revue
- Exécuter `python src/reviewer.py --review` pour ouvrir la session HITL.
- Pour chaque signal, lire le diff, évaluer la pertinence.
- Approuver, rejeter ou demander un complément.

### Phase 3 : Promotion
- Les signaux approuvés sont déplacés vers NEXUS/intelligence/signals/assimilated/.
- Mettre à jour le registre ECOS_ROOT si nécessaire.
- Clôturer la session de review.

## Règles de décision
- **Règle 1** : Ne jamais approuver un signal sans avoir lu le diff.
- **Règle 2** : Les signaux HIGH doivent être traités en priorité.
- **Règle 3** : Un signal rejeté deux fois est définitivement écarté.

## Format de sortie

```markdown
## Revue FLUX
| Signal ID | Décision | Justification |
|-----------|----------|---------------|
| RS-001    | APPROVED | Flag pertinent |
| RS-002    | REJECTED | Doublon        |
```

## Exemples d'utilisation
- "Fais la revue HITL des signaux en attente" → Lister et approuver/rejeter.
- "Pourquoi ce signal a-t-il été rejeté ?" → Afficher l'historique.

## Intégration avec l'écosystème
- Dépôts concernés : FLUX, KRONOS, NEXUS
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS], [HYPOTHÈSE_NON_CONFIRMÉE]
