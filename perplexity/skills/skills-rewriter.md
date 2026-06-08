---
name: skills-rewriter
version: "1.0.0"
description: "Reformulation des intents en sous-quêtes atomiques optimisées pour le retrieval dans le MANIFEST. Équivalent adapté du Query Rewriter de Google Agentic RAG. Transforme chaque intent en sous-quêtes recherchables dans les triggers/descriptions des skills. Utiliser quand l'utilisateur mentionne 'reformuler', 'sous-quêtes', 'REWRITER', 'query rewrite', 'optimiser requête', 'atomiser intent'."
triggers:
  - "reformuler"
  - "sous-quêtes"
  - "REWRITER"
  - "query rewrite"
  - "optimiser requête"
  - "atomiser intent"
  - "enrichir intent"
  - "décomposer intent"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SKILLS_AGENTIC"]
prerequisites:
  - "MANIFEST.json (SKILLS)"
  - "skills-agentic.md (orchestrateur)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Version initiale — reformulation intents → sous-quêtes"}
trit_primitive: TritDocumentClassify
---

# SKILLS_REWRITER — Reformulation des Intents

## Domaine et périmètre

Ce skill est le **Query Rewriter** du pipeline SKILLS_AGENTIC v2. Il prend chaque intent produit par le PARSER et le reformule en **sous-quêtes atomiques** optimisées pour la recherche dans le MANIFEST des skills.

**Inspiration** : Google Query Rewriter — transforme *"What's up with Project X?"* en *"Status report for Project X Q3"* et *"Key blockers for Project X team."*

**Différence avec le PARSER** :
- Le PARSER **décompose** la requête en intents (ex: `audit_structure`)
- Le REWRITER **reformule** chaque intent en sous-quêtes recherchables (ex: `scan_repo_structure`, `check_ddd_compliance`, `detect_epic_size_violations`)

## Méthodologie

### Phase 1 — Réception des intents

Recevoir la liste d'intents du PARSER :
```json
[
  {"action": "audit_structure", "scope": "FLUENCE", "strate": "L1"},
  {"action": "verifier_conformite", "scope": "NEXUS", "strate": "L0"},
  {"action": "generer_rapport", "scope": "FLUENCE", "strate": "L1"}
]
```

### Phase 2 — Reformulation en sous-quêtes

Pour chaque intent :

1. **Charger le MANIFEST.json** — lister tous les skills avec leurs `triggers` et `description`
2. **Matcher l'intent aux skills** — trouver les skills dont les `triggers` ou `description` correspondent à l'intent
3. **Générer les sous-quêtes** — créer des sous-quêtes atomiques à partir des skills matchés
4. **Vérifier la couverture** — chaque sous-quête doit correspondre à un skill existant

### Phase 3 — Validation des sous-quêtes

Pour chaque sous-quête générée :
1. **Existence** : le skill correspondant existe-t-il dans le MANIFEST ?
2. **Activité** : le skill est-il en status `active` ?
3. **Strate** : le skill est-il dans la bonne strate L0-L9 pour le scope ?
4. **Unicité** : pas de doublons de sous-quêtes

### Phase 4 — Sortie structurée

```json
{
  "original_intent": "audit_structure",
  "scope": "FLUENCE",
  "strate": "L1",
  "sub_queries": [
    {"query": "scan_repo_structure", "skill": "reposcope-run", "match_confidence": "HIGH"},
    {"query": "check_ddd_compliance", "skill": "nexus-auditor", "match_confidence": "HIGH"},
    {"query": "detect_epic_size_violations", "skill": "nexus-auditor", "match_confidence": "MEDIUM"},
    {"query": "validate_naming_conventions", "skill": "nexus-compliance", "match_confidence": "MEDIUM"}
  ],
  "coverage": "4/4 sous-quêtes matchées"
}
```

## Règles de décision

- **Règle 1** : Maximum 5 sous-quêtes par intent (au-delà → découper en sous-intents)
- **Règle 2** : Chaque sous-quête doit matcher un skill `active` dans le MANIFEST
- **Règle 3** : Si aucun skill ne match un intent → signaler au PLANNER comme "intent non couvrable"
- **Règle 4** : Privilégier les matchs HIGH (triggers exacts) sur MEDIUM (description)
- **Règle 5** : Conserver le mapping intent → sous-quêtes pour la traçabilité
- **Règle 6** : Si un intent est déjà atomique (1 seul skill matché) → pas de reformulation nécessaire

## Format de sortie

```markdown
## SKILLS_REWRITER — Rapport de reformulation

### Intent : [action] ([scope])
- Sous-quêtes générées : [N]
- Skills matchés : [liste]
- Couverture : [N]/[N]

| Sous-quête | Skill | Confiance |
|------------|-------|-----------|
| scan_repo_structure | reposcope-run | HIGH |
| check_ddd_compliance | nexus-auditor | HIGH |
| ... | ... | ... |

### Intents non couvrables
[Liste des intents sans skill matché]
```

## Exemples de reformulation

### Exemple 1 : Audit structurel
```
Intent : audit_structure (FLUENCE)
Sous-quêtes :
  - scan_repo_structure → reposcope-run
  - check_ddd_compliance → nexus-auditor
  - detect_epic_size_violations → nexus-auditor
  - validate_naming_conventions → nexus-compliance
```

### Exemple 2 : Vérification conformité
```
Intent : verifier_conformite (NEXUS)
Sous-quêtes :
  - validate_adr_format → adr-manager
  - check_phi_cps_threshold → nexus-monitor
  - audit_branch_governance → nexus-compliance
  - verify_hooks_installed → (skill existant)
```

### Exemple 3 : Génération de rapport
```
Intent : generer_rapport (FLUENCE)
Sous-quêtes :
  - compile_audit_results → workflow-orchestration
  - format_prd_output → prd-factory
  - publish_to_brain → reposcope-publish
```

## Intégration avec l'écosystème

- **Dépôts concernés** : SKILLS (MANIFEST.json)
- **Couche EECS** : L4_ORCHESTRATION
- **Skills dépendants** : skills-agentic.md (orchestrateur), skills-coverage.md (vérificateur)
- **Tags NEXUS** : [CONFORME_NEXUS], [SKILLS_AGENTIC]

## Contraintes

| Contrainte | Valeur |
|------------|--------|
| Max sous-quêtes par intent | 5 |
| Skills matchés | status = `active` uniquement |
| Confiance minimum | MEDIUM |
| Traçabilité | Mapping intent → sous-quêtes conservé |
