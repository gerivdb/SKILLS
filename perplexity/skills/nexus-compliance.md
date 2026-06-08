---
name: nexus-compliance
description: "Branch governance, cherry-pick safety, hook validation. Use when user mentions 'conformité', 'gouvernance branche', 'cherry-pick safety'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
trit_primitive: TritEnforcePolicy
---
# NEXUS Compliance

## Domaine et périmètre

Ce skill couvre la **conformité des branches et opérations Git** :
- Gouvernance des branches (naming, lifecycle, protection)
- Cherry-pick safety (vérification avant cherry-pick entre branches)
- Validation des hooks Git (pre-commit, pre-push)
- Conformité avec REPO-STANDARDS et ADR

## Méthodologie

### Phase 1 : Audit des branches
- Lister les branches locales et distantes.
- Vérifier le naming convention (`feature/`, `fix/`, `adr-`, etc.).
- Détecter les branches orphelines ou mergées non supprimées.

### Phase 2 : Vérification des opérations
- Avant un cherry-pick : vérifier les conflits potentiels, les dépendances.
- Avant un push : valider les hooks (lint, format, tests).
- Avant un merge : vérifier la conformité de la branche source.

### Phase 3 : Correction
- Proposer le nettoyage des branches obsolètes.
- Corriger les violations de naming.
- Mettre à jour les hooks si nécessaire.

## Règles de décision
- **Règle 1** : Les branches `main`/`master` sont protégées — jamais de push direct.
- **Règle 2** : Un cherry-pick entre couches EECS différentes nécessite une validation.
- **Règle 3** : Les branches mergées depuis > 30 jours doivent être supprimées.

## Format de sortie

```markdown
## Audit Compliance
- Branches actives : [N]
- Violations naming : [N]
- Branches à nettoyer : [N]
- Hooks valides : [OK | ERREUR]
```

## Exemples d'utilisation
- "Vérifie la conformité des branches de NEXUS" → Audit complet.
- "Ce cherry-pick est-il sûr ?" → Analyser les conflits.
- "Nettoie les branches mergées" → Lister et supprimer.

## Intégration avec l'écosystème
- Dépôts concernés : tous les dépôts gerivdb
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS], [À_VALIDER_NEXUS]
