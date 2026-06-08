---
name: skill-router
version: "2.0.0"
description: "Routeur UAE pour le pipeline SKILLS_AGENTIC. Route les requêtes vers les skills pertinents via les coordonnées UAE 5D — sans règles codées en dur. Utilise TAXONOMY/coords.yaml comme source de vérité et calcule la distance euclidienne dans l'espace UAE. Utiliser quand l'utilisateur mentionne 'router UAE', 'routing géométrique', 'skill-router', 'UAE routing', 'distance UAE'."
triggers:
  - "router UAE"
  - "routing géométrique"
  - "skill-router"
  - "UAE routing"
  - "distance UAE"
  - "router skill"
  - "trouver skill"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SKILLS_AGENTIC", "UAE"]
prerequisites:
  - "TAXONOMY/coords.yaml (SKILLS)"
  - "skills-agentic.md (orchestrateur)"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-06", notes: "Version initiale — routing cross-repo via known_repositories.yaml"}
  - {v: "2.0.0", date: "2026-06-07", notes: "v2 — routing UAE géométrique via coords.yaml, plus de règles en dur"}
trit_primitive: TritResolvePath
---

# SKILL-ROUTER v2 — Routing UAE Géométrique

## Domaine et périmètre

Ce skill est le **routeur UAE** du pipeline SKILLS_AGENTIC v2. Contrairement à la v1 qui utilisait `known_repositories.yaml` pour le routing cross-repo, la v2 route via les **coordonnées UAE 5D** — sans règles codées en dur.

**Principe** : chaque skill a un point dans l'espace UAE 5D. La requête est aussi un point. Le routeur sélectionne les skills les plus proches (distance euclidienne minimale).

## Algorithme de routing

```
1. Parser la requête → vecteur UAE (strate, domaine, env, phase, urgence)
2. Charger TAXONOMY/coords.yaml
3. Pour chaque skill :
   a. Lire ses coordonnées UAE
   b. Calculer distance = √((s_r-s_s)² + (d_r-d_s)² + (e_r-e_s)² + (p_r-p_s)² + (u_r-u_s)²)
4. Trier par distance croissante
5. Sélectionner les N skills les plus proches (N = 5 par défaut)
6. Si distance_min > seuil → escalade HITL
```

## Format de sortie

```markdown
## SKILL-ROUTER v2 — Rapport de routing

### Requête
[Requête utilisateur]

### Coordonnées UAE de la requête
- Strate: [L0-L5]
- Domaine: [governance/sot/cognition/automation/git/agentic/domain/external]
- Env: [ENV1/ENV2/BOTH]
- Phase: [create/audit/fix/close/route]
- Urgence: [P0-P3]

### Skills sélectionnés (par distance croissante)
| Rang | Skill | Distance | Score UAE | Zone |
|------|-------|----------|-----------|------|
| 1 | [skill-1] | [d] | [score] | [zone] |
| 2 | [skill-2] | [d] | [score] | [zone] |
...

### Escalade HITL
[Si distance_min > seuil]
```

## Intégration avec l'écosystème

- **Dépôts concernés** : SKILLS (TAXONOMY/coords.yaml)
- **Couche EECS** : L4_ORCHESTRATION
- **Skills dépendants** : skills-agentic.md (orchestrateur), TAXONOMY/coords.yaml
- **Tags NEXUS** : [CONFORME_NEXUS], [SKILLS_AGENTIC], [UAE]

## Contraintes

| Contrainte | Valeur |
|------------|--------|
| Max skills sélectionnés | 5 |
| Seuil d'escalade HITL | distance > 8.0 |
| Source de vérité | TAXONOMY/coords.yaml |
| Pas de règles en dur | Tout est calculé |
