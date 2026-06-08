---
name: skills-router
version: "1.0.0"
description: "Routeur cross-repo pour le pipeline SKILLS_AGENTIC. Mappe chaque skill vers le(s) repo(s) cible(s) en utilisant known_repositories.yaml comme source de vérité. Applique les contraintes de strate L0-L9 et vérifie l'existence des repos dans le registre gerivdb. Utiliser quand l'utilisateur mentionne 'routing', 'cross-repo', 'mapper skill', 'repo cible', 'known_repositories', 'strates L0-L9'."
triggers:
  - "routing"
  - "cross-repo"
  - "mapper skill"
  - "repo cible"
  - "known_repositories"
  - "strates L0-L9"
  - "router skill"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SKILLS_AGENTIC"]
prerequisites:
  - "known_repositories.yaml (GOVERNANCE-HUB)"
  - "MANIFEST.json (SKILLS)"
  - "skills-agentic.md (orchestrateur)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-06", notes: "Version initiale — routing cross-repo avec contraintes L0-L9"}
trit_primitive: TritResolvePath
---

# SKILLS_ROUTER — Routeur Cross-Repo

## Domaine et périmètre

Ce skill est le **routeur** du pipeline SKILLS_AGENTIC. Il associe chaque skill sélectionné par le PLANNER au(x) repo(s) cible(s) approprié(s) en utilisant `known_repositories.yaml` comme source de vérité. Il applique les **contraintes de strate L0-L9** et vérifie l'existence des repos dans le registre gerivdb.

**Source de vérité** : `gerivdb/GOVERNANCE-HUB/known_repositories.yaml` (GATE-0/1/2/3 obligatoire)

## Méthodologie

### Phase 1 — Chargement du registre

1. Lire `known_repositories.yaml` depuis GOVERNANCE-HUB
2. Extraire la liste des repos avec leurs métadonnées :
   - `name` : nom du repo
   - `path` : chemin local
   - `remote` : URL GitHub
   - `strate` : L0-L9
   - `status` : active / dormant / deprecated / archived
   - `do_not_create` : verrou de création

### Phase 2 — Mapping skill → repo

Pour chaque skill du plan d'exécution :

1. **Identifier le scope** : quel repo ou domaine le skill doit-il traiter ?
2. **Chercher dans le registre** : trouver le(s) repo(s) correspondant au scope
3. **Vérifier la strate** : le repo est-il dans la bonne strate L0-L9 ?
4. **Vérifier le statut** : le repo est-il `active` ? (pas `dormant`/`deprecated`/`archived`)
5. **Enrichir le plan** : ajouter `repo`, `strate`, `path` au plan

### Phase 3 — Application des contraintes de strate

**Règles L0→L9** :

| Contrainte | Description |
|------------|-------------|
| L0_FIRST | Les skills L0 (gouvernance) doivent être exécutés avant les skills L1+ |
| NO_CROSS_STRATE_DEP | Un skill L0 ne peut pas dépendre d'un skill L3+ |
| STRATE_MATCH | Le skill doit être dans la même strate ou une strate supérieure au repo cible |
| L9_LAST | Les skills L9 (archéologie) ne peuvent pas être activés automatiquement |

**Matrice de compatibilité** :

| Skill \ Repo | L0 | L1 | L2 | L2b | L3 | L4 | L5-L8 | L9 |
|--------------|----|----|----|-----|----|----|-------|----|
| L0 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| L1 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| L2 | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| L2b | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| L3 | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| L4 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| L5-L8 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| L9 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Phase 4 — Gestion des erreurs

| Erreur | Action |
|--------|--------|
| Repo non trouvé dans le registre | Erreur + feedback : "Repo X non enregistré dans known_repositories.yaml" |
| Repo en status `dormant` | Warning + feedback : "Repo X est dormant — activation manuelle requise" |
| Repo en status `deprecated` | Erreur + feedback : "Repo X est déprécié — choisir un autre repo" |
| Repo en status `archived` | Erreur + feedback : "Repo X est archivé — non routable" |
| Violation de strate | Erreur + feedback : "Skill L0 ne peut pas dépendre de repo L3+" |

## Règles de décision

- **Règle 1** : `known_repositories.yaml` est la source de vérité absolue (GATE-0)
- **Règle 2** : Un skill ne peut être routé que vers un repo `active`
- **Règle 3** : La hiérarchie L0→L9 doit être respectée (L0_FIRST, NO_CROSS_STRATE_DEP)
- **Règle 4** : Les repos L9 (archéologie) ne sont jamais routés automatiquement
- **Règle 5** : En cas de conflit de strate → privilégier la strate la plus haute (L0 > L9)
- **Règle 6** : Un skill peut être routé vers plusieurs repos si nécessaire (ex: nexus-auditor → NEXUS + FLUENCE)
- **Règle 7** : Si le repo cible n'existe pas → ne pas deviner → erreur explicite

## Format de sortie

```markdown
## SKILLS_ROUTER — Plan routé

### Plan d'exécution enrichi
| Step | Skill | Intent | Repo | Strate | Path |
|------|-------|--------|------|--------|------|
| 1 | reposcope-run | audit_structure | FLUENCE | L1 | D:\DO\WEB\FLUENCE |
| 2 | nexus-auditor | verifier_conformite | NEXUS | L0 | D:\DO\WEB\TOOLS\L0-CANON\NEXUS |
| 3 | workflow-orchestration | generer_rapport | SKILLS | L4 | D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS |

### Vérifications
- [x] Tous les repos existent dans known_repositories.yaml
- [x] Tous les repos sont en status `active`
- [x] La hiérarchie L0→L9 est respectée
- [x] Aucun repo L9 n'est routé
```

## Intégration avec l'écosystème

- **Dépôts concernés** : GOVERNANCE-HUB (known_repositories.yaml), SKILLS (MANIFEST.json)
- **Couche EECS** : L4_ORCHESTRATION
- **Skills dépendants** : skills-agentic.md (orchestrateur), skills-coverage.md (vérificateur)
- **Tags NEXUS** : [CONFORME_NEXUS], [SKILLS_AGENTIC]

## Contraintes

| Contrainte | Valeur |
|------------|--------|
| Source de vérité | known_repositories.yaml |
| Repos routables | status = `active` uniquement |
| Repos interdits | L9 (archéologie), dormant, deprecated, archived |
| Hiérarchie | L0→L9 obligatoire |
| Max repos par skill | 5 |
