# EPIC — SKILLS UAE-KEEL Phase 3 : generate_coords.py

**ID** : EPIC-SKILLS-UAE-KEEL-003
**Date de création** : 2026-06-07
**Auteur** : OPS-ENGINE
**Statut** : DRAFT
**Lié au PRD** : PRD_SKILLS_UAE_KEEL_METAMORPHIC_V1.md
**IntentHash** : `0xEPIC_SKILLS_UAE_KEEL_P3_20260607`

---

## 1. Vision

Créer le script `scripts/generate_coords.py` qui génère automatiquement `TAXONOMY/coords.yaml` depuis `MANIFEST.json`. Ce script élimine les mises à jour manuelles du MANIFEST.

---

## 2. Objectifs

| Objectif | Méthode de mesure |
|----------|-------------------|
| **Créer `scripts/generate_coords.py`** | Script Python autonome |
| **Idempotence** | 2 exécutions = même résultat |
| **Génération UAE** | Coordonnées calculées depuis les métadonnées MANIFEST |
| **Validation intégrée** | Le script valide son propre output |

---

## 3. Algorithme

```
1. Lire MANIFEST.json
2. Pour chaque skill :
   a. Lire strate, domaine, env, phase, urgence depuis frontmatter
   b. Calculer score UAE = 1/√d (distance au centre du plateau 5D)
   c. Attribuer zone LADYBIRD (≥80) / STANDARD (60-79) / BASIC (<60)
3. Écrire TAXONOMY/coords.yaml
4. Valider le output
```

---

## 4. Critères d'acceptation

1. Le script génère coords.yaml depuis MANIFEST.json
2. Idempotent : 2 executions = même résultat
3. Score UAE calculé pour chaque skill
4. Zone LADYBIRD attribuée
5. Validation intégrée (0 erreur)

---

## 5. Planning

| Tâche | Durée estimée |
|-------|---------------|
| Écrire le script | 1.5h |
| Tester avec les 64 skills | 0.5h |
| **Total** | **2h** |

---

*Fin de l'EPIC | IntentHash : `0xEPIC_SKILLS_UAE_KEEL_P3_20260607`*
