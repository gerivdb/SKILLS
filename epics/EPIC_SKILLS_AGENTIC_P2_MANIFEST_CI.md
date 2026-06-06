# EPIC — SKILLS_AGENTIC Phase 2 : Manifest v2 et CI Enrichie

**ID** : EPIC-SKILLS-AGENTIC-002
**Date de création** : 2026-06-06
**Auteur** : OPS-ENGINE
**Statut** : DRAFT — dépend de EPIC-SKILLS-AGENTIC-001
**Lié au PRD** : PRD_SKILLS_AGENTIC_RAG.md
**IntentHash** : `0xEPIC_SKILLS_AGENTIC_P2_20260606`

---

## 1. Vision

Enrichir le `MANIFEST.json` avec les métadonnées agentic (intents, coverage_rules, strate_constraints) et renforcer la CI pour valider automatiquement la conformité des skills agentic. Cette phase garantit que les skills créés en Phase 1 sont traçables, auditables, et que leur intégrité est vérifiée à chaque push.

---

## 2. Objectifs

| Objectif | Méthode de mesure |
|----------|-------------------|
| **Enrichir `MANIFEST.json` en v2** | Ajout des champs agentic : `intents`, `coverage_rules`, `strate_constraints`, `agentic_role` |
| **Enrichir `registry-sync.yml`** | Ajout de la validation du frontmatter agentic (vérification des champs obligatoires pour les skills agentic) |
| **Validation automatique** | La CI échoue si un skill agentic ne contient pas les champs requis |
| **Dashboard mis à jour** | Le `skills-dashboard.md` reflète les nouveaux skills et leur rôle agentic |

---

## 3. Périmètre

### Inclus
- `MANIFEST.json` v2 — enrichissement avec métadonnées agentic
- `.github/workflows/registry-sync.yml` v2 — validation agentic
- `skills-dashboard.md` — mise à jour avec les skills agentic

### Exclus
- Création de nouveaux skills (Phase 1)
- Tests fonctionnels (Phase 3)
- Revue croisée (Phase 4)

---

## 4. Livrables

| ID | Fichier | Description | Slots |
|----|---------|-------------|-------|
| L2.1 | `MANIFEST.json` v2 | Manifest enrichi avec champs agentic | 0 |
| L2.2 | `.github/workflows/registry-sync.yml` v2 | CI avec validation frontmatter agentic | 0 |
| L2.3 | `skills-dashboard.md` (mise à jour) | Dashboard reflétant les skills agentic | 0 |

**Impact total** : 0 slot (pas de nouveau skill)

---

## 5. Critères d'acceptation

1. **Manifest v2** : Le `MANIFEST.json` contient pour chaque skill agentic les champs : `agentic_role` (orchestrator/coverage/router), `intents` (liste), `coverage_rules` (liste), `strate_constraints` (L0-L9)
2. **CI agentic** : Le workflow `registry-sync.yml` valide la présence des champs agentic pour les skills ayant `agentic_role` défini
3. **CI lint** : Le workflow échoue si un skill agentic n'a pas les champs requis
4. **Dashboard** : Le `skills-dashboard.md` affiche les skills agentic avec leur rôle et leurs intents
5. **Rétrocompatibilité** : Les 59 skills existants sans `agentic_role` continuent de passer la CI

---

## 6. Dépendances

| Dépendance | Type | Statut |
|------------|------|--------|
| EPIC-SKILLS-AGENTIC-001 (Phase 1) | Précédence | ⏳ En cours |
| `MANIFEST.json` v1 | Base à enrichir | ✅ Existant |
| `registry-sync.yml` v1 | Base à enrichir | ✅ Existant |

---

## 7. Nouveaux champs MANIFEST.json v2

```json
{
  "name": "skills-agentic",
  "version": "1.0.0",
  "description": "...",
  "triggers": [...],
  "layer": "L4_ORCHESTRATION",
  "nexusTags": ["CONFORME_NEXUS"],
  "prerequisites": [],
  "slotWeight": 1,
  "status": "active",
  "changelog": [...],
  "agentic_role": "orchestrator",
  "intents": ["orchestrate_pipeline", "decompose_query", "activate_skills"],
  "coverage_rules": ["exhaustiveness", "competence", "strate", "dependency"],
  "strate_constraints": ["L0_FIRST", "L9_LAST", "NO_CROSS_STRATE_DEP"]
}
```

---

## 8. Planning

| Tâche | Durée estimée |
|-------|---------------|
| Enrichir `MANIFEST.json` en v2 | 1h |
| Enrichir `registry-sync.yml` | 1h |
| Mettre à jour `skills-dashboard.md` | 0.5h |
| Tests CI (dry-run) | 0.5h |
| **Total** | **3h (0.5 jour)** |

---

*Fin de l'EPIC | IntentHash : `0xEPIC_SKILLS_AGENTIC_P2_20260606`*
