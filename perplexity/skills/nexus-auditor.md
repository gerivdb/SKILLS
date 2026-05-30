---
name: nexus-auditor
description: "Audit repository structure against DDD criteria, EPIC size, violations. Use when user mentions 'audit structure', 'DDD', 'EPIC volumineuse', 'taille'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]---
|
# NEXUS Auditor

## Domaine et périmètre

Ce skill couvre l'**audit de structure des dépôts** selon les critères DDD :
- Audit de la structure des dépôts gerivdb (contextes bornés, autonomie, cohésion)
- Détection des EPICs volumineuses (> 10 Ko = spécification technique, pas un plan)
- Vérification des violations de REPO-STANDARDS
- Évaluation de la conformité DDD (Domain-Driven Design)

## Méthodologie

### Phase 1 : Scan de la structure
- Lister les fichiers et répertoires du dépôt.
- Mesurer la taille des EPICs et PRD.
- Détecter les fichiers hors place (ex: `.py` à la racine de NEXUS).

### Phase 2 : Analyse DDD
- Évaluer les contextes bornés (chaque dépôt = un contexte).
- Vérifier l'autonomie (dépendances minimales entre dépôts).
- Contrôler la cohésion (fichiers liés dans le même dépôt).

### Phase 3 : Rapport et recommandations
- Lister les violations avec sévérité (bloquant, majeur, mineur).
- Proposer des corrections (déplacement, scission, fusion).
- Tagger selon la conformité NEXUS.

## Règles de décision
- **Règle 1** : Un EPIC > 10 Ko dans NEXUS doit être externalisé vers un dépôt dédié.
- **Règle 2** : Tout fichier `.py` à la racine de NEXUS est un agent égaré → migrer vers BRAIN.
- **Règle 3** : Les configs d'outillage (`.kilo`, `.mcp`, `.rules`) doivent résider dans DevTools.

## Format de sortie

```markdown
## Audit DDD — [dépôt]
- Conformité : [conforme | violations]
- EPICs volumineuses : [N]
- Fichiers hors place : [N]
- Violations bloquantes : [N]
- Recommandations : [liste]
```

## Exemples d'utilisation
- "Audite la structure de NEXUS" → Scan complet + rapport DDD.
- "Cette EPIC est-elle trop volumineuse ?" → Mesurer et évaluer.
- "Quels fichiers sont hors place dans FLUENCE ?" → Lister les violations.

## Intégration avec l'écosystème
- Dépôts concernés : NEXUS, REPO-STANDARDS, tous les dépôts gerivdb
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS], [À_VALIDER_NEXUS]
