---
name: nexus-reformer
description: "Refactoring, migration, cleanup, extraction of responsibilities. Use when user mentions 'refactoring', 'migration', 'nettoyage résidus', 'extraction'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
|
# NEXUS Reformer

## Domaine et périmètre

Ce skill couvre le **refactoring et la migration** dans l'écosystème gerivdb :
- Refactoring de la structure des dépôts (scission, fusion, renommage)
- Migration de responsabilités entre dépôts (ex: agent Python de NEXUS → BRAIN)
- Nettoyage des résidus (fichiers obsolètes, branches mortes, configs périmées)
- Extraction de composants vers des dépôts dédiés

## Méthodologie

### Phase 1 : Diagnostic
- Identifier les anomalies structurelles (fichiers hors place, dépendances circulaires).
- Mesurer l'impact du refactoring (dépendants, risques, effort).
- Planifier les étapes (ordre, rollback, validation).

### Phase 2 : Exécution
- Effectuer le refactoring étape par étape.
- Committer chaque étape séparément (traçabilité).
- Mettre à jour les références croisées (imports, docs, configs).

### Phase 3 : Validation
- Vérifier que les tests passent après chaque étape.
- Valider la conformité NEXUS post-refactoring.
- Documenter les changements dans les ADR.

## Règles de décision
- **Règle 1** : Tout refactoring d'un dépôt P0 nécessite une validation φ-CPS.
- **Règle 2** : Chaque étape de refactoring = un commit distinct (pas de commit massif).
- **Règle 3** : Toujours conserver un rollback possible (branche de backup).

## Format de sortie

```markdown
## Plan de Refactoring
- Dépôt : [nom]
- Anomalies détectées : [N]
- Étapes : [liste]
- Risque : [faible | moyen | élevé]
- Rollback : [branche de backup]
```

## Exemples d'utilisation
- "Refactorise NEXUS — extraire les agents vers BRAIN" → Planifier et exécuter.
- "Nettoie les résidus dans DevTools" → Scanner et supprimer.
- "Fusionne les dépôts X et Y" → Planifier la migration.

## Intégration avec l'écosystème
- Dépôts concernés : NEXUS, BRAIN, DevTools, tous les dépôts gerivdb
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS], [À_VALIDER_NEXUS]
