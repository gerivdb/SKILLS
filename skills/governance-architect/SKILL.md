---
name: governance-architect
description: >
  Questionnement architectural par 4 mathèmes attracteurs (M1-M4).
  Active ce skill avant toute création d'artefact de gouvernance (PRD, ADR, INTENT, EPIC,
  design, workflow) pour vérifier les liens causaux entre mathématiques, personas L0,
  repos et patterns. Remplace la hiérarchie N-1->N6 par un topos de constellations.
version: 1.0.0
intent_hash: 0xSKILL_GOVERNANCE_ARCHITECT_20260805
---

# Governance Architect

## Déclencheur

Toute action qui :
- Crée ou modifie un artefact de gouvernance (PRD, ADR, INTENT, EPIC, MOC)
- Définit une architecture ou un design
- Crée un workflow, un pipeline, un script d'orchestration
- Ajoute ou modifie un pattern, un atome, un citizen
- Nécessite une validation cross-repo

## Protocole — 4 Questions Obligatoires

### Q1 (M1 — Continuité) : Topologie

```
Quelle est la structure du problème ?
- Quels sont les objets (ENV, repos, artifacts) ?
- Quels sont les morphismes (déploiements, transformations, workflows) ?
- Quels sont les invariants (symétries, cycles, points fixes) ?
- Comment les objets se recollent-ils en un faisceau cohérent ?
```

**Livrable** : Graphe ASCII ou Mermaid des objets/morphismes.

### Q2 (M2 — Information) : Mesure

```
Quelle est la mesure d'information pertinente ?
- Où est l'entropie ? (H = -Σ p_m log₂ p_m)
- Quelle est la complexité ? (Kolmogorov)
- Quels sont les signaux vs le bruit ?
- Comment mesurer la dérive sémantique ?
```

**Livrable** : Métriques H, K, seuils d'alerte.

### Q3 (M3 — Transformation) : Exécution

```
Comment transformer l'information en action vérifiable ?
- Quel est le morphisme d'exécution ?
- Comment vérifier la correctitude ? (Hoare, Milner)
- Quel est le rollback ? (F⁻¹∘F = id)
- Quelles sont les contraintes ENV2 ? (SSE4.2, 24Go, <50ms)
```

**Livrable** : Spécification d'exécution + rollback + contraintes.

### Q4 (M4 — Finalité) : Gouvernance

```
Quel est le contrat de gouvernance et de transmission ?
- Quelles personas L0 sont activées ?
- Quel est le contrat Default-FAIL ?
- Comment transmettre le savoir ? (documentation, verse, atome)
- Quel est le lien ADR/INTENT/PRD ?
```

**Livrable** : Mapping personas → mathèmes → repos → patterns.

## Règles Causalité

1. **Tout artifact DOIT être rattachable à un mathème.**
   Si aucun M1-M4 ne s'applique → STOP, demander HITL.

2. **Tout mathème DOIT avoir au moins une persona L0 dans VERSES/verses/.**
   Si persona manquante → créer verse + atome + citizen avant de continuer.

3. **Toute persona L0 DOIT être référencée dans unified-design/atoms/ ET REPO-STANDARDS/norms/.**
   Si référence manquante → créer/mettre à jour.

4. **Aucun workflow ne peut démarrer sans calcul de quorum par mathème.**
   ```
   Q(R) = ceil(Σ_{i=1..4} w_i(M_i activés) × 0.75)
   ```
   Si Q(R) < seuil → STOP.

5. **La distance de Wasserstein entre distributions de patterns activés**
   **dans chaque couple de mathèmes DOIT être ≤ 0.5.**
   Si W > 0.5 → alerte, demander médiateur.

6. **La topologie grothendieckienne est l'orchestration par défaut.**
   Chaque ENV = objet, chaque déploiement = morphisme,
   `𝔽_KEEL` = faisceau cohérent sur le site TOPOS.

7. **Default-FAIL** : Un critère ne passe à `true` QUE si preuve tangible
   (hash, log, diff, test_output).

## Mapping Patterns → Mathèmes

| Pattern | Mathème(s) |
|---------|------------|
| @constructive | M3 |
| @entropy | M2 |
| @knuth+@mem_bound | M2 |
| @feynman+@dimension | M3 |
| @lurie_higher_topos | M4 |
| @lafforgue_langlands | M4 |
| @voevodsky_motifs | M4 |
| @vapnik_vc | M2 |
| @mackay_bayes | M2 |
| @scholkopf_kernel | M2 |
| @learning | M2 |
| @jordan_stat | M2 |
| @schmidhuber_metalearn | M2 |
| @symmetry+@topos_rollback | M1 |
| @dijkstra_graph | M1 |
| @berry_causal | M1 |
| @mandelbrot_fractal | M1 |
| @wolfram_automata | M1 |
| @julia_iteration | M1 |
| @feigenbaum_bifurcation | M1 |
| @nash_equilibrium | M1 |
| @bellman_dynamic | M1 |
| @hoare_contract | M3 |
| @milner_types | M3 |
| @sifakis_components | M3 |
| @mccarthy_metalang | M3 |
| @numa | M3 |
| @turing | M3 |
| @feynman | M3 |
| @kolmogorov | M2 |
| @deploy+@compile | M3 |
| @usecase | M4 |
| @sdk | M4 |
| @illusie_fantechi_doc | M4 |
| @audit | M4 |
| @perf | M3 |
| @sse4_only+@zig_0.14 | M3 |
| @korx_372b+@kbin_context | M3 |
| @q243_format+@piano_diff | M1 |
| @boinc_p2p | M3 |
| @cold_start_2s+@causal_latency_50ms | M1 |
| @rlm_243 | M3 |
| @db_schema_v1.0 | M4 |
| @acid_tx_v1.0 | M4 |
| @crm_workflow_v1.0 | M4 |
| @office_export_v1.0 | M4 |

## Workflow d'Implémentation

```yaml
wf create_artifact
resonate M4
vote grothendieck deligne hassani
exec write_prd
ckpt save_metadata
audit check_quorum
merge go
```

## Vérification

Avant toute implémentation, exécuter `architectural-questionnaire.ps1` :
- Q1 : Topologie
- Q2 : Entropie H ≤ 0.6
- Q3 : Rollback F⁻¹∘F = id
- Q4 : Personas L0 présentes

## Références

- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05
- **INTENT** : INTENT-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05
- **META-DESIGN** : unified-design/docs/MATHEMES-FRAMEWORK.md
- **KEEL PRD-005** : TOPOS comme catégorie de sites Grothendieck
- **SCI-VERSE** : VERSES/verses/sci-verse.md
