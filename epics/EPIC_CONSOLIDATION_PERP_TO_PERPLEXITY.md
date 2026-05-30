# EPIC – Consolidation du registre de compétences Perplexity (Perp → Perplexity)

**ID** : EPIC-PERP-CONSOLIDATION-001  
**Date de création** : 2026-05-30  
**Auteur** : OPS‑ENGINE (suite à la revue Selena + Riddler + SABRE + Alfred)  
**Statut** : En attente de planification  
**Lié au PRD** : PRD.md (situé dans le même dossier)  

---

## 1. Vision

Réduire la dette technique du registre de compétences Perplexity en comblant les lacunes critiques, en éliminant les redondances et en assurant une gouvernance légère, tout en restant strictement dans la contrainte du SaaS Perplexity (1 skill = 1 slot, plafond 100 slots).

---

## 2. Objectifs

| Objectif | Méthode de mesure |
|----------|-------------------|
| **Comblér les lacunes critiques** (résilience MCP/Écriture et production de PRD) | Création de deux nouvelles compétences : `mcp-write-guard.md` et `prd-factory.md`. |
| **Éliminer les redondances** via quatre fusions de compétences éprouvées | Fusion des groupes :<br>• `ecos‑vision` ×3 → `ecos‑vision v2`<br>• `hitl‑hub` + `hitl‑ops` → `hitl‑core`<br>• `analyse‑repo‑deepwiki` + `deepwiki_repo_enricher` → `deepwiki‑ops`<br>• `fermi‑legacy` + `scientific‑method` → `reasoning‑toolkit` |
| **Maintenir le plafond de 100 slots** | Après les ajouts et fusions, le nombre total de compétences actives doit être ≤ 100, idéalement 50 pour laisser 50 slots de marge. |
| **Instaurer une gouvernance légère** | Ajout d’un `MANIFEST.json`, d’un `skills‑dashboard.md`, et de workflows CI limités au lint YAML + comptage de fichiers. Aucun sur‑engineering (pas de slotWeight fractionnaire, pas de sous‑dossiers invisibles au runtime). |
| **Assurer la traçabilité et la versionnage** | Chaque compétence possède un front‑matter YAML avec `version:` et `changelog:`. |
| **Faciliter la découverte et l’utilisation** | Toutes les compétences restent dans le même dossier plat (`perplexity/`) ; aucun sous‑dossier `versus/` n’est créé afin d’être visible par le runtime Perplexity. |

---

## 3. Périmètre

- **Inclus** : Toutes les compétences présentes dans `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\perplexity\` (fichiers `.md`).  
- **Exclus** : Tout sous‑dossier tel que `versus/`, `skill‑verse/` ou toute structure hiérarchique qui ne serait pas incluse dans le ZIP déployé vers le SaaS Perplexity.  
- **Contraintes techniques** :  
  - Chaque fichier `.md` compte pour **exactement un slot** dans le SaaS.  
  - Le champ `slotWeight` du front‑matter est uniquement un indicateur interne de priorité/complexité ; il n’est pas utilisé par le SaaS pour le calcul des slots.  
  - Le pipeline CI se limite à la validation du format YAML/Markdown et au comptage de fichiers `.md`.  
  - L’analyse de similarité sémantique sera réalisée **manuellement** (ex. tous les trimestres) et non intégrée à chaque push.

---

## 4. Livrables (epics → stories)

| Story ID | Description | Type | Impact slots |
|----------|-------------|------|--------------|
| **S1** | Créer `mcp-write-guard.md` (nouvelle compétence) | Nouvelle compétence | +1 |
| **S2** | Créer `prd-factory.md` (nouvelle compétence) | Nouvelle compétence | +1 |
| **S3** | Mettre à jour `plix-core.md` v2 (ajout ThermoGate + VDB, version, changelog) | Mise à jour | 0 |
| **S4** | Mettre à jour `github-config.md` v2 (stratégie gros fichiers, version, changelog) | Mise à jour | 0 |
| **S5** | Fusionner `ecos‑vision.md`, `ecosystem‑self.md`, `lecun‑vision.md` → `ecos‑vision v2.md` | Fusion | –2 |
| **S6** | Fusionner `hitl‑hub.md` + `hitl‑ops.md` → `hitl‑core.md` | Fusion | –1 |
| **S7** | Fusionner `analyse‑repo‑deepwiki.md` + `deepwiki_repo_enricher.md` → `deepwiki‑ops.md` | Fusion | –1 |
| **S8** | Fusionner `fermi‑legacy.md` + `scientific‑method.md` → `reasoning‑toolkit.md` | Fusion | –2 |
| **S9** | Générer / mettre à jour `MANIFEST.json` (liste déclarative de toutes compétences) | Artefact de gouvernance | 0 |
| **S10** | Générer / mettre à jour `skills‑dashboard.md` (slot total, marge, heatmap de similarité) | Artefact de gouvernance | 0 |
| **S11** | Créer les workflows CI `validate-skills.yml` et `registry-sync.yml` (lint YAML uniquement + comptage) | Infrastructure CI | 0 |
| **S12** | Réviser et approuver les changements avec le Skill Council (réunion de validation) | Processus de gouvernance | 0 |

**Total net d’impact sur les slots** :  
+2 (nouvelles compétences) –6 (fusins) = **–4 slots** (c’est‑à‑dire 4 slots libérés).  
En partant d’un état actuel de 53 compétences, on obtient **49 compétences actives** après l’épic, laissant **51 slots libres** (marge confortable).

---

## 5. Critères d’acceptation (Definition of Done)

1. **Slot count** : Après merge de l’épic, le nombre de fichiers `.md` dans `perplexity/` doit être **≤ 50** (idéalement 49‑50).  
2. **Format YAML** : Chaque compétence contient les champs obligatoires (`name`, `version`, `description`, `triggers`, `layer`, `nexusTags`, `prerequisites`, `slotWeight`, `status`, `changelog`).  
3. **CI vert** : Le workflow `validate-skills.yml` s’exécute avec succès (code de sortie 0) sur la branche `main`.  
4. **Documentation à jour** : `MANIFEST.json` et `skills‑dashboard.md` présents et reflétant l’état actuel des compétences.  
5. **Pas d’artefacts de sur‑engineering** : Aucun dossier `versus/`, aucun usage de `slotWeight` pour le calcul de slots SaaS, aucune dépendance lourde (sentence‑transformers, etc.) dans les workflows CI.  
6. **Approbation du Skill Council** : Une issue labelée `skill‑council‑review` doit être clôturée avec l’approbation avant le merge vers `main`.

---

## 6. Planning (sprints de deux semaines)

| Sprint | Objectif principal | Livrables |
|--------|-------------------|-----------|
| **Sprint 0** (préparation) | Créer les branches de feature, préparer les scripts CI lint. | Branches `feature/mcp-write-guard`, `feature/prd-factory`, `feature/plix-core-v2`, `feature/github-config-v2`. |
| **Sprint 1** (Phase 1 – créations & mises à jour) | Livrer les deux nouvelles compétences et les deux mises à jour de base. | `mcp-write-guard.md`, `prd-factory.md`, `plix-core.md` v2, `github-config.md` v2, mise à jour du `MANIFEST.json`, génération du dashboard, PR prêt pour revue. |
| **Sprint 2** (Phase 2 – fusions) | Réaliser les quatre fusions, supprimer les compétences sources, créer les compétences fusionnées. | `ecos‑vision v2.md`, `hitl‑core.md`, `deepwiki‑ops.md`, `reasoning‑toolkit.md`, suppression des 6 compétences sources, mise à jour du manifeste et du dashboard. |
| **Sprint 3** (Validation & clôture) | Exécuter le pipeline CI, vérifier le slot count, obtenir l’approbation du Skill Council, merger. | Commit final `push_files` contenant l’ensemble des livrables de l’épic. |

---

## 7. Risques et mesures d’atténuation

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| **Oublier de supprimer une compétence source après fusion** (dépassement du plafond) | Moyenne | Haut | Le workflow CI compte les fichiers `.md` et échoue si > 100 ; revue manuelle du diff avant merge. |
| **Perte de contenu lors de la fusion** (omission d’une règle importante) | Faible | Moyen | Chaque fusion est réalisée par copie‑collé manuel suivie d’une revue détaillée par le Skill Council ; le changelog liste les sections provenant de chaque skill source. |
| **CI trop lourd** (introduction accidentelle de dépendances lourdes) | Faible | Moyen | Le fichier CI est limité à `actions/checkout`, `actions/setup-python` et un script de lint YAML ; toute ajout de dépendance doit être approuvé par la revue CI. |
| **Ambiguïté de déclencheurs après fusion** (utilisateurs ne trouvent plus la compétence attendue) | Faible | Moyen | Les compétences fusionnées conservent **tous** les déclencheurs des skills sources dans le champ `triggers` du front‑matter. |
| **Déviation du processus de versioning** | Faible | Faible | Le champ `version:` est obligatoire ; le workflow lint vérifie sa présence et son format sémantique. |

---

## 8. Ouverture

> **Prochaine étape** : Lancer immédiatement la **Phase 1** (Sprint 1) en un seul commit `push_files` contenant les quatre livrables de création/mise à jour (`mcp-write-guard.md`, `prd-factory.md`, `plix-core.md` v2, `github-config.md` v2).  
> Une fois ce commit mergé, enchainer avec la **Phase 2** (Sprint 2) pour réaliser les fusions, puis finaliser avec la validation et le clôture de l’épic.

---

### Annexes

- **Annexe A** – Modèle de front‑matter YAML obligatoire pour toutes compétences.  
- **Annexe B** – Exemple de `MANIFEST.json` généré.  
- **Annexe C** – Script de lint YAML utilisé dans `validate-skills.yml`.  
- **Annexe D** – Exemple de `skills‑dashboard.md` généré.  

--- 

*Fin de l’EPIC*