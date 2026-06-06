---
name: skills-coverage
version: "2.0.0"
description: "Vérificateur de couverture fonctionnelle v2 pour le pipeline SKILLS_AGENTIC. Évalue si l'ensemble des skills sélectionnés couvre tous les intents (4 critères). Produit un brouillon intermédiaire (Draft Agent) et un feedback ciblé sur les pièces manquantes (Gap Analyzer). Équivalent enrichi du Sufficient Context Agent de Google. Utiliser quand l'utilisateur mentionne 'couverture', 'gap skills', 'vérifier couverture', 'COVERAGE Agent', 'sufficient context', 'brouillon', 'draft', 'gap analyzer', 'pièces manquantes'."
triggers:
  - "couverture"
  - "gap skills"
  - "vérifier couverture"
  - "COVERAGE Agent"
  - "sufficient context"
  - "compétence manquante"
  - "skill manquant"
  - "brouillon"
  - "draft"
  - "gap analyzer"
  - "pièces manquantes"
  - "feedback ciblé"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SKILLS_AGENTIC"]
prerequisites:
  - "MANIFEST.json (SKILLS)"
  - "skills-agentic.md (orchestrateur)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-06", notes: "Version initiale — 4 critères de couverture"}
  - {v: "2.0.0", date: "2026-06-07", notes: "v2 — + Draft Agent (brouillon intermédiaire) + Gap Analyzer (feedback ciblé)"}
---

# SKILLS_COVERAGE v2 — Vérificateur de Couverture Fonctionnelle

## Domaine et périmètre

Ce skill est le **gardien de qualité** du pipeline SKILLS_AGENTIC v2. Il évalue si l'ensemble des skills sélectionnés par le PLANNER couvre **tous les intents** de la requête. La v2 ajoute le **Draft Agent** (brouillon intermédiaire) et le **Gap Analyzer** (feedback ciblé sur les pièces manquantes).

**3 composants** :
1. **Coverage Checker** (4 critères) — vérifie exhaustivité, compétence, strate, dépendance
2. **Draft Agent** (nouveau v2) — produit un brouillon de réponse avant exécution
3. **Gap Analyzer** (nouveau v2) — compare le brouillon à la requête et génère un feedback ciblé

**Différence fondamentale avec Google** : Google vérifie si le contexte informationnel est suffisant. Nous, on vérifie si l'ensemble de skills activés est suffisant **et** on produit un brouillon pour identifier exactement ce qui manque.

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

## Méthodologie v2

### Phase 1 — Collecte des données

1. Recevoir le plan routé du ROUTER (skills + repos + strates)
2. Recevoir les intents originaux du PARSER
3. Recevoir les sous-quêtes du REWRITER (v2)
4. Charger le `MANIFEST.json` pour les métadonnées des skills
5. Charger `known_repositories.yaml` pour les strates des repos

### Phase 2 — Évaluation des 4 critères (Coverage Checker)

Pour chaque critère :
1. Appliquer la méthode décrite ci-dessus
2. Produire un verdict partiel : PASS / FAIL
3. En cas de FAIL, lister les gaps identifiés

### Phase 3 — Verdict global (Coverage Checker)

```
Si les 4 critères PASS → verdict = SUFFICIENT
Si au moins 1 critère FAIL → verdict = INSUFFICIENT
```

### Phase 4 — Draft Agent (nouveau v2)

**Objectif** : Produire un brouillon de réponse basé sur les skills activés, avant l'exécution réelle.

**Déclenchement** : Systématique pour les requêtes de niveau 2 et 3.

**Méthode** :
1. Pour chaque skill du plan, générer une section de brouillon basée sur la `description` du skill
2. Identifier les intents couverts et les intents non couverts
3. Produire un brouillon structuré

**Format du brouillon** :
```markdown
## Brouillon — [Titre]

### Couverture
- Skills activés : [liste]
- Intents couverts : [liste]
- Intents non couverts : [liste]

### Résultats attendus
#### [skill-1] — [intent]
- Résultat attendu : [description basée sur la description du skill]
- Source : [repo]

#### [skill-2] — [intent]
...

### Lacunes identifiées
[Liste des intents sans skill assigné]
```

### Phase 5 — Gap Analyzer (nouveau v2)

**Objectif** : Comparer le brouillon à la requête originale et générer un feedback ciblé sur les pièces manquantes.

**Méthode** :
1. Comparer chaque section du brouillon à l'intent correspondant
2. Identifier les pièces manquantes (intents non couverts, compétences manquantes)
3. Recommander des skills spécifiques pour combler les gaps
4. Générer un feedback structuré et ciblé

**Format du feedback ciblé** :
```json
{
  "coverage_verdict": "INSUFFICIENT",
  "draft_summary": "Le brouillon couvre l'audit structurel et la conformité NEXUS",
  "missing_pieces": [
    {
      "intent": "generer_rapport",
      "reason": "Aucun skill de génération de rapport n'est activé",
      "recommended_skills": ["workflow-orchestration", "prd-factory"],
      "priority": "HIGH",
      "targeted_feedback": "Le skill reposcope-run couvre l'audit structurel, mais il manque un skill pour générer le rapport final. Ajouter workflow-orchestration (L4) ou prd-factory (L2)."
    }
  ],
  "draft_quality": "PARTIAL",
  "iteration_recommendation": "Ajouter workflow-orchestration au plan et relancer la vérification"
}
```

### Phase 6 — Génération du feedback pour l'ITERATOR

Si INSUFFICIENT :
1. Combiner les résultats du Coverage Checker + Draft Agent + Gap Analyzer
2. Générer un feedback structuré pour l'ITERATOR
3. Le feedback inclut : verdict, brouillon, pièces manquantes, skills recommandés

Si SUFFICIENT :
1. Transmettre le brouillon au FANOUT comme référence
2. Passer à l'exécution

## Règles de décision

- **Règle 1** : Un intent sans skill assigné = gap d'exhaustivité → INSUFFICIENT
- **Règle 2** : Un skill avec `status: deprecated` ou `status: archived` ne peut pas couvrir un intent
- **Règle 3** : Un skill L0 ne peut pas dépendre d'un skill L3+ (violation de strate)
- **Règle 4** : Si un skill a des `prerequisites` non satisfaits → gap de dépendance
- **Règle 5** : En cas de doute sur la compétence → consulter la `description` du skill dans le MANIFEST
- **Règle 6** : Le verdict doit être binaire (SUFFICIENT / INSUFFICIENT) — pas de "partiel"

## Format de sortie v2

```markdown
## SKILLS_COVERAGE v2 — Rapport de couverture

### Verdict : [SUFFICIENT / INSUFFICIENT]

### Critères
| Critère | Verdict | Détails |
|---------|---------|---------|
| Exhaustivité | [PASS / FAIL] | [Détails] |
| Compétence | [PASS / FAIL] | [Détails] |
| Strate | [PASS / FAIL] | [Détails] |
| Dépendance | [PASS / FAIL] | [Détails] |

### Brouillon (Draft Agent)
[Structure du brouillon]

### Pièces manquantes (Gap Analyzer)
| Intent | Raison | Skills recommandés | Priorité |
|--------|--------|--------------------|----------|
| ... | ... | ... | ... |

### Feedback ciblé
[Feedback structuré pour l'ITERATOR avec skills recommandés]
```

## Intégration avec l'écosystème

- **Dépôts concernés** : SKILLS (MANIFEST.json), GOVERNANCE-HUB (known_repositories.yaml)
- **Couche EECS** : L4_ORCHESTRATION
- **Skills dépendants** : skills-agentic.md (orchestrateur), skills-router.md (routeur), skills-rewriter.md (rewriter)
- **Tags NEXUS** : [CONFORME_NEXUS], [SKILLS_AGENTIC]

## Contraintes

| Contrainte | Valeur |
|------------|--------|
| Seuil d'exhaustivité | 100% |
| Seuil de compétence | 100% |
| Seuil de strate | 100% |
| Seuil de dépendance | 100% |
| Verdict | Binaire (SUFFICIENT / INSUFFICIENT) |
| Brouillon | Systématique pour niveaux 2 et 3 |
| Feedback ciblé | Skills recommandés avec priorité |
| Max skills recommandés par gap | 3 |
