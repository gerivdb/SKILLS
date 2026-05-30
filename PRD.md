# PRD – Optimisation du registre de compétences Perplexity (ECOS L4‑TOOLS)

**Version** : 1.0  
**Date** : 2026‑05‑30  
**Auteur** : OPS‑ENGINE (revue Selena + Riddler + SABRE + Alfred)  
**Statut** : Approuvé pour implémentation immédiate

---

## 1. Objectif

Réduire la dette technique du registre de compétences Perplexity en :

1. **Comblant deux lacunes critiques** identifiées lors de l’audit (résilience MCP/Écriture et production de PRD).  
2. **Eliminant les redondances** via quatre fusions de compétences éprouvées.  
3. **Garantissant la conformité au plafond de 100 slots** du SaaS Perplexity (1 skill = 1 slot).  
4. **Mettant en place une gouvernance légère** (versioning, changelog, tableau de bord) sans introduire d’over‑engineering.

Le résultat visé est **50 compétences actives** laissant **50 slots libres** pour les évolutions futures (domaines L5‑L7, nouveaux besoins métier, etc.).

---

## 2. Portée

- **Compétences concernées** : toutes les compétences présentes dans le dossier  
  `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\perplexity\`.  
- **Exclusions** : aucun sous‑dossier `versus/` ou `skill‑verse` n’est créé, car le runtime Perplexity ne lit que le fichier ZIP à plat (règle 8 du `SKILL_FORMAT_CANONICAL.md`).  
- **Contraintes** :  
  - Chaque fichier `.md` représente exactement **un slot**.  
  - Aucun mécanisme de `slotWeight` fractionnaire n’est pris en compte par le SaaS ; le champ `slotWeight` restera uniquement un indicateur interne de priorité/complexité.  
  - Le pipeline CI se limite à la validation du format YAML/Markdown et au comptage de fichiers.  
  - L’analyse de similarité sémantique sera effectuée **manuellement** (trimestriel) et non intégrée à chaque push.

---

## 3. Fonctionnalités / Livrables

| ID | Livrable | Description | Impact slots |
|----|----------|-------------|--------------|
| **F1** | `mcp-write-guard.md` | Nouvelle compétence couvrant la résilience d’écriture MCP (payload‑size estimator, retry‑strategy escalator, session‑context monitor, fail‑verbosity). | +1 |
| **F2** | `prd-factory.md` | Nouvelle compétence pour la production complète d’un PRD (spec‑cross‑validator, okr‑consistency‑checker, guide de rédaction PRD canonique). | +1 |
| **F3** | `plix-core.md` (v2) | Mise à jour : ajout de la couverture ThermoGate et VDB, champ `version:`, `changelog:`. | 0 |
| **F4** | `github-config.md` (v2) | Mise à jour : ajout de la stratégie de gestion des gros fichiers (push_files vs create_or_update, split‑payload, SHA‑management), champ `version:`, `changelog:`. | 0 |
| **F5** | `ecos‑vision v2.md` | Fusion de `ecos‑vision.md`, `ecosystem‑self.md`, `lecun‑vision.md` → une seule compétence enrichie. | –2 |
| **F6** | `hitl‑core.md` | Fusion de `hitl‑hub.md` + `hitl‑ops.md`. | –1 |
| **F7** | `deepwiki‑ops.md` | Fusion de `analyse‑repo‑deepwiki.md` + `deepwiki_repo_enricher.md`. | –1 |
| **F8** | `reasoning‑toolkit.md` | Fusion de `fermi‑legacy.md` + `scientific‑method.md` (pruning‑explainer conservé séparément pending verification). | –2 |
| **F9** | `MANIFEST.json` | Fichier déclaratif listant toutes compétences avec métadonnées (name, version, description, triggers, layer, nexusTags, prerequisites, slotWeight = 1, status, changelog). Utilisé pour le tableau de bord interne et la génération du ZIP de déploiement. | 0 |
| **F10** | `skills‑dashboard.md` | Tableau de bord généré automatiquement (slot total, marge, heatmap de similarité, liste des compétences dépréciées). | 0 |
| **F11** | Workflows CI (`validate-skills.yml`, `registry-sync.yml`) | Lint YAML uniquement (vérifie front‑matter, présence des sections obligatoires) + comptage de fichiers `.md`. En cas de PR, poste un commentaire avec le résultat du lint. | 0 |

---

## 4. Critères d’acceptation

1. **Slot count** : Après merge du commit de Phase 1 + Phase 2, le nombre de fichiers `.md` dans `perplexity/` doit être exactement **50**.  
2. **Format** : Chaque compétence doit contenir le front‑matter YAML requis (`name`, `version`, `description`, `triggers`, `layer`, `nexusTags`, `prerequisites`, `slotWeight`, `status`, `changelog`).  
3. **CI vert** : Le workflow `validate-skills.yml` doit s’exécuter avec succès (code de sortie 0) sur la branche `main`.  
4. **Documentation** : Le `MANIFEST.json` et le `skills‑dashboard.md` doivent être présents et à jour après chaque merge.  
5. **Absence d’artefacts de sur‑engineering** : Aucun dossier `versus/`, aucun champ `slotWeight` utilisé pour le calcul de slots SaaS, aucune dépendance lourde (sentence‑transformers, etc.) dans les workflows CI.  

---

## 5. Planning (sprints de deux semaines)

| Sprint | Objectif | Livrables |
|--------|----------|-----------|
| **Sprint 0** (préparation) | Créer les branches de feature, copier le template de skill, préparer les scripts CI lint. | Branches `feature/mcp-write-guard`, `feature/prd-factory`, `feature/plix-core-v2`, `feature/github-config-v2`. |
| **Sprint 1** (Phase 1) | Implémenter les deux nouvelles compétences et mettre à jour les deux compétences de base. | `mcp-write-guard.md`, `prd-factory.md`, `plix-core.md` v2, `github-config.md` v2, mise à jour du `MANIFEST.json`, génération du dashboard, création du PR. |
| **Sprint 2** (Phase 2 – fusions) | Réaliser les quatre fusions, supprimer les compétences redondantes, créer les compétences fusionnées. | `ecos‑vision v2.md`, `hitl‑core.md`, `deepwiki‑ops.md`, `reasoning‑toolkit.md`, suppression de les 6 compétences sources, mise à jour du manifeste et du dashboard. |
| **Sprint 3** (validation & clôture) | Exécuter le pipeline CI sur la branche `main`, vérifier le slot count, obtenir l’approbation du Skill Council, merger. | Commit final `push_files` contenant les 8 livrables (4 créations/updates + 4 fusions). |

*Chaque sprint inclut une revue de code légère (auteur + un reviewer) et une mise à jour du changelog des compétences modifiées.*

---

## 6. Risques et mesures d’atténuation

| Risque | Probabilité | Impact | Mitigation |
|--------|--------------|--------|------------|
| **Mauvaise comptabilisation des slots** (oublier de supprimer une compétence source après fusion) | Moyenne | Haut (dépassement du plafond) | Le workflow CI compte les fichiers `.md` et échoue si le total dépasse 100 ; revue manuelle du diff avant merge. |
| **Perte de contenu lors de la fusion** (omission d’une règle importante) | Faible | Moyen | Chaque fusion est réalisée par copie‑collé manuel suivi d’une revue détaillée par le Skill Council ; le changelog liste les sections provenant de chaque skill source. |
| **CI trop lourd** (introduction accidentelle de dépendances lourdes) | Faible | Moyen | Le fichier CI est limité à `actions/checkout`, `actions/setup-python`, et un script de lint YAML ; toute ajout de dépendance doit être approuvé par le revue CI. |
| **Ambiguïté de déclencheurs après fusion** (les utilisateurs ne trouvent plus la compétence attendue) | Faible | Moyen | Les compétences fusionnées conservent tous les déclencheurs des skills sources dans le champ `triggers` du front‑matter. |
| **Déviation du processus de versioning** | Faible | Faible | Le champ `version:` est obligatoire dans le front‑matter ; le workflow lint vérifie sa présence et son format sémantique. |

---

## 7. Ouverture du travail

> **Prochaine étape** : Lancer immédiatement la **Phase 1** en un seul commit `push_files` contenant les quatre livrables (F1‑F4).  
> Une fois ce commit mergé, lancer la **Phase 2** (fusions) suivant le même schéma.

---

### Annexes

- **Annexe A** – Modèle de front‑matter YAML obligatoire pour toutes compétences.  
- **Annexe B** – Exemple de `MANIFEST.json` généré.  
- **Annexe C** – Script de lint YAML utilisé dans `validate-skills.yml`.  
- **Annexe D** – Exemple de `skills‑dashboard.md` généré.

--- 

*Fin du PRD*  