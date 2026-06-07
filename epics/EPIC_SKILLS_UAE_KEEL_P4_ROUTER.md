# EPIC — SKILLS UAE-KEEL Phase 4 : skill-router UAE

**ID** : EPIC-SKILLS-UAE-KEEL-004
**Date de création** : 2026-06-07
**Auteur** : OPS-ENGINE
**Statut** : DRAFT
**Lié au PRD** : PRD_SKILLS_UAE_KEEL_METAMORPHIC_V1.md
**IntentHash** : `0xEPIC_SKILLS_UAE_KEEL_P4_20260607`

---

## 1. Vision

Créer le skill `skill-router` qui permet au DELEGATOR de router via les coordonnées UAE **sans règles codées en dur**. Le routing est purement géométrique dans l'espace UAE 5D.

---

## 2. Objectifs

| Objectif | Méthode de mesure |
|----------|-------------------|
| **Créer `skill-router.md`** | Skill de routing UAE dynamique |
| **Routing géométrique** | Distance UAE entre requête et skills |
| **Pas de règles en dur** | Tout est calculé depuis coords.yaml |
| **Test** | 10 requêtes → 10 routages corrects |

---

## 3. Algorithme de routing

```
1. Parser la requête → vecteur UAE (strate, domaine, env, phase, urgence)
2. Charger coords.yaml
3. Pour chaque skill : calculer distance UAE = √(Σ(axe_requête - axe_skill)²)
4. Trier par distance croissante
5. Sélectionner les N skills les plus proches
6. Si distance > seuil → escalade HITL
```

---

## 4. Critères d'acceptation

1. Le skill-router route via UAE sans règles codées en dur
2. 10 requêtes test → 10 routages corrects
3. Le format KEEL v0.5 est respecté dans les foncteurs
4. Le skill passe le lint YAML
5. BDCP inviolé

---

## 5. Planning

| Tâche | Durée estimée |
|-------|---------------|
| Écrire skill-router.md | 1.5h |
| Tester le routing | 0.5h |
| **Total** | **2h** |

---

*Fin de l'EPIC | IntentHash : `0xEPIC_SKILLS_UAE_KEEL_P4_20260607`*
