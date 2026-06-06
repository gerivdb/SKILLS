---
name: skills-coverage
version: "1.0.0"
description: "Vérificateur de couverture fonctionnelle pour le pipeline SKILLS_AGENTIC. Évalue si l'ensemble des skills sélectionnés couvre tous les intents d'une requête. Détecte les gaps de compétences et génère le feedback d'itération. Équivalent adapté du Sufficient Context Agent de Google pour le métacluster gerivdb. Utiliser quand l'utilisateur mentionne 'couverture', 'gap skills', 'vérifier couverture', 'COVERAGE Agent', 'sufficient context'."
triggers:
  - "couverture"
  - "gap skills"
  - "vérifier couverture"
  - "COVERAGE Agent"
  - "sufficient context"
  - "compétence manquante"
  - "skill manquant"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SKILLS_AGENTIC"]
prerequisites:
  - "MANIFEST.json (SKILLS)"
  - "skills-agentic.md (orchestrateur)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-06", notes: "Version initiale — 4 critères de couverture"}
---

# SKILLS_COVERAGE — Vérificateur de Couverture Fonctionnelle

## Domaine et périmètre

Ce skill est le **gardien de qualité** du pipeline SKILLS_AGENTIC. Il évalue si l'ensemble des skills sélectionnés par le PLANNER couvre **tous les intents** de la requête utilisateur. C'est l'équivalent adapté du **Sufficient Context Agent** de Google — mais au lieu de vérifier la complétude des données, il vérifie la **complétude des capacités**.

**Différence fondamentale avec Google** : Google vérifie si le contexte informationnel est suffisant pour répondre. Nous, on vérifie si l'ensemble de skills activés est suffisant pour **traiter** la requête.

## Les 4 Critères de Couverture

### Critère 1 — Exhaustivité

**Question** : Chaque intent de la requête a-t-il au moins un skill assigné ?

**Méthode** :
1. Extraire la liste des intents du plan (depuis le PLANNER)
2. Pour chaque intent, vérifier qu'au moins un skill du plan le couvre
3. Un intent est "couvert" si un skill du plan a un `triggers` ou `description` qui correspond

**Seuil** : 100% des intents doivent être couverts

**Exemple de gap** :
```
Intents : [audit_structure, verifier_conformite, generer_rapport]
Skills  : [reposcope-run, nexus-auditor]
Gap     : generer_rapport → aucun skill assigné
```

### Critère 2 — Compétence

**Question** : Le skill assigné a-t-il la capacité réelle de traiter l'intention ?

**Méthode** :
1. Pour chaque intent-skill assigné, vérifier la `description` du skill dans le `MANIFEST.json`
2. Vérifier que les `triggers` du skill correspondent à l'intent
3. Vérifier que le skill n'est pas en status `deprecated` ou `archived`

**Seuil** : 100% des assignations doivent être compétentes

**Exemple de gap** :
```
Intent : audit_structure
Skill  : prd-factory
Gap    : prd-factory ne sait pas auditer une structure → compétence incorrecte
```

### Critère 3 — Strate

**Question** : Le skill est-il dans la bonne strate L0-L9 pour le repo cible ?

**Méthode** :
1. Pour chaque skill, vérifier son `layer` dans le `MANIFEST.json`
2. Vérifier la strate du repo cible (depuis `known_repositories.yaml`)
3. Règle : un skill L0 (gouvernance) ne peut pas dépendre d'un skill L3+ (outil)
4. Règle : un skill L3+ ne peut pas override un skill L0

**Seuil** : 100% des assignations doivent respecter la hiérarchie L0→L9

**Exemple de gap** :
```
Skill      : nexus-auditor (L0)
Repo cible : FLUENCE (L1)
Dépendance : reposcope-run (L3) → nexus-auditor ne peut pas dépendre de reposcope-run
```

### Critère 4 — Dépendance

**Question** : Les dépendances inter-skills sont-elles respectées ?

**Méthode** :
1. Pour chaque skill du plan, vérifier ses `prerequisites` dans le `MANIFEST.json`
2. Vérifier que les skills prérequis sont aussi dans le plan (ou déjà exécutés)
3. Vérifier l'ordre d'exécution : un skill ne peut pas s'exécuter avant ses prérequis

**Seuil** : 100% des dépendances doivent être satisfaites

**Exemple de gap** :
```
Plan : [nexus-auditor (step 1), reposcope-run (step 2)]
Gap  : nexus-auditor dépend de reposcope-run → ordre inversé
```

## Méthodologie

### Phase 1 — Collecte des données

1. Recevoir le plan routé du ROUTER (skills + repos + strates)
2. Recevoir les intents originaux du PARSER
3. Charger le `MANIFEST.json` pour les métadonnées des skills
4. Charger `known_repositories.yaml` pour les strates des repos

### Phase 2 — Évaluation des 4 critères

Pour chaque critère :
1. Appliquer la méthode décrite ci-dessus
2. Produire un verdict partiel : PASS / FAIL
3. En cas de FAIL, lister les gaps identifiés

### Phase 3 — Verdict global

```
Si les 4 critères PASS → verdict = SUFFICIENT
Si au moins 1 critère FAIL → verdict = INSUFFICIENT
```

### Phase 4 — Génération du feedback (si INSUFFICIENT)

Pour chaque gap identifié :
1. Identifier le type de gap (exhaustivité, compétence, strate, dépendance)
2. Identifier le(s) skill(s) manquant(s) ou incorrect(s)
3. Proposer un skill de remplacement (depuis le `MANIFEST.json`)
4. Générer un feedback structuré pour l'ITERATOR

**Format du feedback** :
```json
{
  "coverage_verdict": "INSUFFICIENT",
  "covered_intents": ["audit_structure", "verifier_conformite"],
  "missing_intents": ["generer_rapport"],
  "missing_skills": ["workflow-orchestration"],
  "incorrect_assignments": [],
  "strate_violations": [],
  "dependency_violations": [],
  "feedback": "Le plan couvre l'audit et la conformité, mais ne génère pas de rapport. Ajouter workflow-orchestration."
}
```

## Règles de décision

- **Règle 1** : Un intent sans skill assigné = gap d'exhaustivité → INSUFFICIENT
- **Règle 2** : Un skill avec `status: deprecated` ou `status: archived` ne peut pas couvrir un intent
- **Règle 3** : Un skill L0 ne peut pas dépendre d'un skill L3+ (violation de strate)
- **Règle 4** : Si un skill a des `prerequisites` non satisfaits → gap de dépendance
- **Règle 5** : En cas de doute sur la compétence → consulter la `description` du skill dans le MANIFEST
- **Règle 6** : Le verdict doit être binaire (SUFFICIENT / INSUFFICIENT) — pas de "partiel"

## Format de sortie

```markdown
## SKILLS_COVERAGE — Rapport de couverture

### Verdict : [SUFFICIENT / INSUFFICIENT]

### Critères
| Critère | Verdict | Détails |
|---------|---------|---------|
| Exhaustivité | [PASS / FAIL] | [Détails] |
| Compétence | [PASS / FAIL] | [Détails] |
| Strate | [PASS / FAIL] | [Détails] |
| Dépendance | [PASS / FAIL] | [Détails] |

### Gaps identifiés
[Liste des gaps avec type et skill manquant]

### Recommandation
[Feedback structuré pour l'ITERATOR]
```

## Intégration avec l'écosystème

- **Dépôts concernés** : SKILLS (MANIFEST.json), GOVERNANCE-HUB (known_repositories.yaml)
- **Couche EECS** : L4_ORCHESTRATION
- **Skills dépendants** : skills-agentic.md (orchestrateur), skills-router.md (routeur)
- **Tags NEXUS** : [CONFORME_NEXUS], [SKILLS_AGENTIC]

## Contraintes

| Contrainte | Valeur |
|------------|--------|
| Seuil d'exhaustivité | 100% |
| Seuil de compétence | 100% |
| Seuil de strate | 100% |
| Seuil de dépendance | 100% |
| Verdict | Binaire (SUFFICIENT / INSUFFICIENT) |
